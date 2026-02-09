import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- HTML LOGIN ---
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SIKEPAL - LOGIN</title>
    <style>
        body { background: #020205; color: #00f0ff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { border: 2px solid #00f0ff; padding: 30px; text-align: center; box-shadow: 0 0 20px #00f0ff; }
        input { background: #111; border: 1px solid #00f0ff; color: #00f0ff; padding: 10px; margin: 10px 0; width: 200px; text-align: center; }
        button { background: #00f0ff; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; width: 100%; }
    </style>
</head>
<body>
    <div class="box">
        <h2>SIKEPAL V.ULTRA</h2>
        <input type="password" id="p" placeholder="PASSWORD">
        <button onclick="check()">LOGIN</button>
    </div>
    <script>
        function check(){ if(document.getElementById('p').value==='BIMZ2026') window.location.href='/dashboard'; else alert('DENIED'); }
    </script>
</body>
</html>
"""

# --- HTML DASHBOARD ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; }
        body { background: var(--dark); color: white; font-family: monospace; margin: 0; padding: 20px; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 35px; color: var(--cyan); font-family: Impact; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.9); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0,240,255,0.1); border: 1px solid var(--cyan); color: white; cursor: pointer; text-align: left; text-decoration: none; font-size: 12px; }
        .btn-cyber:hover { background: var(--cyan); color: black; }
        .ticker { background: rgba(255,0,255,0.1); color: var(--pink); padding: 10px; border: 1px solid var(--pink); margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header"><h1>SIKEPAL V.ULTRA</h1></div>
    <div class="ticker">SYSTEM ONLINE | STATION: CIKEMBAR_CORE_0210</div>
    <div class="main-grid">
        <div class="panel">
            <h3 style="color:var(--cyan)">📂 MODULE SIGA</h3>
            <a href="https://newsiga-siga.bkkbn.go.id" target="_blank" class="btn-cyber">🏥 PELAYANAN KB</a>
            <button class="btn-cyber">👤 DATA PPKBD</button>
            <button class="btn-cyber">👶 KELOMPOK BKB</button>
        </div>
        <div class="panel">
            <h3 style="color:var(--pink)">📺 MEDIA</h3>
            <div style="height:150px; background:black; border:1px solid var(--pink); display:flex; align-items:center; justify-content:center; color:var(--pink);">MONITOR ACTIVE</div>
        </div>
        <div class="panel">
            <h3 style="color:var(--cyan)">🌐 HUB</h3>
            <a href="https://kinerja.bkn.go.id" target="_blank" class="btn-cyber">🔗 E-KINERJA</a>
            <a href="https://evisum4.bkkbn.go.id" target="_blank" class="btn-cyber">🔗 E-VISUM</a>
            <a href="https://google.com" target="_blank" class="btn-cyber">🔗 GOOGLE</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LOGIN_HTML)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

# Versi Vercel membutuhkan object app
app = app
