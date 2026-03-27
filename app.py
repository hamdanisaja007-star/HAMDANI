from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- KONFIGURASI DATABASE VERCEL SAFE ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Di Vercel, folder /tmp adalah satu-satunya tempat yang bisa ditulis
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/tmp', 'kepegawaian.db')
app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS (Sesuai Kode Bos) ---
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

class BankSoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)

class Pesan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_pengirim = db.Column(db.String(100))
    nip_pengirim = db.Column(db.String(20))
    isi_pesan = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.now)

# Data Cadangan agar Desain tidak Kosong saat Demo
DUMMY_PEGAWAI = [
    {"nip": "19820406001", "nama": "HAMDANI", "jabatan": "PLKB", "jenis_pegawai": "PNS", "pangkat_gol": "III/a", "kecamatan": "Pabuaran"}
]

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
    
    # Cek Database
    try:
        user_plkb = Pegawai.query.filter_by(nip=user_in).first()
        if user_plkb:
            session['user_role'] = 'plkb'
            session['user_nip'] = user_in
            return redirect(url_for('dashboard'))
    except:
        # Fallback untuk NIP Admin jika DB belum siap
        if user_in == "19820406001":
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
    
    try:
        pegawai_list = Pegawai.query.all()
        if not pegawai_list: pegawai_list = DUMMY_PEGAWAI
        soal_list = BankSoal.query.all()
        pesan_list = Pesan.query.order_by(Pesan.tanggal.desc()).all()
    except:
        pegawai_list = DUMMY_PEGAWAI
        soal_list, pesan_list = [], []

    # Inisialisasi variabel agar template tidak error
    berkas_masuk, berkas_saya, notif_pangkat, notif_pensiun = [], [], [], []
    user_data = None

    if role != 'admin':
        user_data = next((p for p in pegawai_list if p['nip'] == session.get('user_nip')), DUMMY_PEGAWAI[0])

    return render_template('index.html', role=role, user_data=user_data, 
                           soal=soal_list, pegawai=pegawai_list, today=today,
                           berkas=berkas_masuk, berkas_saya=berkas_saya,
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun,
                           pesan_masuk=pesan_list)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
