import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'rahasia_dhede_bimz_123'

# --- KONFIGURASI DATABASE KHUSUS VERCEL ---
# Vercel hanya mengizinkan penulisan file di folder /tmp/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODEL DATABASE ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jenis_pegawai = db.Column(db.String(10))  # PNS / PPPK
    jabatan = db.Column(db.String(100))
    kecamatan = db.Column(db.String(50))

# Buat tabel otomatis saat aplikasi jalan
with app.app_context():
    db.create_all()

# --- ROUTES / JALUR APLIKASI ---

@app.route('/')
def home():
    if 'user' in session:
        # Ambil semua data pegawai untuk ditampilkan di dashboard
        semua_pegawai = Pegawai.query.all()
        return render_template('index.html', 
                               pegawai=semua_pegawai, 
                               role=session.get('role'), 
                               today=datetime.now())
    return render_template('login.html')

@app.route('/login', methods=['POST']) # Pastikan pakai 'methods' (pakai S)
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Logic Login Sederhana
    if username == 'admin' and password == 'admin123':
        session['user'] = username
        session['role'] = 'admin'
        flash('Selamat Datang Admin!', 'success')
        return redirect(url_for('home'))
    elif username and len(username) >= 4: # Login sebagai user umum
        session['user'] = username
        session['role'] = 'user'
        return redirect(url_for('home'))
    else:
        flash('Login Gagal! Periksa kembali Username/Password.', 'danger')
        return redirect(url_for('home'))

@app.route('/tambah_pegawai', methods=['POST'])
def tambah_pegawai():
    if session.get('role') == 'admin':
        try:
            new_p = Pegawai(
                nip=request.form.get('nip'),
                nama=request.form.get('nama'),
                jenis_pegawai=request.form.get('jenis_pegawai'),
                jabatan=request.form.get('jabatan'),
                kecamatan=request.form.get('kecamatan')
            )
            db.session.add(new_p)
            db.session.commit()
            flash('Data Pegawai Berhasil Disimpan!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Gagal simpan data: {str(e)}', 'danger')
    return redirect(url_for('home'))

@app.route('/hapus_pegawai/<int:id>')
def hapus_pegawai(id):
    if session.get('role') == 'admin':
        p = Pegawai.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
            flash('Data Berhasil Dihapus!', 'info')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar sistem.', 'info')
    return redirect(url_for('home'))

# Fitur Export (Dibuat dummy dulu agar tidak crash karena Pandas/Numpy)
@app.route('/export_excel')
def export_excel():
    flash('Fitur Export Excel sedang dimaintenance untuk Vercel.', 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
