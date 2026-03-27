from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

# Dummy data agar Dashboard tidak kosong (Sesuaikan dengan kolom di index.html bos)
dummy_pegawai = [
    {
        "id": 1, 
        "nip": "19820406001", 
        "nama": "HAMDANI", 
        "jabatan": "PLKB", 
        "jenis_pegawai": "PNS", 
        "pangkat_gol": "III/a",
        "kecamatan": "Pabuaran"
    }
]

@app.route('/')
def landing():
    if 'user_role' in session: # Sesuaikan nama session dengan login.html
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pw = request.form.get('password')

    if user == "admin" and pw == "admin123":
        session['user_role'] = 'admin'
        return redirect(url_for('dashboard'))
    
    # Login pakai NIP dummy
    if user == "19820406001":
        session['user_role'] = 'plkb'
        session['user_nip'] = user
        return redirect(url_for('dashboard'))

    flash("Login gagal! Periksa NIP/Password", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session:
        return redirect(url_for('landing'))
    
    role = session.get('user_role')
    
    # Kirim SEMUA variabel yang dipanggil di index.html bos agar tidak error Jinja2
    return render_template('index.html', 
                           pegawai=dummy_pegawai, 
                           role=role, 
                           today=date.today(),
                           berkas=[], 
                           berkas_saya=[],
                           notif_pangkat=[], 
                           notif_pensiun=[],
                           pesan_masuk=[],
                           soal=[],
                           user_data=dummy_pegawai[0])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

# KHUSUS VERCEL: Tidak perlu app.run di dalam if __name__
