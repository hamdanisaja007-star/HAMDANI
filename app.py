from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ==========================================
# 1. HALAMAN LOGIN (SIKEPAL V.ULTRA ACCESS)
# ==========================================
login_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - ACCESS POINT</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; }
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background: black; font-family: 'Consolas', monospace; }
        #bg-video { position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -2; filter: brightness(0.4) contrast(1.2); }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle, transparent 20%, var(--dark) 80%); z-index: -1; }
        .login-container { display: flex; justify-content: center; align-items: center; height: 100vh; gap: 40px; }
        .login-box { width: 380px; padding: 40px; background: rgba(5, 5, 10, 0.9); border: 1px solid var(--cyan); box-shadow: 0 0 30px var(--cyan); text-align: center; }
        .login-box h2 { color: var(--cyan); letter-spacing: 5px; margin: 0; font-family: 'Impact'; font-size: 35px; text-shadow: 0 0 10px var(--cyan); }
        .input-group { margin: 30px 0; }
        .input-group input { width: 100%; padding: 15px; background: rgba(0, 240, 255, 0.1); border: 1px solid var(--cyan); color: var(--cyan); font-size: 20px; text-align: center; outline: none; box-sizing: border-box; }
        .btn-login { width: 100%; padding: 15px; background: var(--cyan); border: none; color: black; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; text-transform: uppercase; }
        .btn-login:hover { background: white; box-shadow: 0 0 25px var(--cyan); letter-spacing: 2px; }
        .footer-tag { position: absolute; bottom: 20px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <video autoplay muted loop playsinline id="bg-video">
        <source src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/iklan_bkkbn.mp4" type="video/mp4">
    </video>
    <div class="overlay"></div>
    <div class="login-container">
        <div class="login-box">
            <h2>SIKEPAL<br><span style="font-size: 16px; letter-spacing: 2px;">V.ULTRA ACCESS</span></h2>
            <div class="input-group">
                <input type="password" id="pass" placeholder="ENTER ACCESS KEY" autocomplete="off">
            </div>
            <button class="btn-login" onclick="checkAuth()">INITIALIZE ACCESS</button>
            <div id="msg" style="margin-top: 15px; font-size: 12px; color: #444;">AWAITING COMMAND...</div>
        </div>
    </div>
    <script>
        function checkAuth() {
            const pass = document.getElementById('pass').value;
            if (pass === "BIMZ2026") {
                window.location.href = "/dashboard";
            } else {
                alert("INVALID ACCESS KEY!");
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# 2. HALAMAN DASHBOARD (COMMAND CENTER)
# ==========================================
dashboard_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body {
            background: var(--dark); color: white; font-family: 'Consolas', monospace;
            margin: 0; padding: 20px; overflow-x: hidden;
            background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
            background-size: 30px 30px;
        }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }
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
        <div style="font-size: 13px; color: var(--pink); letter-spacing: 2px;">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN (2024-2026)</div>
    </div>
    <div class="hud-bar">
        <div id="clock">TIME: 00:00:00</div>
        <div>STATION: CIKEMBAR_CORE_0210</div>
        <div style="color: #0f0;">● SYSTEM ONLINE</div>
    </div>
    <div class="ticker-wrap">
        <div class="ticker">INITIALIZING QUANTUM LINK... WAITING FOR REMOTE BROADCAST... SYNCING DATA CIKEMBAR...</div>
    </div>
    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE ENTRI SIGA</div>
            <button class="btn-cyber">🏥 PELAYANAN KB</button>
            <button class="btn-cyber">👤 DATA PPKBD</button>
            <button class="btn-cyber">👶 KELOMPOK BKB</button>
        </div>
        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div style="height:150px; background:#000; border:1px solid var(--pink); display:flex; align-items:center; justify:center;">
                <p style="color:var(--pink); font-size:10px; text-align:center;">VIDEO MONITOR ACTIVE</p>
            </div>
        </div>
        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id')">🔗 PORTAL E-KINERJA</button>
            <button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id')">🔗 E-VISUM WEB</button>
            <button class="btn-cyber" onclick="window.open('https://newsiga-siga.bkkbn.go.id')">🔗 WEB NEWSIGA</button>
        </div>
    </div>
    <div style="text-align: center; margin-top: 20px;">
        <a href="/" style="color: #f00; text-decoration: none;">[ LOGOUT SYSTEM ]</a>
    </div>
    <script>
        function updateClock() {
            document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString();
        }
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

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
