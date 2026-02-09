from flask import Flask, render_template_string

app = Flask(__name__)

# KODE UTUH: LOGIN, VIDEO, & BANNER SUDAH FIX
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
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; position: relative; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .visual-box { width: 100%; height: 130px; margin-bottom: 15px; border: 1px solid #444; overflow: hidden; position: relative; background: #000; }
        .visual-box img, .visual-box video { width: 100%; height: 100%; object-fit: cover; }
        .ads-label { position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8); color: var(--cyan); font-size: 10px; text-align: center; padding: 5px 0; border-top: 1px solid var(--cyan); }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; font-size: 12px; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); }
        .lock-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; justify-content: center; align-items: center; }
        .lock-box { width: 320px; padding: 30px; border: 2px solid var(--cyan); background: #05050a; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SIKEPAL V.ULTRA</h1>
        <div style="font-size: 12px; color: var(--pink);">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN (2024-2026)</div>
    </div>

    <div class="hud-bar">
        <div id="clock">TIME: 00:00:00</div>
        <div style="color: #0f0;">● SYSTEM ONLINE</div>
    </div>

    <div class="ticker-wrap"><div class="ticker">SIKEPAL COMMAND CENTER ONLINE... BROADCASTING FROM STATION CIKEMBAR...</div></div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE SIGA</div>
            <div class="visual-box">
                <img src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/banner1.jpg" onerror="this.src='https://via.placeholder.com/300x150/000000/00f0ff?text=BANNER+1+MISSING'">
                <div class="ads-label">DASHBOARD MODULE ACTIVE</div>
            </div>
            <button class="btn-cyber" onclick="showLock()">🔓 OPEN SIGA MODULES</button>
            <div id="siga-unlocked" style="display:none; margin-top:10px;">
                <button class="btn-cyber" onclick="window.open('https://newsiga-siga.bkkbn.go.id')">🏥 PELAYANAN KB</button>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div class="visual-box" style="height: 160px; border-color: var(--pink);">
                <video autoplay muted loop playsinline>
                    <source src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/iklan_bkkbn.mp4" type="video/mp4">
                </video>
            </div>
            <button class="btn-cyber" style="border-color:var(--pink); color:var(--pink);" onclick="window.open('https://youtube.com/@bimz82official50')">▶ BIMZ82 OFFICIAL</button>
        </div>

        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <div class="visual-box">
                <img src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/banner2.jpg" onerror="this.src='https://via.placeholder.com/300x150/000000/00f0ff?text=BANNER+2+MISSING'">
                <div class="ads-label">PARTNER NETWORK</div>
            </div>
            <button class="btn-cyber" onclick="window.open('https://kinerja.bkn.go.id')">🔗 E-KINERJA</button>
            <button class="btn-cyber" onclick="window.open('https://evisum4.bkkbn.go.id')">🔗 E-VISUM</button>
        </div>
    </div>

    <div class="lock-overlay" id="lock-screen">
        <div class="lock-box">
            <div style="color:var(--cyan); margin-bottom:15px;">🔐 ENTER ACCESS KEY</div>
            <input type="password" id="key" style="width:100%; padding:10px; margin-bottom:15px; background:#111; border:1px solid var(--cyan); color:var(--cyan); text-align:center;">
            <button class="btn-cyber" style="text-align:center;" onclick="unlock()">UNLOCK</button>
        </div>
    </div>

    <script>
        setInterval(() => { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }, 1000);
        function showLock() { document.getElementById('lock-screen').style.display = 'flex'; }
        function unlock() {
            if(document.getElementById('key').value === 'BIMZ2026') {
                document.getElementById('lock-screen').style.display = 'none';
                document.getElementById('siga-unlocked').style.display = 'block';
            } else { alert('DENIED!'); }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FULL)

if __name__ == "__main__":
    app.run()
