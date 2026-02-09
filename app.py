from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Data desa (Pastikan tidak ada salah ketik di sini)
DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/')
def home():
    try:
        return render_template('login.html')
    except Exception as e:
        return f"Error: File login.html tidak ditemukan di folder templates. {str(e)}"

@app.route('/dashboard')
def dashboard():
    try:
        # Kita kirim desa=DESA_DATA supaya index.html tidak error saat mencari data desa
        return render_template('index.html', desa=DESA_DATA)
    except Exception as e:
        return f"Error di Dashboard: {str(e)}"

@app.route('/handler', methods=['POST'])
def handler():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data"}), 400
        
        target = data.get('target', '')
        mode = data.get('mode', '')

        if mode == 'web':
            url = target if target.startswith('http') else f"https://{target}"
            return jsonify({"status": "redirect", "url": url})
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Standar Vercel
if __name__ == '__main__':
    app.run()
