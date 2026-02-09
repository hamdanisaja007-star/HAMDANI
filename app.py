from flask import Flask, render_template, request, jsonify

# Kita arahkan Flask untuk mencari file Bapak di folder utama
app = Flask(__name__, template_folder='.')

@app.route('/')
def login_page():
    # Ini akan membuka file login.html milik Bapak
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    # Ini akan membuka file index.html (Command Center) milik Bapak
    return render_template('index.html')

@app.route('/pelayanan_kb')
def pelayanan_kb():
    # Ini akan membuka file pelayanan_kb.html milik Bapak
    return render_template('pelayanan_kb.html')

@app.route('/handler', methods=['POST'])
def handler():
    # Ini supaya tombol-tombol di web Bapak bisa diklik tanpa error
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
