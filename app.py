from flask import Flask, render_template_string, jsonify, request
import requests

app = Flask(__name__)

# --- TEMPLATE HTML TETAP SAMA ---
HTML_FULL = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; }
        body { background: var(--dark); color: white; font-family: 'Consolas', monospace; margin: 0; padding: 20px; }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 40px; color: var(--cyan); font-family: 'Impact'; letter-spacing: 5px; }
        .main-grid { display: grid; grid-template-columns: 1fr 320px 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .visual-box { width: 100%; height: 150px; margin-bottom: 15px; border: 1px solid #444; background: #000; overflow: hidden; }
        .visual-box video, .visual-box img { width: 100%; height: 100%; object-fit: cover; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; font-weight: bold; cursor: pointer; text-align: left; transition: 0.3s; }
        .btn-cyber:hover { background: var(--cyan); color: black; box-shadow: 0 0 20px var(--cyan); }
        #login-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: black; z-index: 9999; display: flex; justify-content: center; align-items: center; }
    </style>
</head>
<body>
    <div id="login-overlay">
        <div style="border:2px solid var(--cyan); padding:40px; text-align:center; background:#05050a;">
            <h2 style="color:var(--cyan);">SIKEPAL LOGIN</h2>
            <input type="password" id="pass" style="padding:10px; text-align:center; background:#111; color:white; border:1px solid var(--cyan);" placeholder="ACCESS KEY">
            <button class="btn-cyber" style="margin-top:20px; text-align:center; width:100%;" onclick="checkLogin()">AUTHORIZE SYSTEM</button>
        </div>
    </div>

    <div class="header"><h1>SIKEPAL V.ULTRA</h1></div>

    <div class="main-grid">
        <div class="panel">
            <div style="color:var(--cyan); margin-bottom:15px; font-weight:bold;">📂 MODULE ENTRI SIGA</div>
            <div class="visual-box">
                <img src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan1.jpg">
            </div>
            <button class="btn-cyber" onclick="runRobot('🏥 PELAYANAN KB', 'pelayanan_kb')">🏥 PELAYANAN KB (ROBOT)</button>
            <button class="btn-cyber" onclick="runRobot('👤 DATA PPKBD', 'ppkbd')">👤 DATA PPKBD (ROBOT)</button>
        </div>

        <div class="panel">
            <div style="color:var(--pink); margin-bottom:15px; font-weight:bold;">📺 MONITOR</div>
            <div class="visual-box" style="border-color:var(--pink);">
                <video autoplay muted loop playsinline><source src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan_bkkbn.mp4" type="video/mp4"></video>
            </div>
            <button class="btn-cyber" style="color:var(--pink); border-color:var(--pink);" onclick="window.open('https://youtube.com/@bimz82official50')">▶ BIMZ82 OFFICIAL</button>
        </div>

        <div class="panel">
            <div style="color:var(--cyan); margin-bottom:15px; font-weight:bold;">🌐 EXTERNAL HUB</div>
            <div class="visual-box">
                <img src="https://github.com/hamdanisaja007-star/HAMDANI/raw/main/iklan2.jpg">
            </div>
            <a href="https://kinerja.bkn.go.id" target="_blank" class="btn-cyber" style="text-decoration:none;">🔗 E-KINERJA</a>
            <a href="https://evisum4.bkkbn.go.id" target="_blank" class="btn-cyber" style="text-decoration:none;">🔗 E-VISUM</a>
        </div>
    </div>

    <script>
        function checkLogin() {
            if(document.getElementById('pass').value === 'BIMZ2026') {
                document.getElementById('login-overlay').style.display = 'none';
            } else { alert('ACCESS DENIED'); }
        }

        function runRobot(nama, target) {
            console.log("Memanggil robot...");
            fetch('/handler', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: nama, target: target})
            })
            .then(res => res.json())
            .then(data => {
                alert("Status: " + data.status);
            })
            .catch(err => {
                alert("Gagal terhubung ke laptop!");
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FULL)

# --- BAGIAN PERBAIKAN JEMBATAN KE NGROK ---
@app.route('/handler', methods=['POST'])
def handler():
    data = request.json
    
    # LINK NGROK MAS HAMDANI
    URL_LAPTOP = "https://plastered-nonsubtly-tamera.ngrok-free.dev/jalankan-robot"
    
    try:
        # Kirim sinyal ke laptop Mas
        response = requests.post(URL_LAPTOP, json=data, timeout=5)
        return jsonify({"status": "Robot Berhasil Dipanggil!", "detail": response.json()})
    except:
        return jsonify({"status": "Laptop Offline / Ngrok Mati!"})

# Ini supaya Vercel bisa melihat aplikasinya
app = app

if __name__ == "__main__":
    app.run(debug=True)

