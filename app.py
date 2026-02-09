from flask import Flask, render_template, request, jsonify
import os

# KUNCI: Kita paksa Flask mencari template di folder utama ('.'), bukan di folder 'templates'
app = Flask(__name__, template_folder='.')

DESA_DATA = {
    "Bojongraharja": {"user": "opbojongraharja.0210", "pass": "Cikembar@0210"},
    "Cimanggu": {"user": "opcimanggu.0210", "pass": "Cikembar@0210"},
    "Cikembar": {"user": "opcikembar.0210", "pass": "Cikembar@0210"}
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def command_center():
    # Ini akan memanggil index.html yang ada di folder utama Bapak
    return render_template('index.html', desa=DESA_DATA)

@app.route('/handler', methods=['POST'])
def handler():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error"}), 400
    
    target = data.get('target')
    mode = data.get('mode')

    if mode == 'web':
        url = target if target.startswith('http') else f"https://{target}"
        return jsonify({"status": "redirect", "url": url})
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
