from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- HTML LOGIN ---
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>SIKEPAL ACCESS</title>
    <style>
        body { background: #000; color: #00f0ff; font-family: 'Consolas', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { border: 1px solid #00f0ff; padding: 40px; text-align: center; box-shadow: 0 0 20px #00f0ff; }
        input { background: #111; border: 1px solid #00f0ff; color: #00f0ff; padding: 10px; margin: 10px; text-align: center; }
        button { background: #00f0ff; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>SIKEPAL V.ULTRA</h2>
        <input type="password" id="p" placeholder="PASSWORD">
        <button onclick="go()">ENTER</button>
    </div>
    <script>
        function go() { if(document.getElementById('p').value==='BIMZ2026') window.location.href='/dashboard'; else alert('WRONG'); }
    </script>
</body>
</html>
"""

# --- HTML DASHBOARD (SESUAI DESAIN BAPAK) ---
dashboard_page = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; }
        body { background: var(--dark); color: white; font-family: 'Consolas', monospace; margin: 0; padding: 20px; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 35px; color: var(--cyan); font-family: 'Impact'; }
        .main-grid { display: grid; grid-template-columns: 1fr 300px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0,240,255,0.05); border: 1px solid var(--cyan); color: white; cursor: pointer; text-align: left; }
        .btn-cyber:hover { background: var(--cyan); color: black; }
        .ticker { background: rgba(255,0,255,0.1); color: var(--pink); padding: 10px; border: 1px solid var(--pink); margin-bottom: 20px; overflow: hidden; }
    </style>
</head>
<body>
    <div class="header"><h1>SIKEPAL V.ULTRA</h1></div>
    <div class="ticker">SYSTEM ONLINE | STATION: CIKEMBAR_CORE</div>
    <div class="main-grid">
        <div class="panel">
            <h3 style="color:var(--cyan)">📂 MODULE SIGA</h3>
            <button class="btn-cyber" onclick="window.open('https://newsiga-siga.bkkbn.go.id')">🏥 PELAYANAN KB</button>
            <button class="btn-cyber">👤 DATA PPKBD</button>
            <button class="btn-cyber">👶 KELOMPOK BKB</button>
        </div>
        <div class="panel">
            <h3 style="color:var(--pink)">📺 MONITOR</h3>
            <div style="height:100px; background:black; border:1px solid var(--pink);"></div>
        </div>
        <div class="panel">
            <h3 style="color:var(--cyan)">🌐 HUB</h3>
            <button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id')">🔗 E-KINERJA</button>
            <button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id')">🔗 E-VISUM</button>
        </div>
    </div>
    <p style="text-align:center;"><a href="/" style="color:red">[ LOGOUT ]</a></p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(login_page)

@app.route('/dashboard')
def dashboard():
    return render_template_string(dashboard_page)

# Ini penting agar Vercel tidak error saat memanggil route /handler
@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "ok"})

# Baris ini krusial untuk Flask di Vercel
app.debug = True
