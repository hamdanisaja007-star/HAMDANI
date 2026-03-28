import os
import pandas as pd
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sidallap_sukabumi_2026_secure"

# --- KONFIGURASI (Vercel & Local) ---
BASE_TMP = "/tmp"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_TMP, "sidalap.db")}'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_TMP, 'loker_berkas')
app.config['CHAT_UPLOAD'] = os.path.join(BASE_TMP, 'chat_files')
app.config['PROFIL_UPLOAD'] = os.path.join(BASE_TMP, 'foto_profil')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pastikan semua folder siap
for folder in [app.config['UPLOAD_FOLDER'], app.config['CHAT_UPLOAD'], app.config['PROFIL_UPLOAD']]:
    os.makedirs(folder, exist_ok=True)

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
    jenis_pegawai = db.Column(db.String(10)) # PNS / PPPK
    pangkat_gol = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    desa_binaan = db.Column(db.String(200))
    no_hp = db.Column(db.String(20))
    tmt_pangkat = db.Column(db.Date)
    tgl_lahir = db.Column(db.Date)
    foto = db.Column(db.String(200), default='default_user.png')

class Pengumuman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    file_lampiran = db.Column(db.String(200))
    tanggal = db.Column(db.DateTime, default=datetime.now)
    logs = db.relationship('LogBaca', backref='pengumuman', cascade="all, delete-orphan")

class LogBaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengumuman_id = db.Column(db.Integer, db.ForeignKey('pengumuman.id'))
    nip_pembaca = db.Column(db.String(20))
    nama_pembaca = db.Column(db.String(100))
    waktu_baca = db.Column(db.DateTime, default=datetime.now)

# --- MIDDLEWARE LOGIN CHECK ---
@app.context_processor
def inject_user():
    user_data = None
    if 'user_nip' in session:
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
    return dict(user_now=user_data)

# --- ROUTES ---
@app.route('/')
def landing():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    u, p = request.form.get('username'), request.form.get('password')
    if u == "admin" and p == "admin123":
        session['user_role'] = 'admin'
        return redirect(url_for('dashboard'))
    user = Pegawai.query.filter_by(nip=u).first()
    if user:
        session['user_role'], session['user_nip'] = 'plkb', u
        return redirect(url_for('profil'))
    flash("Login Gagal!", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    pegawai = Pegawai.query.all()
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).limit(5).all()
    return render_template('dashboard.html', pegawai=pegawai, info=info)

# --- SIDEBAR PLKB 1: PROFIL ---
@app.route('/profil')
def profil():
    if session.get('user_role') != 'plkb': return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session['user_nip']).first()
    return render_template('profil.html', user=user)

# --- SIDEBAR PLKB 2: UPLOAD BERKAS ---
@app.route('/berkas_saya')
def berkas_saya():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session['user_nip']).first()
    path_user = os.path.join(app.config['UPLOAD_FOLDER'], user.nip)
    os.makedirs(path_user, exist_ok=True)
    files = os.listdir(path_user)
    return render_template('upload_plkb.html', user=user, files=files)

@app.route('/simpan_berkas', methods=['POST'])
def simpan_berkas():
    user_nip = session.get('user_nip')
    file = request.files.get('file_berkas')
    kat = request.form.get('kategori')
    if file and user_nip:
        fname = f"{kat}_{datetime.now().strftime('%Y%m%d%H%M')}_{secure_filename(file.filename)}"
        target = os.path.join(app.config['UPLOAD_FOLDER'], user_nip)
        os.makedirs(target, exist_ok=True)
        file.save(os.path.join(target, fname))
        flash("Berkas Berhasil Terkirim ke Admin!", "success")
    return redirect(url_for('berkas_saya'))

# --- SIDEBAR ADMIN 4: BERKAS MASUK ---
@app.route('/admin/berkas_masuk')
def berkas_masuk():
    if session.get('user_role') != 'admin': return redirect(url_for('dashboard'))
    list_masuk = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for nip in os.listdir(app.config['UPLOAD_FOLDER']):
            p = Pegawai.query.filter_by(nip=nip).first()
            p_path = os.path.join(app.config['UPLOAD_FOLDER'], nip)
            for f in os.listdir(p_path):
                list_masuk.append({'nama': p.nama if p else nip, 'nip': nip, 'file': f, 'kat': f.split('_')[0]})
    return render_template('admin_berkas.html', data=list_masuk)

# --- SIDEBAR 3: CHAT / INFO ---
@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    if role == 'plkb':
        user = Pegawai.query.filter_by(nip=session['user_nip']).first()
        for i in info:
            if not LogBaca.query.filter_by(pengumuman_id=i.id, nip_pembaca=user.nip).first():
                db.session.add(LogBaca(pengumuman_id=i.id, nip_pembaca=user.nip, nama_pembaca=user.nama))
        db.session.commit()
    
    logs = {i.id: LogBaca.query.filter_by(pengumuman_id=i.id).all() for i in info} if role == 'admin' else {}
    return render_template('chat_info.html', info=info, logs=logs, role=role)

@app.route('/kirim_info', methods=['POST'])
def kirim_info():
    pesan = request.form.get('isi')
    file = request.files.get('lampiran')
    fname = None
    if file:
        fname = secure_filename(file.filename)
        file.save(os.path.join(app.config['CHAT_UPLOAD'], fname))
    db.session.add(Pengumuman(isi=pesan, file_lampiran=fname))
    db.session.commit()
    return redirect(url_for('chat_info'))

# --- EXTRAS ---
@app.route('/download/<nip>/<filename>')
def download_file(nip, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], nip), filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
