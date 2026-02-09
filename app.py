from flask import Flask, render_template, request, jsonify
import os

# Mencari alamat folder tempat app.py berada secara otomatis
base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=base_dir)

@app.route('/')
def login_page():
    # Flask akan mencari login.html di folder utama (base_dir)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    # Flask akan mencari index.html di folder utama (base_dir)
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
