from flask import Flask, render_template, request, jsonify
import os

# Paksa Flask mencari file HTML di folder yang sama dengan app.py
app = Flask(__name__, template_folder='.')

@app.route('/')
def login_page():
    # Pastikan file Bapak namanya persis: login.html
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    # Pastikan file Bapak namanya persis: index.html
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

# Ini penting untuk Vercel agar tidak crash
if __name__ == '__main__':
    app.run(debug=False)
