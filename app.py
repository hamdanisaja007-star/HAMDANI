import os
import pandas as pd
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- KONFIGURASI DATABASE & FOLDER ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['CHAT_UPLOAD'] = '/tmp/chat_files'
app.config['BERKAS_PEGAWAI'] = '/tmp/berkas_pegawai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['CHAT_UPLOAD'], exist_ok=True)
os.makedirs(app.config['BERKAS_PEGAWAI'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# --- MODELS (Data Tetap Sama) ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100))
    jenis_pegawai = db.Column(db.String(10), default='PNS') 
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

# --- DASHBOARD (RESTORASI TOTAL) ---
@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    today = date.today()
    info_list = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).limit(3).all()
    
    # Inisialisasi variabel agar tidak error di template
    pegawai_list = []
    notif_pangkat, notif_pensiun = [], []
    user_data = None

    if role == 'admin':
        # ADMIN: Menampilkan SEMUA Data Pegawai
        pegawai_list = Pegawai.query.all()
        for p in pegawai_list:
            if p.jenis_pegawai == 'PNS' and p.tmt_pangkat:
                if (today - p.tmt_pangkat).days >= 1370: notif_pangkat.append(p.nama)
            if p.tgl_lahir and (today - p.tgl_lahir).days >= 20805:
                notif_pensiun.append(p.nama)
    else:
        # PLKB: Menampilkan PROFIL PRIBADI
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()

    return render_template('index.html', 
                           role=role, 
                           user_data=user_data, 
                           pegawai=pegawai_list, # Ini yang bikin tabel muncul di Admin
                           today=today,
                           notif_pangkat=notif_pangkat, 
                           notif_pensiun=notif_pensiun,
                           info_terkini=info_list)

# --- FITUR LOKER (HANYA UNTUK PLKB) ---
@app.route('/berkas_saya')
def berkas_saya():
    if session.get('user_role') != 'plkb': 
        flash("Akses khusus PLKB!", "danger")
        return redirect(url_for('dashboard'))
        
    user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
    folder_user = os.path.join(app.config['BERKAS_PEGAWAI'], session['user_nip'])
    os.makedirs(folder_user, exist_ok=True)
    files = os.listdir(folder_user)
    info_list = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).limit(3).all()
    
    return render_template('berkas_plkb.html', role='plkb', user_data=user_data, files=files, info_terkini=info_list)

@app.route('/upload_dokumen', methods=['POST'])
def upload_dokumen():
    if session.get('user_role') == 'plkb':
        kategori, file = request.form.get('kategori'), request.files.get('file_berkas')
        if file and allowed_file(file.filename):
            user_nip = session['user_nip']
            folder_user = os.path.join(app.config['BERKAS_PEGAWAI'], user_nip)
            os.makedirs(folder_user, exist_ok=True)
            filename = f"{kategori.replace(' ', '_')}_{user_nip}_{secure_filename(file.filename)}"
            file.save(os.path.join(folder_user, filename))
            flash(f"Berkas {kategori} Berhasil Diupload!", "success")
    return redirect(url_for('berkas_saya'))

# --- KOMUNIKASI ---
@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    info_list = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    user_data = Pegawai.query.filter_by(nip=session.get('user_nip')).first() if role == 'plkb' else None
    
    read_data = {info.id: LogBaca.query.filter_by(pengumuman_id=info.id).all() for info in info_list} if role == 'admin' else {}
    return render_template('chat_info.html', role=role, user_data=user_data, info_terkini=info_list, read_data=read_data, today=date.today())

# --- MANAJEMEN PEGAWAI (ADMIN ONLY) ---
@app.route('/tambah_pegawai', methods=['POST'])
def tambah_pegawai():
    if session.get('user_role') == 'admin':
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
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
