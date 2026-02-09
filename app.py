from flask import Flask, render_template_string

app = Flask(__name__)

# SEMUA SISTEM LOGIN DAN DASHBOARD JADI SATU BIAR TIDAK CRASH
HTML_FULL = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body, html { margin: 0; padding: 0; background: var(--dark); color: white; font-family: 'Consolas', monospace; height: 100%; }
        
        /* --- TAMPILAN LOGIN --- */
        #login-layer { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: black; z-index: 9999; display: flex; justify-content: center; align-items: center; 
        }
        .login-box { 
            border: 2px solid var(--cyan); padding: 40px; text-align: center; 
            box-shadow: 0 0 30px var(--cyan); background: rgba(5, 5, 10, 0.95); width: 350px; 
        }
        .login-box h2 { color: var(--cyan); letter-spacing: 5px; font-family: 'Impact'; margin-bottom: 20px; }
        input[type="password"] { 
            width: 100%; padding: 12px; margin-bottom: 20px; background: #111; 
            border: 1px solid var(--cyan); color: var(--cyan); text-align: center; box-sizing: border-box; font-size: 18px;
        }
        .btn-auth { width: 100%; padding: 15px; background: var(--cyan); border: none; font-weight: bold; cursor: pointer; text-transform: uppercase; }
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

        .ticker-wrap {
            width: 100%; overflow: hidden; background: rgba(255, 0, 255, 0.1);
            border-bottom: 1px solid var(--pink); border-top: 1px solid var(--pink);
            margin-bottom: 20px; white-space: nowrap;
        }
        .ticker {
            display: inline-block; padding-left: 100%;
            animation: ticker 25s linear infinite;
            color: var(--pink); font-weight: bold; font-size: 14px; padding: 10px 0;
        }
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }

        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        
        .panel {
            background: rgba(5, 5, 10, 0.95); border: 1px solid #333;
            border-top: 4px solid var(--cyan); padding: 20px; position: relative;
        }
        .panel-title { color: var(--cyan); font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; text-transform: uppercase; }

        .visual-box { 
            width: 100%; height: 130px; margin-bottom: 15px; border: 1px solid #222; 
            overflow: hidden; position: relative; background: #000;
        }
        .visual-box img, .visual-box video { 
            width: 100%; height: 100%; object-fit: cover; 
            transition: opacity 0.8s ease-in-out; opacity: 0.9;
        }
        .ads-label {
            position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8);
            color: var(--cyan); font-size: 10px; text-align: center; padding: 5px 0;
            border-top: 1px solid var(--cyan); text-transform: uppercase;
        }

        .btn-cyber {
            display: block; width: 100%; padding: 12px; margin-bottom: 8px;
            background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan);
            color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s;
        }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); transform: scale(1.02); }
        
        .btn-pink { border-color: var(--pink); color: var(--pink); }
        .btn-pink:hover { background: var(--pink); color: white; box-shadow: 0 0 20px var(--pink); }

        /* AFFILIATE MINI STYLE */
        .affiliate-mini {
            border: 1px dashed var(--green); background: rgba(0, 255, 0, 0.05);
            padding: 8px; margin-top: 10px; transition: 0.3s;
        }
        .affiliate-mini:hover { background: rgba(0, 255, 0, 0.1); }
        .price-tag { color: var(--green); font-size: 10px; font-weight: bold; display: block; margin-bottom: 3px; }

        /* CYBER LOCK STYLE */
        .lock-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.95); z-index: 2000; justify-content: center; align-items: center;
        }
        .lock-box {
            width: 350px; padding: 30px; border: 2px solid var(--cyan);
            background: #05050a; text-align: center; box-shadow: 0 0 30px var(--cyan);
        }
        .lock-input {
            width: 100%; padding: 10px; margin: 15px 0; background: #111;
            border: 1px solid var(--cyan); color: var(--cyan); text-align: center;
            font-family: 'Consolas'; font-size: 18px; outline: none; box-sizing: border-box;
        }

        .tools-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        .footer { text-align: center; margin-top: 30px; padding: 15px; font-size: 12px; color: #666; border-top: 1px solid #222; }
        
        .scanline { width: 100%; height: 100px; background: linear-gradient(0deg, transparent, rgba(0, 240, 255, 0.05), transparent); position: fixed; top: -100px; left: 0; z-index: 100; animation: scanning 6s linear infinite; pointer-events: none; }
        @keyframes scanning { from { top: -100px; } to { top: 100%; } }
    </style>
</head>
<body>
    <div class="scanline"></div>

    <div class="header">
        <h1>SIKEPAL V.ULTRA</h1>
        <div style="font-size: 13px; color: var(--pink); letter-spacing: 2px;">OFFICIAL LICENSE: DHEDE_BIMZ & RAHMAN (2024-2026)</div>
    </div>

    <div class="hud-bar">
        <div id="clock">TIME: 00:00:00</div>
        <div>STATION: CIKEMBAR_CORE_0210</div>
        <div style="color: #0f0;" id="net-status">● SYSTEM ONLINE</div>
    </div>

    <div class="ticker-wrap">
        <div class="ticker" id="running-text">INITIALIZING QUANTUM LINK... WAITING FOR REMOTE BROADCAST...</div>
    </div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">📂 MODULE ENTRI SIGA</div>
            <div class="visual-box" id="box-1">
                <img id="img-1" src="">
                <div class="ads-label" id="txt-1">LOADING ADS...</div>
            </div>

            <div id="siga-locked" style="text-align: center; padding: 10px;">
                <div style="font-size: 40px; margin-bottom: 10px;">🔐</div>
                <button class="btn-cyber" style="text-align: center;" onclick="showLock('FOLDER SIGA', 'all', 'folder_siga')">🔓 OPEN SIGA MODULES</button>
            </div>

            <div id="siga-unlocked" style="display: none;">
                <button class="btn-cyber" onclick="processExe('🏥 PELAYANAN KB', 'pelayanan_kb', 'modul')">🏥 PELAYANAN KB</button>
                <button class="btn-cyber" onclick="processExe('👤 DATA PPKBD', 'ppkbd', 'modul')">👤 DATA PPKBD</button>
                <button class="btn-cyber" onclick="processExe('👶 KELOMPOK BKB', 'bkb', 'modul')">👶 KELOMPOK BKB</button>
                <button class="btn-cyber" onclick="processExe('🧑 KELOMPOK BKR', 'bkr', 'modul')">🧑 KELOMPOK BKR</button>
                <button class="btn-cyber" onclick="processExe('👴 KELOMPOK BKL', 'bkl', 'modul')">👴 KELOMPOK BKL</button>
                <button class="btn-cyber" onclick="processExe('👥 KELOMPOK PIK-R', 'pikr', 'modul')">👥 KELOMPOK PIK-R</button>
                <button class="btn-cyber" onclick="processExe('💰 KELOMPOK UPPKA', 'uppka', 'modul')">💰 KELOMPOK UPPKA</button>
                <button class="btn-cyber" style="border-color: #ff4444; color: #ff4444; margin-top: 10px; font-size: 10px; text-align: center;" onclick="lockSiga()">🔒 CLOSE FOLDER</button>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">📺 MEDIA MONITOR</div>
            <div class="visual-box" style="border-color: var(--pink); height: 160px;" id="box-2">
                <video id="video-ads" autoplay muted loop playsinline style="width: 100%; height: 100%; object-fit: cover;">
                    <source src="/static/iklan_bkkbn.mp4" type="video/mp4">
                </video>
                <div class="ads-label" id="txt-2" style="color: var(--pink);">EXCLUSIVE SPONSOR VIDEO</div>
            </div>
            
            <div style="color: var(--green); font-size: 11px; margin-bottom: 10px; text-align: center;">🛒 LOGISTIC CENTER (Cek Promo)</div>
            
            <div class="affiliate-mini">
                <span class="price-tag">KERTAS HVS A4 - RP 45.000</span>
                <button class="btn-cyber" style="border-color: var(--green); padding: 5px; font-size: 10px;" onclick="window.open('https://shope.ee/link_hvs_bapak', '_blank')">🛒 BELI SEKARANG</button>
            </div>

            <div class="affiliate-mini">
                <span class="price-tag">TINTA PRINTER ORIGINAL</span>
                <button class="btn-cyber" style="border-color: var(--green); padding: 5px; font-size: 10px;" onclick="window.open('https://shope.ee/link_tinta_bapak', '_blank')">🛒 CEK HARGA</button>
            </div>

            <button class="btn-cyber btn-pink" style="margin-top: 15px;" onclick="exe('CHANNEL BIMZ', 'youtube.com/@bimz82official50', 'web')">▶ BIMZ82 OFFICIAL</button>
        </div>

        <div class="panel">
            <div class="panel-title">🌐 EXTERNAL HUB</div>
            <div class="visual-box" id="box-3">
                <img id="img-3" src="">
                <div class="ads-label" id="txt-3">PARTNER ADS</div>
            </div>
            <button class="btn-cyber" onclick="exe('E-KINERJA', 'kinerja.bkn.go.id', 'web')">🔗 PORTAL E-KINERJA</button>
            <button class="btn-cyber" onclick="exe('E-VISUM', 'evisum4.bkkbn.go.id', 'web')">🔗 E-VISUM WEB</button>
            <button class="btn-cyber" onclick="exe('NEWSIGA', 'newsiga-siga.bkkbn.go.id', 'web')">🔗 WEB NEWSIGA</button>
            <button class="btn-cyber" onclick="exe('SIMSDM_BKKBN', 'simsdm.bkkbn.go.id', 'web')">🔗 SIMSDM_BKKBN</button>
            <button class="btn-cyber" onclick="exe('GOOGLE', 'google.com', 'web')">🔗 GOOGLE SEARCH</button>
        </div>
    </div>

    <div class="tools-grid">
        <div class="panel" style="border-top-color: #ff0;">
            <div class="panel-title" style="color: #ff0;">🛠️ TOOLS SYSTEM</div>
            <button class="btn-cyber" style="border-color: #ff0;" onclick="exe('🤖 DUPAK', 'DUPAK.exe', 'exe')">🤖 GENERATE DUPAK</button>
        </div>
        <div class="panel" style="border-top-color: #0f0;">
            <div class="panel-title" style="color: #0f0;">📑 PB TOOLS</div>
            <button class="btn-cyber" style="border-color: #0f0;" onclick="exe('📋 SPJ', 'SPJ.exe', 'exe')">📋 TOOLS SPJ</button>
        </div>
    </div>

    <div class="lock-overlay" id="lock-screen">
        <div class="lock-box">
            <div style="color: var(--cyan); font-weight: bold; margin-bottom: 10px;">🔐 ACCESS RESTRICTED</div>
            <p style="font-size: 12px; color: #888;">Fitur ini memerlukan Lisensi Pro.<br>Hubungi Admin: <b>DHEDE_BIMZ</b></p>
            <input type="password" id="access-key" class="lock-input" placeholder="ENTER ACCESS KEY">
            <button class="btn-cyber" onclick="validateKey()">UNLOCK MODULE</button>
            <button class="close-btn" style="border-color: #ff4444; color: #ff4444; margin-top: 10px; padding: 5px 15px;" onclick="hideLock()">CANCEL</button>
        </div>
    </div>

    <div class="footer">
        DEDE BIMZ & RAHMAN &copy; 2026 | SIKEPAL ULTRA WEB-INTERFACE V.2.0
    </div>

    <script>
        function updateClock() {
            const now = new Date();
            document.getElementById('clock').innerText = "TIME: " + now.toLocaleTimeString();
        }
        setInterval(updateClock, 1000);

        const RAW_URL = "https://raw.githubusercontent.com/hamdanisaja007-star/HAMDANI/main/iklan.json";
        const SECRET_KEY = "BIMZ2026"; 
        let daftarIklan = [];
        let currentIndex = 0;
        let currentLockedAction = null;

        async function fetchIklan() {
            try {
                const response = await fetch(RAW_URL + "?nocache=" + new Date().getTime());
                const data = await response.json();
                if (data) {
                    if(data.running_text) document.getElementById('running-text').innerText = data.running_text;
                    if(data.video_url) {
                        const v = document.getElementById('video-ads');
                        if(v.querySelector('source').src !== data.video_url) {
                            v.querySelector('source').src = data.video_url;
                            v.load();
                        }
                    }
                    if (data.iklan_aktif && data.iklan_aktif.length > 0) {
                        daftarIklan = data.iklan_aktif;
                        updateDisplay(0);
                        if (daftarIklan.length > 1) startRotation();
                    }
                }
            } catch (e) { console.error("Sync Error"); }
        }

        function updateDisplay(index) {
            [1, 3].forEach(id => {
                const img = document.getElementById('img-' + id);
                const txt = document.getElementById('txt-' + id);
                if (img && txt && daftarIklan[index]) {
                    img.src = daftarIklan[index].img;
                    txt.innerText = daftarIklan[index].text;
                }
            });
        }

        function startRotation() {
            setInterval(() => {
                currentIndex = (currentIndex + 1) % daftarIklan.length;
                updateDisplay(currentIndex);
            }, 8000);
        }

        function exe(name, target, mode) {
            if (mode === 'modul' || mode === 'exe') {
                showLock(name, target, mode);
            } else {
                processExe(name, target, mode);
            }
        }

        function showLock(name, target, mode) {
            currentLockedAction = {name, target, mode};
            document.getElementById('lock-screen').style.display = 'flex';
            document.getElementById('access-key').value = '';
            document.getElementById('access-key').focus();
        }

        function hideLock() { document.getElementById('lock-screen').style.display = 'none'; }

        function validateKey() {
            const input = document.getElementById('access-key').value;
            if (input === SECRET_KEY) {
                hideLock();
                if (currentLockedAction.mode === 'folder_siga') {
                    document.getElementById('siga-locked').style.display = 'none';
                    document.getElementById('siga-unlocked').style.display = 'block';
                } else {
                    processExe(currentLockedAction.name, currentLockedAction.target, currentLockedAction.mode);
                }
            } else { alert("ACCESS DENIED!"); }
        }

        function lockSiga() {
            document.getElementById('siga-locked').style.display = 'block';
            document.getElementById('siga-unlocked').style.display = 'none';
        }

        function processExe(name, target, mode) {
            fetch('/handler', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: name, target: target, mode: mode})
            })
            .then(res => res.json())
            .then(data => {
                if(data.status === 'redirect') window.location.href = data.url;
            }).catch(err => console.error(err));
        }

        fetchIklan();
    </script>
</body>
</html>
       

@app.route('/')
def main():
    return render_template_string(HTML_FULL)

