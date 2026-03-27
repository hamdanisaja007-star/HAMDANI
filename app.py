import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_sukabumi"

# --- KONFIGURASI DATABASE & FOLDER (VERCEL FRIENDLY) ---
# Menggunakan /tmp/ agar tidak error 'Read-only file system' di Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Daftar Kategori Utama Berkas
KATEGORI_LIST = ['Kenaikan_Pangkat', 'Kenaikan_Jabatan', 'Pensiun', 'Berkas_Umum']

db = SQLAlchemy(app)

# --- MODELS ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100))
    jenis_pegawai = db.Column(db.String(10), default='PNS')
    pangkat_gol = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    desa_binaan = db.Column(db.String(100))
    tmt_pangkat = db.Column(db.Date, nullable=True)
    tgl_lahir = db.Column(db.Date)

# --- FUNGSI OTOMATISASI FOLDER ---
def buat_folder_pegawai(nama_pegawai):
    folder_aman = nama_pegawai.replace(" ", "_")
    for kat in KATEGORI_LIST:
        path = os.path.join(app.config['UPLOAD_FOLDER'], kat, folder_aman)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

# --- ROUTES ---

@app.route('/')
def landing():
    if 'user_role' in session: 
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    user_in = request.form.get('username')
    pass_in = request.form.get('password')
    
    # Login Admin
    if user_in == "admin" and pass_in == "admin123":
        session['user_role'] = 'admin'
        flash("Selamat Datang Admin R&D IPeKB!", "success")
        return redirect(url_for('dashboard'))
    
    # Login PLKB via NIP
    user_plkb = Pegawai.query.filter_by(nip=user_in).first()
    if user_plkb:
        session['user_role'] = 'plkb'
        session['user_nip'] = user_in
        flash(f"Selamat Datang, {user_plkb.nama}", "info")
        return redirect(url_for('dashboard'))
        
    flash("Akses Ditolak! NIP atau Password Salah.", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: 
        return redirect(url_for('landing'))
    
    role = session['user_role']
    today = date.today()
    pegawai_list = Pegawai.query.all()
    
    # --- LOGIKA REKAPAN DASHBOARD ---
    total_pegawai = len(pegawai_list)
    pns_count = Pegawai.query.filter_by(jenis_pegawai='PNS').count()
    pppk_count = Pegawai.query.filter_by(jenis_pegawai='PPPK').count()
    
    notif_pangkat = []
    notif_pensiun = []
    berkas_masuk = []

    # Hitung Otomatis Naik Pangkat & Pensiun
    for p in pegawai_list:
        if p.jenis_pegawai == 'PNS':
            # Estimasi Naik Pangkat (4 Tahun = 1460 hari)
            if p.tmt_pangkat and (today - p.tmt_pangkat).days >= 1460:
                notif_pangkat.append(p)
            # Estimasi Pensiun (Usia 58 Tahun = ~21170 hari)
            if p.tgl_lahir and (today - p.tgl_lahir).days >= 21170:
                notif_pensiun.append(p)

    # Scan Berkas (Hanya jika Admin)
    if role == 'admin':
        for kat in KATEGORI_LIST:
            kat_path = os.path.join(app.config['UPLOAD_FOLDER'], kat)
            if os.path.exists(kat_path):
                for folder_nama in os.listdir(kat_path):
                    pegawai_folder = os.path.join(kat_path, folder_nama)
                    if os.path.isdir(pegawai_folder):
                        for file in os.listdir(pegawai_folder):
                            berkas_masuk.append({
                                'nama_file': file, 
                                'kategori': kat, 
                                'pemilik': folder_nama.replace("_", " ")
                            })
    
    user_data = Pegawai.query.filter_by(nip=session.get('user_nip')).first() if role == 'plkb' else None

    return render_template('index.html', 
                           role=role, 
                           user_data=user_data, 
                           pegawai=pegawai_list, 
                           total=total_pegawai,
                           pns=pns_count,
                           pppk=pppk_count,
                           notif_pangkat=notif_pangkat,
                           notif_pensiun=notif_pensiun,
                           berkas=berkas_masuk,
                           today=today)

@app.route('/tambah_pegawai', methods=['POST'])
def tambah_pegawai():
    if session.get('user_role') != 'admin': return redirect(url_for('landing'))
    try:
        nama = request.form.get('nama')
        tmt = datetime.strptime(request.form.get('tmt'), '%Y-%m-%d').date() if request.form.get('tmt') else None
        lahir = datetime.strptime(request.form.get('lahir'), '%Y-%m-%d').date()
        
        baru = Pegawai(
            nip=request.form.get('nip'), 
            nama=nama, 
            jabatan=request.form.get('jabatan'),
            jenis_pegawai=request.form.get('jenis_pegawai'),
            pangkat_gol=request.form.get('pangkat_gol'),
            kecamatan=request.form.get('kecamatan'),
            desa_binaan=request.form.get('desa_binaan'),
            tmt_pangkat=tmt, 
            tgl_lahir=lahir
        )
        db.session.add(baru)
        db.session.commit()
        buat_folder_pegawai(nama)
        flash(f"Data {nama} Berhasil Disimpan!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Gagal Simpan: {str(e)}", "danger")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# Inisialisasi Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
