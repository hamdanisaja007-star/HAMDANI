from flask import Flask, render_template_string

app = Flask(__name__)

# SEMUA SUDAH JADI SATU (LOGIN & DASHBOARD)
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
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .visual-box { width: 100%; height: 140px; margin-bottom: 15px; border: 1px solid #444; overflow: hidden; position: relative; background: #000; }
        .visual-box img, .visual-box video { width: 100%; height: 100%; object-fit: cover; }
        .ads-label { position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8); color: var(--cyan); font-size: 10px; text-align: center; padding: 5px 0; border-top: 1px solid var(--cyan); }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; font-size: 12px; text-decoration: none; box-sizing: border-box; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
        
        /* LOGIN OVERLAY */
        #login-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: black; z-index: 9999; display: flex; justify-content: center; align-items: center; }
        .login-box { border: 2px solid var(--cyan); padding: 40px; text-align: center; background: #05050a; box-shadow: 0 0 30px var(--cyan); }
    </style>
</head>
<body>

    <div id="login-overlay">
        <div class="login-box">
            <h2 style="color:var(--cyan); letter-spacing:5px;">SIKEPAL LOGIN</h2>
            <input type="password" id="pass" style="background:#111; border:1px solid var(--cyan); color:var(--cyan); padding:10px; text-align:center; width:200px; margin-bottom:20px;" placeholder="ACCESS KEY">
            <br>
            <button class="btn-cyber" style="text-align:center" onclick="checkLogin()">AUTHORIZE SYSTEM</button>
        </div>
    </div>

    <div class="header"><h1>SIKEPAL V.ULTRA</h1></div>
    <div class="hud-bar"><div id="clock">TIME: 00:00:00</div><div>STATION: CIKEMBAR_CORE_0210</div><div style="color: #0f0;">● SYSTEM ONLINE</div></div>
    <div class="ticker-wrap"><div class="ticker">SIKEPAL SYSTEM READY... MONITORING ACTIVE... STATION CIKEMBAR ONLINE...</div></div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE SIGA</div>
            <div class="visual-box">
                <img src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan1.jpg">
                <div class="ads-label">SIGA MODULE ACTIVE</div>
            </div>
            <div id="siga-locked">
                <button class="btn-cyber" style="text-align:center" onclick="unlockSiga()">🔓 OPEN SIGA FOLDER</button>
            </div>
            <div id="siga-content" style="display:none">
                <a href="https://newsiga-siga.bkkbn.go.id" target="_blank" class="btn-cyber">🏥 PELAYANAN KB</a>
                <a href="#" class="btn-cyber">👤 DATA PPKBD</a>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div class="visual-box" style="height: 180px; border-color: var(--pink);">
                <video autoplay muted loop playsinline>
                    <source src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan_bkkbn.mp4" type="video/mp4">
                </video>
            </div>
            <button class="btn-cyber" style="border-color:var(--pink); color:var(--pink);" onclick="window.open('https://youtube.com/@bimz82official50')">▶ BIMZ82 OFFICIAL</button>
        </div>

        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <div class="visual-box">
                <img src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan2.jpg">
                <div class="ads-label">PARTNER NETWORK</div>
            </div>
            <a href="https://kinerja.bkn.go.id" target="_blank" class="btn-cyber">🔗 E-KINERJA</a>
            <a href="https://evisum4.bkkbn.go.id" target="_blank" class="btn-cyber">🔗 E-VISUM</a>
        </div>
    </div>

    <script>
        function updateClock() { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }
        setInterval(updateClock, 1000);

        function checkLogin() {
            if(document.getElementById('pass').value === 'BIMZ2026') {
                document.getElementById('login-overlay').style.display = 'none';
            } else { alert('ACCESS DENIED'); }
        }

        function unlockSiga() {
            let p = prompt("Enter Siga Key:");
            if(p === 'BIMZ2026') {
                document.getElementById('siga-locked').style.display = 'none';
                document.getElementById('siga-content').style.display = 'block';
            }
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
