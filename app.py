from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def debug_check():
    # Ini akan mengecek apakah folder templates dan isinya benar-benar ada
    if not os.path.exists('templates'):
        return "ERROR: Folder 'templates' (huruf kecil semua) tidak ditemukan!"
    
    files = os.listdir('templates')
    
    # Cek file login.html
    if 'login.html' in files:
        return render_template('login.html')
    else:
        return f"ERROR: File 'login.html' tidak ada di folder templates. Yang ada cuma: {files}"

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
