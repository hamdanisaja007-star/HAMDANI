from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- KONFIGURASI DATABASE & FOLDER (KHUSUS VERCEL) ---
# Database ditaruh di /tmp agar bisa ditulis (Writeable) di server Vercel
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/tmp', 'kepegawaian.db')
app.config['UPLOAD_FOLDER'] = os.path.join('/tmp', 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Daftar Kategori Dokumen
KATEGORI_UTAMA = ['Berkas_Umum', 'Kenaikan_Pangkat', 'Kenaikan_Jabatan', 'Pensiun', 'Perpanjangan_Kontrak', 'Kenaikan_Golongan']

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

# --- FUNGSI OTOMATISASI FOLDER ---
def buat_folder_pegawai(pegawai_obj):
    folder_aman = pegawai_obj.nama.replace(" ", "_")
    status = pegawai_obj.jenis_pegawai 
    kategori_wajib = ['Berkas_Umum']
    if status == 'PNS':
        kategori_spesifik = ['Kenaikan_Pangkat', 'Kenaikan_Jabatan', 'Pensiun']
    else:
        kategori_spesifik = ['Perpanjangan_Kontrak', 'Kenaikan_Golongan']
    
    daftar_folder = kategori_wajib + kategori_spesifik
    for kat in daftar_folder:
        path = os.path.join(app.config['UPLOAD_FOLDER'], status, folder_aman, kat)
        if not os.path.exists(path):
            os.makedirs(path)

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
    soal_list = BankSoal.query.all()
    pesan_list = Pesan.query.order_by(Pesan.tanggal.desc()).all()
    
    berkas_masuk, berkas_saya, notif_pangkat, notif_pensiun = [], [], [], []
    user_data = None

    if role == 'admin':
        for status_dir in ['PNS', 'PPPK']:
            status_path = os.path.join(app.config['UPLOAD_FOLDER'], status_dir)
            if os.path.exists(status_path):
                for nama_p_folder in os.listdir(status_path):
                    p_path = os.path.join(status_path, nama_p_folder)
                    if os.path.isdir(p_path):
                        for kat_folder in os.listdir(p_path):
                            kat_path = os.path.join(p_path, kat_folder)
                            if os.path.isdir(kat_path):
                                for file in os.listdir(kat_path):
                                    berkas_masuk.append({
                                        'nama_file': file, 'kategori': kat_folder, 
                                        'pemilik': nama_p_folder.replace("_", " "), 'status': status_dir
                                    })
        for p in pegawai_list:
            if p.jenis_pegawai == 'PNS':
                if p.tmt_pangkat and (today - p.tmt_pangkat).days >= 1370: notif_pangkat.append(p.nama)
                if p.tgl_lahir and (today - p.tgl_lahir).days >= 20805: notif_pensiun.append(p.nama)
    else:
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
        if user_data:
            folder_p = user_data.nama.replace(" ", "_")
            base_p = os.path.join(app.config['UPLOAD_FOLDER'], user_data.jenis_pegawai, folder_p)
            if os.path.exists(base_p):
                for kat in os.listdir(base_p):
                    kat_path = os.path.join(base_p, kat)
                    if os.path.isdir(kat_path):
                        for f in os.listdir(kat_path):
                            berkas_saya.append({'nama_file': f, 'kategori': kat})

    return render_template('index.html', role=role, user_data=user_data, 
                           soal=soal_list, pegawai=pegawai_list, today=today,
                           berkas=berkas_masuk, berkas_saya=berkas_saya,
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
        buat_folder_pegawai(baru)
        flash(f"Data {baru.nama} Berhasil Disimpan!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Gagal Simpan: {str(e)}", "danger")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# --- BOOTSTRAP DATABASE ---
if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        db.create_all()
    app.run()
