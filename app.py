import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'rahasia_dhede_bimz'

# KONFIGURASI DATABASE KHUSUS VERCEL (Wajib ke /tmp/)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/kepegawaian.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODEL DATABASE
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jenis_pegawai = db.Column(db.String(10))  # PNS atau PPPK
    jabatan = db.Column(db.String(100))
    kecamatan = db.Column(db.String(50))

# Buat Database di awal
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user' in session:
        pegawai_list = Pegawai.query.all()
        return render_template('index.html', pegawai=pegawai_list, role=session['role'], today=datetime.now())
    return render_template('login.html')

@app.route('/login', method=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple Logic Login
    if username == 'admin' and password == 'admin123':
        session['user'] = username
        session['role'] = 'admin'
        return redirect(url_for('home'))
    elif username.isdigit(): # Anggap kalau input angka itu NIP Pegawai
        session['user'] = username
        session['role'] = 'user'
        return redirect(url_for('home'))
    else:
        flash('Username atau Password Salah!', 'danger')
        return redirect(url_for('home'))

@app.route('/tambah_pegawai', methods=['POST'])
def tambah_pegawai():
    if 'role' in session and session['role'] == 'admin':
        new_p = Pegawai(
            nip=request.form.get('nip'),
            nama=request.form.get('nama'),
            jenis_pegawai=request.form.get('jenis_pegawai'),
            jabatan=request.form.get('jabatan'),
            kecamatan=request.form.get('kecamatan')
        )
        db.session.add(new_p)
        db.session.commit()
        flash('Data Berhasil Ditambahkan!', 'success')
    return redirect(url_for('home'))

@app.route('/hapus_pegawai/<int:id>')
def hapus_pegawai(id):
    if 'role' in session and session['role'] == 'admin':
        p = Pegawai.query.get(id)
        db.session.delete(p)
        db.session.commit()
        flash('Data Berhasil Dihapus!', 'info')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Bagian Export Excel dimatikan dulu agar tidak error numpy
@app.route('/export_excel')
def export_excel():
    flash('Fitur Export sedang dalam perbaikan sistem (Library Incompatibility)', 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
