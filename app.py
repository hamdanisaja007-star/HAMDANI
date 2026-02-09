from flask import Flask, render_template, request, jsonify

# Flask secara otomatis akan mencari folder bernama 'templates'
app = Flask(__name__)

@app.route('/')
def login_page():
    # Flask akan otomatis mencari templates/login.html
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    # Flask akan otomatis mencari templates/index.html
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
