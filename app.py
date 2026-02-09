from flask import Flask, render_template_string

app = Flask(__name__)

# SEMUA KODE TAMPILAN (LOGIN & DASHBOARD) DISATUKAN DI SINI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body, html { margin: 0; padding: 0; background: var(--dark); color: white; font-family: 'Consolas', monospace; height: 100%; overflow-x: hidden; }
        
        /* --- STYLE LOGIN --- */
        #login-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; display: flex; justify-content: center; align-items: center; }
        .login-box { border: 2px solid var(--cyan); padding: 40px; text-align: center; box-shadow: 0 0 25px var(--cyan); background: rgba(5, 5, 10, 0.95); width: 320px; }
        .login-box h2 { color: var(--cyan); letter-spacing: 5px; font-family: 'Impact'; margin-bottom: 30px; }
        input[type="password"] { width: 100%; padding: 12px; margin-bottom: 20px; background: #111; border: 1px solid var(--cyan); color: var(--cyan); text-align: center; box-sizing: border-box; }
        .btn-login { width: 100%; padding: 12px; background: var(--cyan); border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-login:hover { background: white; box-shadow: 0 0 15px var(--cyan); }

        /* --- STYLE DASHBOARD --- */
        .dashboard-container { display: none; padding: 20px; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; text-decoration: none; font-size: 12px; box-sizing: border-box; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); }
        .visual-box { width: 100%; height: 130px; margin-bottom: 15px; border: 1px solid #222; overflow: hidden; background: #000; }
    </style>
</head>
<body>

    <div id="login-screen">
        <div class="login-box">
            <h2>SIKEPAL LOGIN</h2>
            <input type="password" id="access-key" placeholder="ENTER ACCESS KEY">
            <button class="btn-login" onclick="validate()">INITIALIZE ACCESS</button>
        </div>
    </div>

    <div id="main-dashboard" class="dashboard-container">
        <div class="header">
            <h1>SIKEPAL V.ULTRA</h1>
            <div style="font-size: 13px; color: var(--pink);">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN (2024-2026)</div>
        </div>

        <div class="hud-bar">
            <div id="clock">TIME: --:--:--</div>
            <div>STATION: CIKEMBAR_CORE_0210</div>
            <div style="color: #0f0;">● SYSTEM ONLINE</div>
        </div>

        <div class="ticker-wrap"><div class="ticker">SIKEPAL SYSTEM READY... CONNECTING TO NEWSIGA... MONITORING ACTIVE... STATION CIKEMBAR ONLINE...</div></div>

        <div class="main-grid">
            <div class="panel">
                <div class="panel-title">📂 MODULE ENTRI SIGA</div>
                <a href="https://newsiga-siga.bkkbn.go.id" target="_blank" class="btn-cyber">🏥 PELAYANAN KB</a>
                <button class="btn-cyber">👤 DATA PPKBD</button>
                <button class="btn-cyber">👶 KELOMPOK BKB</button>
                <button class="btn-cyber">🧑 KELOMPOK BKR</button>
                <button class="btn-cyber">👴 KELOMPOK BKL</button>
            </div>

            <div class="panel">
                <div class="panel-title">📺 MEDIA MONITOR</div>
                <div class="visual-box">
                    <video autoplay muted loop playsinline style="width: 100%; height: 100%; object-fit: cover;">
                        <source src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/iklan_bkkbn.mp4" type="video/mp4">
                    </video>
                </div>
                <button class="btn-cyber" style="border-color: var(--pink); color: var(--pink);" onclick="window.open('https://youtube.com/@bimz82official50')">▶ BIMZ82 OFFICIAL</button>
            </div>

            <div class="panel">
                <div class="panel-title">🌐 EXTERNAL HUB</div>
                <a href="https://kinerja.bkn.go.id" target="_blank" class="btn-cyber">🔗 PORTAL E-KINERJA</a>
                <a href="https://evisum4.bkkbn.go.id" target="_blank" class="btn-cyber">🔗 E-VISUM WEB</a>
                <a href="https://newsiga-siga.bkkbn.go.id" target="_blank" class="btn-cyber">🔗 WEB NEWSIGA</a>
                <a href="https://google.com" target="_blank" class="btn-cyber">🔗 GOOGLE SEARCH</a>
            </div>
        </div>
        <div style="text-align: center; margin-top: 20px; border-top: 1px solid #222; padding-top: 10px;">
            <button onclick="location.reload()" style="background:none; border:none; color:red; cursor:pointer;">[ LOGOUT ]</button>
        </div>
    </div>

    <script>
        function validate() {
            const key = document.getElementById('access-key').value;
            if (key === 'BIMZ2026') {
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('main-dashboard').style.display = 'block';
                startClock();
            } else {
                alert('ACCESS DENIED!');
            }
        }
        function startClock() {
            setInterval(() => {
                document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString();
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Vercel setup
app = app
