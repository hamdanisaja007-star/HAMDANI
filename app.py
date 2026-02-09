from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Data simulasi sesuai script Bapak
DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        # Bypass simpel untuk demo: Username 'BIMZ2026'
        if user == "BIMZ2026":
            return render_template('dashboard.html', desa=DESA_DATA)
        else:
            return "<h1>LOGIN GAGAL! Periksa kode akses Anda.</h1><br><a href='/'>Kembali ke Login</a>"
    
    # Jika ada yang coba akses /dashboard langsung tanpa login (GET)
    return render_template('login.html')

@app.route('/start_robot', methods=['POST'])
def start_robot():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    desa = data.get('desa')
    kb_type = data.get('kb_type')
    
    return jsonify({
        "status": "success",
        "message": f"Robot SIKEPAL berhasil sinkronisasi data {kb_type} untuk Desa {desa} ke SIGA!"
    })

# Bagian ini sangat penting untuk Vercel
if __name__ == '__main__':
    app.run()
