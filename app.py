import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sidalap_ippkb_sukabumi_2026"

# DATABASE (Sementara pakai /tmp/ agar Vercel tidak error saat testing)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sidalap_v1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODEL DATA (Identitas PLKB) ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100))
    jenis_pegawai = db.Column(db.String(10)) # PNS / PPPK
    pangkat_gol = db.Column(db.String(50))
    tmt_pangkat = db.Column(db.Date) # Tanggal terakhir naik pangkat
    tgl_lahir = db.Column(db.Date)   # Untuk hitung pensiun

# --- LOGIKA DASHBOARD ---
@app.route('/')
def index():
    if 'role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html') # Pastikan Bos punya file login.html

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple Logic: Admin Kabupaten
    if username == "admin" and password == "admin123":
        session['role'] = 'admin'
        return redirect(url_for('dashboard'))
    
    # Login PLKB via NIP
    user = Pegawai.query.filter_by(nip=username).first()
    if user:
        session['role'] = 'plkb'
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
        
    flash("NIP atau Password salah, Bos!", "danger")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'role' not in session: return redirect(url_for('index'))
    
    today = date.today()
    if session['role'] == 'admin':
        # TAMPILAN KABUPATEN
        semua_pegawai = Pegawai.query.all()
        return render_template('admin.html', pegawai=semua_pegawai, total=len(semua_pegawai))
    else:
        # TAMPILAN PERSONAL PLKB
        p = Pegawai.query.get(session['user_id'])
        # Hitung sisa waktu (Contoh: naik pangkat tiap 4 tahun)
        days_since_pangkat = (today - p.tmt_pangkat).days
        sisa_hari = 1460 - days_since_pangkat
        return render_template('plkb.html', u=p, sisa=sisa_hari)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- ISI DATA AWAL (Buat Tes Besok Pagi) ---
with app.app_context():
    db.create_all()
    if not Pegawai.query.filter_by(nip="19820406001").first():
        db.session.add(Pegawai(
            nip="19820406001", 
            nama="Dhede Bimz", 
            jabatan="PLKB Ahli Muda", 
            jenis_pegawai="PNS", 
            pangkat_gol="III/c", 
            tmt_pangkat=date(2022, 1, 1), 
            tgl_lahir=date(1982, 4, 6)
        ))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
