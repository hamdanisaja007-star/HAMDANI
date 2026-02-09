from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>SIKEPAL ONLINE</h1><p>Kalau muncul tulisan ini, berarti Vercel sudah SEMBUH. Kabari saya Mas!</p>"

@app.route('/handler', methods=['POST'])
def handler():
    data = request.json
    # Link Ngrok Mas Hamdani
    URL_LAPTOP = "https://plastered-nonsubtly-tamera.ngrok-free.dev/jalankan-robot"
    try:
        response = requests.post(URL_LAPTOP, json=data, timeout=5)
        return jsonify({"status": "Sinyal Terkirim!", "detail": response.json()})
    except:
        return jsonify({"status": "Laptop Offline"})

if __name__ == "__main__":
    app.run()
