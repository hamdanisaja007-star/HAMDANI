from flask import Flask, render_template, jsonify
import json
import os

# PENTING: ../templates artinya naik satu tingkat keluar dari folder api
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def dashboard():
    # Menampilkan Dashboard Utama SIKEPAL ULTRA
    return render_template('index.html')

@app.route('/pelayanan-kb')
def pelayanan_kb():
    # Menampilkan Modul Pelayanan KB yang Mas buat tadi
    return render_template('pelayanan_kb.html')

@app.route('/api/iklan')
def get_iklan():
    # Mengambil data iklan dari root folder
    path_iklan = os.path.join(os.path.dirname(__file__), '../iklan.json')
    if os.path.exists(path_iklan):
        with open(path_iklan, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify([])

# Supaya Vercel bisa mengenali app ini
app.debug = True
