from flask import Flask, render_template, request, jsonify

# Flask akan otomatis mencari folder 'templates' yang sudah Bapak buat
app = Flask(__name__)

@app.route('/')
def login_page():
    # Ini akan membuka file login.html di folder templates
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    # Ini akan membuka file index.html di folder templates
    return render_template('index.html')

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
