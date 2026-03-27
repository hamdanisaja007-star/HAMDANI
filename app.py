from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# DATA DUMMY (Agar Dashboard Bos tidak kosong saat demo)
DUMMY_PEGAWAI = [
    {"nip": "19820406001", "nama": "HAMDANI", "jabatan": "PLKB", "jenis_pegawai": "PNS", "pangkat_gol": "III/a", "kecamatan": "Pabuaran"}
]

@app.route('/')
def landing():
    if 'user_role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    user_in = request.form.get('username')
    pass_in = request.form.get('password')
    
    # Login Admin (Sesuai kode bos)
    if user_in == "admin" and pass_in == "admin123":
        session['user_role'] = 'admin'
        return redirect(url_for('dashboard'))
    
    # Login NIP (Sesuai kode bos)
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
    
    # Mengirimkan variabel yang dibutuhkan INDEX.HTML agar tampilan tidak pecah
    return render_template('index.html', 
                           role=role, 
                           pegawai=DUMMY_PEGAWAI, 
                           today=date.today(),
                           berkas=[], 
                           berkas_saya=[],
                           notif_pangkat=[], 
                           notif_pensiun=[],
                           pesan_masuk=[],
                           soal=[],
                           user_data=DUMMY_PEGAWAI[0])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
