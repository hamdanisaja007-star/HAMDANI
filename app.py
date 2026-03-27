from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "dhede_bimz_final_full_2026_secure"

# Dummy data Pegawai
dummy_pegawai = [
    {"id": 1, "nip": "123456", "nama": "Budi"},
    {"id": 2, "nip": "654321", "nama": "Ani"}
]

# ================= ROUTES =================

@app.route('/')
def landing():
    if 'role' in session:
        return redirect('/dashboard')
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
    
    # pakai dummy data
    return render_template('index.html', pegawai=dummy_pegawai)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
