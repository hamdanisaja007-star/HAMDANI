from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>MESIN SIKEPAL SUDAH NYALA!</h1><p>Kalau tulisan ini muncul, berarti Python sudah aman.</p>"

if __name__ == '__main__':
    app.run()
