from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data desa untuk dashboard
DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/')
def home():
    # INI HALAMAN PERTAMA: Munculkan Login
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # INI HALAMAN KEDUA: Munculkan Command Center (index.html)
    # Kita kirim data DESA_DATA supaya bisa dibaca di dashboard
    return render_template('index.html', desa=DESA_DATA)

@app.route('/handler', methods=['POST'])
def handler():
    # Fungsi ini untuk menjalankan tombol-tombol di Dashboard
    data = request.get_json()
    if not data:
        return jsonify({"status": "error"}), 400
    
    target = data.get('target')
    mode = data.get('mode')

    if mode == 'web':
        url = target if target.startswith('http') else f"https://{target}"
        return jsonify({"status": "redirect", "url": url})
    
    return jsonify({"status": "success", "message": "Module Executed"})

if __name__ == '__main__':
    app.run()
