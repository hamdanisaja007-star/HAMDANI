import os
import pandas as pd
# Gunakan timezone lokal jika perlu, default menggunakan datetime.now
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- KONFIGURASI DATABASE & FOLDER ---
# Menggunakan /tmp/ agar kompatibel dengan beberapa layanan hosting (seperti Vercel/PythonAnywhere)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['CHAT_UPLOAD'] = '/tmp/chat_files'
app.config['LOKER_PLKB'] = '/tmp/loker_plkb'  # Folder arsip mandiri PLKB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pastikan semua folder penyimpanan tersedia
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CHAT_UPLOAD'], exist_ok=True)
os.makedirs(app.config['LOKER_PLKB'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# --- MODELS ---
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

class Pengumuman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    file_lampiran = db.Column(db.String(200), nullable=True)
    admin_name = db.Column(db.String(50), default="Admin Kabupaten")
    tanggal = db.Column(db.DateTime, default=datetime.now)
    logs = db.relationship('LogBaca', backref='pengumuman', cascade="all, delete-orphan")

class LogBaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengumuman_id = db.Column(db.Integer, db.ForeignKey('pengumuman.id'), nullable=False)
    nip_pembaca = db.Column(db.String(20), nullable=False)
    nama_pembaca = db.Column(db.String(100))
    waktu_baca = db.Column(db.DateTime, default=datetime.now)

# --- ROUTES AUTENTIKASI ---

@app.route('/')
def landing():
    if 'user_role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    user_in = request.form.get('username')
    pass_in = request.form.get('password')
    
    # Login Admin
    if user_in == "admin" and pass_in == "admin123":
        session['user_role'] = 'admin'
        return redirect(url_for('dashboard'))
    
    # Login PLKB via NIP
    user_plkb = Pegawai.query.filter_by(nip=user_in).first()
    if user_plkb:
        session['user_role'] = 'plkb'
        session['user_nip'] = user_in
        return redirect(url_for('dashboard'))
        
    flash("Akses Ditolak! NIP atau Password Salah.", "danger")
    return redirect(url_for('landing'))

# --- DASHBOARD UTAMA ---
@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    today = date.today()
    pegawai_list = Pegawai.query.all()
    info_list = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).limit(3).all()
    
    notif_pangkat = []
    notif_pensiun = []
    user_data = None

    if role == 'admin':
        for p in pegawai_list:
            if p.jenis_pegawai == 'PNS' and p.tmt_pangkat:
                # Logika notifikasi naik pangkat (kira-kira 4 tahun / 1370 hari)
                if (today - p.tmt_pangkat).days >= 1370: notif_pangkat.append(p.nama)
            # Logika pensiun (usia 58 tahun / 21170 hari)
            if p.tgl_lahir and (today - p.tgl_lahir).days >= 21170:
                notif_pensiun.append(p.nama)
    else:
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()

    return render_template('index.html', role=role, user_data=user_data, 
                           pegawai=pegawai_list, today=today,
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun,
                           info_terkini=info_list)

# --- FITUR LOKER DIGITAL (KHUSUS PLKB) ---
@app.route('/berkas_saya')
def berkas_saya():
    if session.get('user_role') != 'plkb': return redirect(url_for('dashboard'))
    
    user_nip = session['user_nip']
    user_data = Pegawai.query.filter_by(nip=user_nip).first()
    
    # Buat folder khusus per NIP
    path_user = os.path.join(app.config['LOKER_PLKB'], user_nip)
    os.makedirs(path_user, exist_ok=True)
    
    # Ambil list berkas yang sudah ada
    files = os.listdir(path_user)
    
    return render_template('berkas_plkb.html', role='plkb', user_data=user_data, files=files)

@app.route('/upload_dokumen', methods=['POST'])
def upload_dokumen():
    if session.get('user_role') == 'plkb':
        user_nip = session['user_nip']
        file = request.files.get('file_berkas') # Sinkron dengan name="file_berkas" di HTML
        kategori = request.form.get('kategori')
        
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            # Nama file format: Kategori_NIP_Timestamp.ext
            filename = f"{kategori}_{user_nip}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            
            path_user = os.path.join(app.config['LOKER_PLKB'], user_nip)
            file.save(os.path.join(path_user, filename))
            flash(f"Berkas {kategori} berhasil disimpan ke server!", "success")
        else:
            flash("Gagal! Format file tidak didukung.", "danger")
            
    return redirect(url_for('berkas_saya'))

# --- KOMUNIKASI & CHAT INFO ---
@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    info_list = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    
    if role == 'plkb':
        user = Pegawai.query.filter_by(nip=session['user_nip']).first()
        if user:
            for info in info_list:
                sudah_baca = LogBaca.query.filter_by(pengumuman_id=info.id, nip_pembaca=user.nip).first()
                if not sudah_baca:
                    baru = LogBaca(pengumuman_id=info.id, nip_pembaca=user.nip, nama_pembaca=user.nama)
                    db.session.add(baru)
            db.session.commit()

    read_data = {}
    if role == 'admin':
        for info in info_list:
            read_data[info.id] = LogBaca.query.filter_by(pengumuman_id=info.id).all()

    user_data = None
    if role == 'plkb':
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
        
    return render_template('chat_info.html', role=role, user_data=user_data, info_terkini=info_list, read_data=read_data, today=date.today())

@app.route('/kirim_pengumuman', methods=['POST'])
def kirim_pengumuman():
    if session.get('user_role') == 'admin':
        pesan = request.form.get('isi_pengumuman')
        file = request.files.get('lampiran')
        filename = None
        if file and allowed_file(file.filename):
            orig_filename = secure_filename(file.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{orig_filename}"
            file.save(os.path.join(app.config['CHAT_UPLOAD'], filename))

        if pesan:
            baru = Pengumuman(isi=pesan, file_lampiran=filename)
            db.session.add(baru)
            db.session.commit()
            flash("Informasi Berhasil Disiarkan!", "success")
    return redirect(url_for('chat_info'))

@app.route('/hapus_pengumuman/<int:id>')
def hapus_pengumuman(id):
    if session.get('user_role') == 'admin':
        info = Pengumuman.query.get(id)
        if info:
            if info.file_lampiran:
                file_path = os.path.join(app.config['CHAT_UPLOAD'], info.file_lampiran)
                if os.path.exists(file_path): os.remove(file_path)
            db.session.delete(info)
            db.session.commit()
            flash("Informasi berhasil dihapus!", "warning")
    return redirect(url_for('chat_info'))

# --- MANAJEMEN DATA PEGAWAI (ADMIN ONLY) ---
@app.route('/data_pegawai')
def data_pegawai():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    pegawai_list = Pegawai.query.all()
    user_data = None
    if role == 'plkb':
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
        
    return render_template('data_pegawai.html', role=role, pegawai=pegawai_list, 
                           user_data=user_data, today=date.today())

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
        flash(f"Data {baru.nama} Berhasil Disimpan!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Gagal Simpan: {str(e)}", "danger")
    return redirect(url_for('data_pegawai'))

@app.route('/hapus_pegawai/<int:id>')
def hapus_pegawai(id):
    if 'user_role' in session and session['user_role'] == 'admin':
        p = Pegawai.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
            flash("Pegawai Berhasil Dihapus!", "warning")
    return redirect(url_for('data_pegawai'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# --- INISIALISASI DATABASE ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Gunakan debug=True selama masa pengembangan
    app.run(debug=True)
