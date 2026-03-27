import os
import pandas as pd
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- KONFIGURASI DATABASE & FOLDER (MODIFIKASI AMAN VERCEL) ---
# Gunakan /tmp/ agar Vercel bisa menulis database sementara
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS (Sesuai Rancangan Bos) ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100))
    jenis_pegawai = db.Column(db.String(10), default='PNS') # PNS / PPPK
    pangkat_gol = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    desa_binaan = db.Column(db.String(200))
    no_hp = db.Column(db.String(20))
    tmt_pangkat = db.Column(db.Date, nullable=True)
    tgl_lahir = db.Column(db.Date, nullable=True)

class BankSoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)

class Pesan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pengirim = db.Column(db.String(100))
    nip_pengirim = db.Column(db.String(20))
    isi_pesan = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.now)

# --- FUNGSI OTOMATISASI FOLDER (Logika Bos) ---
def buat_folder_pegawai(pegawai_obj):
    folder_aman = pegawai_obj.nama.replace(" ", "_")
    status = pegawai_obj.jenis_pegawai 
    
    kategori_wajib = ['Berkas_Umum']
    if status == 'PNS':
        kategori_spesifik = ['Kenaikan_Pangkat', 'Kenaikan_Jabatan', 'Pensiun']
    else:
        kategori_spesifik = ['Perpanjangan_Kontrak', 'Kenaikan_Golongan']
    
    for kat in kategori_wajib + kategori_spesifik:
        path = os.path.join(app.config['UPLOAD_FOLDER'], status, folder_aman, kat)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

# --- ROUTES ---
@app.route('/')
def landing():
    if 'user_role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    user_in = request.form.get('username')
    pass_in = request.form.get('password')
    
    if user_in == "admin" and pass_in == "admin123":
        session['user_role'] = 'admin'
        return redirect(url_for('dashboard'))
    
    user_plkb = Pegawai.query.filter_by(nip=user_in).first()
    if user_plkb:
        session['user_role'] = 'plkb'
        session['user_nip'] = user_in
        return redirect(url_for('dashboard'))
        
    flash("Akses Ditolak! NIP atau Password Salah.", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    today = date.today()
    pegawai_list = Pegawai.query.all()
    pesan_list = Pesan.query.order_by(Pesan.tanggal.desc()).all()
    
    berkas_masuk = []
    berkas_saya = []
    notif_pangkat = []
    notif_pensiun = []
    user_data = None

    if role == 'admin':
        # Logika Notifikasi Pangkat & Pensiun
        for p in pegawai_list:
            if p.jenis_pegawai == 'PNS' and p.tmt_pangkat:
                if (today - p.tmt_pangkat).days >= 1370: notif_pangkat.append(p.nama)
            if p.tgl_lahir and (today - p.tgl_lahir).days >= 20805:
                notif_pensiun.append(p.nama)
    else:
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()

    return render_template('index.html', role=role, user_data=user_data, 
                           pegawai=pegawai_list, today=today,
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun,
                           pesan_masuk=pesan_list)

@app.route('/tambah_pegawai', methods=['POST'])
def tambah_pegawai():
    try:
        tmt = datetime.strptime(request.form.get('tmt'), '%Y-%m-%d').date() if request.form.get('tmt') else None
        lahir = datetime.strptime(request.form.get('lahir'), '%Y-%m-%d').date() if request.form.get('lahir') else None
        
        baru = Pegawai(
            nip=request.form.get('nip'), nama=request.form.get('nama'), 
            jabatan=request.form.get('jabatan'), jenis_pegawai=request.form.get('jenis_pegawai'),
            pangkat_gol=request.form.get('pangkat_gol'), kecamatan=request.form.get('kecamatan'), 
            desa_binaan=request.form.get('desa_binaan'), no_hp=request.form.get('no_hp'), 
            tmt_pangkat=tmt, tgl_lahir=lahir
        )
        db.session.add(baru)
        db.session.commit()
        # Nonaktifkan sementara buat_folder di Vercel agar tidak error
        # buat_folder_pegawai(baru) 
        flash(f"Data {baru.nama} Berhasil Disimpan!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Gagal Simpan: {str(e)}", "danger")
    return redirect(url_for('dashboard'))

@app.route('/export_excel')
def export_excel():
    pegawai = Pegawai.query.all()
    data_excel = [{
        'NIP': p.nip, 'Nama': p.nama, 'Status': p.jenis_pegawai,
        'Gol/Pangkat': p.pangkat_gol, 'Jabatan': p.jabatan, 
        'Kecamatan': p.kecamatan, 'Desa Binaan': p.desa_binaan,
        'No HP': p.no_hp, 'TMT Pangkat': p.tmt_pangkat, 'Tgl Lahir': p.tgl_lahir
    } for p in pegawai]
    
    df = pd.DataFrame(data_excel)
    f_path = '/tmp/Laporan_Kepegawaian.xlsx'
    df.to_excel(f_path, index=False)
    return send_file(f_path, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# --- INISIALISASI DATABASE ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
