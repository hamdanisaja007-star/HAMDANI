from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- SEMUA KODE TAMPILAN (LOGIN + DASHBOARD) ---
HTML_FULL = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body, html { margin: 0; padding: 0; background: var(--dark); color: white; font-family: 'Consolas', monospace; height: 100%; }
        
        /* --- TAMPILAN LOGIN (LAYER PALING ATAS) --- */
        #login-screen { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: black; z-index: 9999; display: flex; justify-content: center; align-items: center; 
        }
        .login-box { 
            border: 2px solid var(--cyan); padding: 40px; text-align: center; 
            box-shadow: 0 0 30px var(--cyan); background: rgba(5, 5, 10, 0.95); width: 350px; 
        }
        .login-box h2 { color: var(--cyan); letter-spacing: 5px; font-family: 'Impact'; margin-bottom: 20px; }
        .login-input { 
            width: 100%; padding: 12px; margin-bottom: 20px; background: #111; 
            border: 1px solid var(--cyan); color: var(--cyan); text-align: center; box-sizing: border-box; font-size: 18px; outline: none;
        }

        /* --- TAMPILAN DASHBOARD --- */
        #main-dashboard { display: none; padding: 20px; overflow-x: hidden; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 45px; letter-spacing: 5px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .hud-bar { display: flex; justify-content: space-between; padding: 10px 20px; color: var(--pink); font-size: 14px; font-weight: bold; }
        .ticker-wrap { width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1); border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink); margin-bottom: 20px; white-space: nowrap; }
        .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0; }
        @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; position: relative; }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }
        
        .visual-box { width: 100%; height: 140px; margin-bottom: 15px; border: 1px solid #222; overflow: hidden; position: relative; background: #000; }
        .visual-box img, .visual-box video { width: 100%; height: 100%; object-fit: cover; }

        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; text-decoration: none; font-size: 12px; box-sizing: border-box; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
        .btn-pink { border-color: var(--pink); color: var(--pink); }
        .btn-pink:hover { background: var(--pink); color: white; }

        .affiliate-mini { border: 1px dashed var(--green); background: rgba(0, 255, 0, 0.05); padding: 8px; margin-top: 10px; }
        .lock-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 2000; justify-content: center; align-items: center; }
        .lock-box { width: 320px; padding: 30px; border: 2px solid var(--cyan); background: #05050a; text-align: center; }
    </style>
</head>
<body>
    <div id="login-screen">
        <div class="login-box">
            <h2>SIKEPAL LOGIN</h2>
            <input type="password" id="main-pass" class="login-input" placeholder="ACCESS KEY">
            <button class="btn-cyber" style="text-align:center" onclick="mainAuth()">INITIALIZE ACCESS</button>
        </div>
    </div>

    <div id="main-dashboard">
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
            <div class="ticker" id="running-text">INITIALIZING QUANTUM LINK... WAITING FOR REMOTE BROADCAST...</div>
        </div>

        <div class="main-grid">
            <div class="panel">
                <div class="panel-title">📂 MODULE ENTRI SIGA</div>
                <div class="visual-box">
                    <img id="img-1" src="https://via.placeholder.com/300x150/000000/00f0ff?text=SIKEPAL+SIGA">
                </div>

                <div id="siga-locked" style="text-align: center; padding: 10px;">
                    <div style="font-size: 40px; margin-bottom: 10px;">🔐</div>
                    <button class="btn-cyber" style="text-align: center;" onclick="showLock('FOLDER SIGA', 'folder_siga')">🔓 OPEN SIGA MODULES</button>
                </div>

                <div id="siga-unlocked" style="display: none;">
                    <button class="btn-cyber" onclick="exe('🏥 PELAYANAN KB', 'https://newsiga-siga.bkkbn.go.id')">🏥 PELAYANAN KB</button>
                    <button class="btn-cyber" onclick="exe('👤 DATA PPKBD', '#')">👤 DATA PPKBD</button>
                    <button class="btn-cyber" onclick="exe('👶 KELOMPOK BKB', '#')">👶 KELOMPOK BKB</button>
                    <button class="btn-cyber" onclick="exe('🧑 KELOMPOK BKR', '#')">🧑 KELOMPOK BKR</button>
                    <button class="btn-cyber" style="border-color: #ff4444; color: #ff4444; margin-top: 10px; text-align: center;" onclick="lockSiga()">🔒 CLOSE FOLDER</button>
                </div>
            </div>

            <div class="panel">
                <div class="panel-title">📺 MEDIA MONITOR</div>
                <div class="visual-box" style="border-color: var(--pink); height: 160px;">
                    <video id="video-ads" autoplay muted loop playsinline>
                        <source src="https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/static/iklan_bkkbn.mp4" type="video/mp4">
                    </video>
                </div>
                
                <div class="affiliate-mini">
                    <span style="color:var(--green); font-size:10px;">🛒 KERTAS HVS A4 - RP 45.000</span>
                    <button class="btn-cyber" style="border-color: var(--green); padding: 5px; font-size: 10px;" onclick="window.open('https://shope.ee/link_hvs', '_blank')">🛒 BELI</button>
                </div>

                <button class="btn-cyber btn-pink" style="margin-top: 15px;" onclick="window.open('https://youtube.com/@bimz82official50','_blank')">▶ BIMZ82 OFFICIAL</button>
            </div>

            <div class="panel">
                <div class="panel-title">🌐 EXTERNAL HUB</div>
                <div class="visual-box">
                    <img id="img-3" src="https://via.placeholder.com/300x150/000000/00f0ff?text=HUB+ACTIVE">
                </div>
                <button class="btn-cyber" onclick="exe('E-KINERJA', 'https://kinerja.bkn.go.id')">🔗 PORTAL E-KINERJA</button>
                <button class="btn-cyber" onclick="exe('E-VISUM', 'https://evisum4.bkkbn.go.id')">🔗 E-VISUM WEB</button>
                <button class="btn-cyber" onclick="exe('NEWSIGA', 'https://newsiga-siga.bkkbn.go.id')">🔗 WEB NEWSIGA</button>
                <button class="btn-cyber" onclick="exe('GOOGLE', 'https://google.com')">🔗 GOOGLE SEARCH</button>
            </div>
        </div>

        <div class="footer" style="text-align: center; margin-top: 30px; color: #444;">
            DEDE BIMZ & RAHMAN &copy; 2026 | <a href="#" onclick="location.reload()" style="color:red; text-decoration:none;">[ EXIT ]</a>
        </div>
    </div>

    <div class="lock-overlay" id="lock-screen">
        <div class="lock-box">
            <div style="color: var(--cyan); font-weight: bold; margin-bottom: 10px;">🔐 MODULE LOCKED</div>
            <input type="password" id="access-key" class="login-input" style="font-size:14px" placeholder="ENTER KEY">
            <button class="btn-cyber" style="text-align:center" onclick="validateKey()">UNLOCK</button>
            <button class="btn-cyber" style="border-color:red; color:red; text-align:center" onclick="hideLock()">CANCEL</button>
        </div>
    </div>

    <script>
        const SECRET_KEY = "BIMZ2026";
        
        function mainAuth() {
            if(document.getElementById('main-pass').value === SECRET_KEY) {
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('main-dashboard').style.display = 'block';
                startClock();
            } else { alert("WRONG KEY!"); }
        }

        function startClock() {
            setInterval(() => {
                document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString();
            }, 1000);
        }

        function showLock(name, mode) {
            document.getElementById('lock-screen').style.display = 'flex';
        }

        function hideLock() { document.getElementById('lock-screen').style.display = 'none'; }

        function validateKey() {
            if(document.getElementById('access-key').value === SECRET_KEY) {
                hideLock();
                document.getElementById('siga-locked').style.display = 'none';
                document.getElementById('siga-unlocked').style.display = 'block';
            } else { alert("DENIED!"); }
        }

        function lockSiga() {
            document.getElementById('siga-locked').style.display = 'block';
            document.getElementById('siga-unlocked').style.display = 'none';
        }

        function exe(name, url) { if(url !== '#') window.open(url, '_blank'); }
    </script>
</body>
</html>
"""

@app.route('/')
def main():
    return render_template_string(HTML_FULL)

@app.route('/handler', methods=['POST'])
def handler():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
