from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Data simulasi sesuai script Bapak
DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    user = request.form.get('username')
    pw = request.form.get('password')
    
    # Bypass simpel untuk demo: Username 'BIMZ2026'
    if user == "BIMZ2026":
        return render_template('dashboard.html', desa=DESA_DATA)
    else:
        return "<h1>LOGIN GAGAL! Periksa kode akses Anda.</h1>"

@app.route('/start_robot', methods=['POST'])
def start_robot():
    desa = request.json.get('desa')
    kb_type = request.json.get('kb_type')
    # Di sini nanti logika Playwright Bapak bekerja
    # Untuk demo, kita kirim respon balik sukses simulasi
    return jsonify({
        "status": "success",
        "message": f"Robot SIKEPAL berhasil sinkronisasi data {kb_type} untuk Desa {desa} ke SIGA!"
    })

if __name__ == '__main__':
    app.run(debug=True)