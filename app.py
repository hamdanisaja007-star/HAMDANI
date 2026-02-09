from flask import Flask, render_template_string, jsonify, request
import requests

app = Flask(__name__)

# --- TEMPLATE HTML KEREN PUNYA MAS HAMDANI ---
HTML_FULL = """
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
        .header {
            border: 2px solid var(--cyan); padding: 15px; text-align: center;
            box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9);
        }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; position: relative; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .visual-box { width: 100%; height: 130px; margin-bottom: 15px; border: 1px solid #222; overflow: hidden; position: relative; background: #000; }
        .visual-box img, .visual-box video { width: 100%; height: 100%; object-fit: cover; transition: opacity 0.8s ease-in-out; opacity: 0.9; }
        .ads-label { position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8); color: var(--cyan); font-size: 10px; text-align: center; padding: 5px 0; border-top: 1px solid var(--cyan); text-transform: uppercase; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
        .btn-pink { border-color: var(--pink); color: var(--pink); }
        .btn-pink:hover { background: var(--pink); color: white; box-shadow: 0 0 20px var(--pink); }
        .affiliate-mini { border: 1px dashed var(--green); background: rgba(0, 255, 0, 0.05); padding: 8px; margin-top: 10px; transition: 0.3s; }
        .affiliate-mini:hover { background: rgba(0, 255, 0, 0.1); }
        .price-tag { color: var(--green); font-size: 10px; font-weight: bold; display: block; margin-bottom: 3px; }
        .lock-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; justify-content: center; align-items: center; }
        .lock-box { width: 350px; padding: 30px; border: 2px solid var(--cyan); background: #05050a; text-align: center; box-shadow: 0 0 30px var(--cyan); }
        .lock-input { width: 100%; padding: 10px; margin: 15px 0; background: #111; border: 1px solid var(--cyan); color: var(--cyan); text-align: center; font-family: 'Consolas'; font-size: 18px; outline: none; box-sizing: border-box; }
        .tools-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 30px; padding: 15px; font-size: 12px; color: #666; border-top: 1px solid #222; }
        .scanline { width: 100%; height: 100px; background: linear-gradient(0deg, transparent, rgba(0, 240, 255, 0.05), transparent); position: fixed; top: -100px; left: 0; z-index: 100; animation: scanning 6s linear infinite; pointer-events: none; }
        @keyframes scanning { from { top: -100px; } to { top: 100%; } }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="header"><h1>SIKEPAL V.ULTRA</h1><div style="font-size: 13px; color: var(--pink); letter-spacing: 2px;">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN (2024-2026)</div></div>
    <div class="hud-bar"><div id="clock">TIME: 00:00:00</div><div>STATION: CIKEMBAR_CORE_0210</div><div style="color: #0f0;" id="net-status">● SYSTEM ONLINE</div></div>
    <div class="ticker-wrap"><div class="ticker" id="running-text">INITIALIZING QUANTUM LINK...</div></div>
    <div class="main-grid">
        <div class="panel"><div class="panel-title">📂 MODULE ENTRI SIGA</div><div class="visual-box" id="box-1"><img id="img-1" src=""><div class="ads-label" id="txt-1">LOADING ADS...</div></div><div id="siga-locked" style="text-align: center; padding: 10px;"><div style="font-size: 40px; margin-bottom: 10px;">🔐</div><button class="btn-cyber" style="text-align: center;" onclick="showLock('FOLDER SIGA', 'all', 'folder_siga')">🔓 OPEN SIGA MODULES</button></div><div id="siga-unlocked" style="display: none;"><button class="btn-cyber" onclick="processExe('🏥 PELAYANAN KB', 'pelayanan_kb', 'modul')">🏥 PELAYANAN KB</button><button class="btn-cyber" onclick="processExe('👤 DATA PPKBD', 'ppkbd', 'modul')">👤 DATA PPKBD</button><button class="btn-cyber" style="border-color: #ff4444; color: #ff4444; margin-top: 10px; font-size: 10px; text-align: center;" onclick="lockSiga()">🔒 CLOSE FOLDER</button></div></div>
        <div class="panel"><div class="panel-title">📺 MEDIA MONITOR</div><div class="visual-box" style="border-color: var(--pink); height: 160px;"><video autoplay muted loop playsinline style="width: 100%; height: 100%; object-fit: cover;"><source src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan_bkkbn.mp4" type="video/mp4"></video></div><button class="btn-cyber btn-pink" onclick="window.open('https://youtube.com/@bimz82official50')">▶ BIMZ82 OFFICIAL</button></div>
        <div class="panel"><div class="panel-title">🌐 EXTERNAL HUB</div><div class="visual-box" id="box-3"><img id="img-3" src=""><div class="ads-label" id="txt-3">PARTNER ADS</div></div><button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id')">🔗 PORTAL E-KINERJA</button><button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id')">🔗 E-VISUM WEB</button></div>
    </div>
    <div class="lock-overlay" id="lock-screen"><div class="lock-box"><div style="color: var(--cyan); font-weight: bold; margin-bottom: 10px;">🔐 ACCESS RESTRICTED</div><input type="password" id="access-key" class="lock-input" placeholder="ENTER ACCESS KEY"><button class="btn-cyber" onclick="validateKey()">UNLOCK MODULE</button></div></div>
    <script>
        function updateClock() { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000);
        const SECRET_KEY = "BIMZ2026";
        let currentLockedAction = null;
        function showLock(name, target, mode) { currentLockedAction = {name, target, mode}; document.getElementById('lock-screen').style.display = 'flex'; }
        function hideLock() { document.getElementById('lock-screen').style.display = 'none'; }
        function validateKey() { if (document.getElementById('access-key').value === SECRET_KEY) { hideLock(); if (currentLockedAction.mode === 'folder_siga') { document.getElementById('siga-locked').style.display = 'none'; document.getElementById('siga-unlocked').style.display = 'block'; } else { processExe(currentLockedAction.name, currentLockedAction.target, currentLockedAction.mode); } } else { alert("DENIED"); } }
        function lockSiga() { document.getElementById('siga-locked').style.display = 'block'; document.getElementById('siga-unlocked').style.display = 'none'; }
        function processExe(name, target, mode) {
            fetch('/handler', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, target: target, mode: mode})
            }).then(res => res.json()).then(data => alert(data.status)).catch(err => alert("Offline"));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FULL)

@app.route('/handler', methods=['POST'])
def handler():
    data = request.json
    # PAKAI LINK NGROK TERBARU MAS
    URL_LAPTOP = "https://plastered-nonsubtly-tamera.ngrok-free.dev/jalankan-robot"
    try:
        response = requests.post(URL_LAPTOP, json=data, timeout=8)
        return jsonify({"status": "Robot Dipanggil!", "detail": response.json()})
    except:
        return jsonify({"status": "Gagal Terhubung ke Laptop"})

if __name__ == "__main__":
    app.run()
