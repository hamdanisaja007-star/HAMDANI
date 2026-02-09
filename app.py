from flask import Flask, render_template, request, jsonify
import os

# Kode ini akan otomatis nyari alamat folder yang benar
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
