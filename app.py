from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "dhede_bimz_final_full_2026_secure"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'kepegawaian.db')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)

# ================= ROUTES =================

@app.route('/')
def landing():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pw = request.form.get('password')

    if user == "admin" and pw == "admin123":
        session['role'] = 'admin'
        return redirect('/dashboard')

    flash("Login gagal")
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect('/')
    
    data = Pegawai.query.all()
    return render_template('index.html', pegawai=data)

@app.route('/tambah', methods=['POST'])
def tambah():
    p = Pegawai(
        nip=request.form.get('nip'),
        nama=request.form.get('nama')
    )
    db.session.add(p)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/hapus/<int:id>')
def hapus(id):
    p = Pegawai.query.get(id)
    if p:
        db.session.delete(p)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= RUN =================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
