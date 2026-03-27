from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# --- LOGIN DUMMY AGAR DESAIN TETAP JALAN ---
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
    
    # Login User (NIP)
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
    
    # Data ini dikirim agar INDEX.HTML tampil sempurna seperti desain asli bos
    pegawai_list = [
        {"nip": "19820406001", "nama": "HAMDANI", "jabatan": "PLKB", "jenis_pegawai": "PNS", "pangkat_gol": "III/a"}
    ]
    
    return render_template('index.html', 
                           role=role, 
                           pegawai=pegawai_list, 
                           today=date.today(),
                           berkas=[], 
                           berkas_saya=[],
                           notif_pangkat=[], 
                           notif_pensiun=[],
                           pesan_masuk=[],
                           soal=[]) # Tambahkan variabel lain jika di index.html ada pemanggilan 'soal'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))
