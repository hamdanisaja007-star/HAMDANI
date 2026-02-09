from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- LOGIN PAGE ---
login_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL - LOGIN</title>
    <style>
        body { background: #020205; color: #00f0ff; font-family: 'Consolas', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { border: 2px solid #00f0ff; padding: 30px; text-align: center; box-shadow: 0 0 20px #00f0ff; background: rgba(0,0,0,0.8); }
        input { background: #111; border: 1px solid #00f0ff; color: #00f0ff; padding: 10px; margin: 15px 0; width: 80%; text-align: center; outline: none; }
        button { background: #00f0ff; color: black; border: none; padding: 10px 25px; font-weight: bold; cursor: pointer; width: 100%; transition: 0.3s; }
        button:hover { background: white; box-shadow: 0 0 15px #00f0ff; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2 style="letter-spacing: 5px;">SIKEPAL V.ULTRA</h2>
        <input type="password" id="pass" placeholder="ACCESS KEY">
        <button onclick="check()">INITIALIZE ACCESS</button>
    </div>
    <script>
        function check() {
            if(document.getElementById('pass').value === 'BIMZ2026') { window.location.href='/dashboard'; }
            else { alert('ACCESS DENIED'); }
        }
    </script>
</body>
</html>
"""

# --- DASHBOARD PAGE (HTML BAPAK UTUH) ---
dashboard_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body { background: var(--dark); color: white; font-family: 'Consolas', monospace; margin: 0; padding: 20px; overflow-x: hidden; background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px); background-size: 30px 30px; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; position: relative; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
    </style>
</head>
<body>
    <div class="header">
        <h1>SIKEPAL V.ULTRA</h1>
        <div style="font-size: 13px; color: var(--pink);">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN</div>
    </div>
    <div class="hud-bar">
        <div id="clock">TIME: 00:00:00</div>
        <div>STATION: CIKEMBAR_CORE_0210</div>
        <div style="color: #0f0;">● SYSTEM ONLINE</div>
    </div>
    <div class="ticker-wrap"><div class="ticker">SIKEPAL SYSTEM READY... CONNECTING TO NEWSIGA... MONITORING ACTIVE...</div></div>
    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE ENTRI SIGA</div>
            <button class="btn-cyber" onclick="window.open('https://newsiga-siga.bkkbn.go.id')">🏥 PELAYANAN KB</button>
            <button class="btn-cyber">👤 DATA PPKBD</button>
            <button class="btn-cyber">👶 KELOMPOK BKB</button>
        </div>
        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div style="height:150px; background:#000; border:1px solid var(--pink); display:flex; align-items:center; justify-content:center; color:var(--pink);">VIDEO FEED ACTIVE</div>
        </div>
        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id')">🔗 PORTAL E-KINERJA</button>
            <button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id')">🔗 E-VISUM WEB</button>
        </div>
    </div>
    <div style="text-align:center; margin-top:20px;"><a href="/" style="color:red; text-decoration:none;">[ LOGOUT ]</a></div>
    <script>
        function updateClock() { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(login_html)

@app.route('/dashboard')
def dashboard():
    return render_template_string(dashboard_html)

# Handler dummy agar tidak error saat dipanggil JS
@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "ok"})

# Baris wajib untuk Vercel
if __name__ == "__main__":
    app.run()
