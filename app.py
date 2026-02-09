from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- 1. HALAMAN LOGIN ---
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - ACCESS</title>
    <style>
        body { background: #020205; color: #00f0ff; font-family: 'Consolas', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { border: 2px solid #00f0ff; padding: 40px; text-align: center; box-shadow: 0 0 20px #00f0ff; background: rgba(0,0,0,0.9); }
        input { background: #111; border: 1px solid #00f0ff; color: #00f0ff; padding: 12px; margin: 20px 0; width: 250px; text-align: center; font-size: 18px; outline: none; }
        button { background: #00f0ff; color: black; border: none; padding: 12px 30px; font-weight: bold; cursor: pointer; width: 100%; transition: 0.3s; }
        button:hover { background: white; box-shadow: 0 0 15px #00f0ff; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2 style="letter-spacing: 5px; margin: 0;">SIKEPAL LOGIN</h2>
        <input type="password" id="pass" placeholder="ACCESS KEY">
        <button onclick="check()">INITIALIZE ACCESS</button>
    </div>
    <script>
        function check() {
            if(document.getElementById('pass').value === 'BIMZ2026') { window.location.href='/dashboard'; }
            else { alert('ACCESS DENIED!'); }
        }
    </script>
</body>
</html>
"""

# --- 2. HALAMAN DASHBOARD (DENGAN KODE BAPAK YG ASLI) ---
DASHBOARD_PAGE = """
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
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
        .visual-box { width: 100%; height: 130px; margin-bottom: 15px; border: 1px solid #222; overflow: hidden; position: relative; background: #000; }
        .visual-box video { width: 100%; height: 100%; object-fit: cover; }
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
    <div class="ticker-wrap"><div class="ticker">SYSTEM ACTIVE... READY TO SERVE... CONNECTING TO NEWSIGA CORE...</div></div>
    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE ENTRI SIGA</div>
            <button class="btn-cyber" onclick="window.open('https://newsiga-siga.bkkbn.go.id','_blank')">🏥 PELAYANAN KB</button>
            <button class="btn-cyber">👤 DATA PPKBD</button>
            <button class="btn-cyber">👶 KELOMPOK BKB</button>
            <button class="btn-cyber">🧑 KELOMPOK BKR</button>
        </div>
        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div class="visual-box">
                <video autoplay muted loop playsinline style="width:100%;">
                    <source src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/iklan_bkkbn.mp4" type="video/mp4">
                </video>
            </div>
            <button class="btn-cyber" style="border-color:var(--pink);color:var(--pink);" onclick="window.open('https://youtube.com/@bimz82official50','_blank')">▶ BIMZ82 OFFICIAL</button>
        </div>
        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id','_blank')">🔗 E-KINERJA</button>
            <button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id','_blank')">🔗 E-VISUM</button>
            <button class="btn-cyber" onclick="window.open('https://google.com','_blank')">🔗 GOOGLE</button>
        </div>
    </div>
    <div style="text-align:center; margin-top:30px;"><a href="/" style="color:red; text-decoration:none;">[ LOGOUT SYSTEM ]</a></div>
    <script>
        function updateClock() { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(LOGIN_PAGE)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_PAGE)

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "success"})

# PENTING: Untuk Vercel, jangan pakai app.run() di dalam indentasi
if __name__ == '__main__':
    app.run(debug=True)
