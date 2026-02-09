from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data simulasi desa
DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/')
def index():
    return render_template('login.html')

# Kita buat rute ini bisa menerima GET karena JavaScript Bapak pakai window.location.href
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', desa=DESA_DATA)

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

if __name__ == '__main__':
    app.run()
