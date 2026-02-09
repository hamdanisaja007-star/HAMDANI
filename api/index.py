from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>SIKEPAL ONLINE</h1><p>Vercel sudah AKTIF! Kabari saya kalau sudah muncul tulisan ini Mas!</p>"

@app.route('/handler', methods=['POST'])
def handler():
    data = request.json
    URL_LAPTOP = "https://plastered-nonsubtly-tamera.ngrok-free.dev/jalankan-robot"
    try:
        response = requests.post(URL_LAPTOP, json=data, timeout=5)
        return jsonify({"status": "Sinyal Terkirim!"})
    except:
        return jsonify({"status": "Laptop Offline"})

# PENTING: Jangan pakai app.run() di Vercel
# Cukup biarkan seperti ini agar Vercel yang menjalankan
