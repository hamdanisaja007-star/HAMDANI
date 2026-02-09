from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- 1. HALAMAN LOGIN (Ganteng & Futuristik) ---
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
        .login-box { width: 380px; padding: 40px; background: rgba(5, 5, 10, 0.9); border-top: 4px solid var(--cyan); border: 1px solid var(--cyan); box-shadow: 0 0 30px var(--cyan); text-align: center; }
        .login-box h2 { color: var(--cyan); letter-spacing: 5px; margin: 0; font-family: 'Impact'; font-size: 35px; text-shadow: 0 0 10px var(--cyan); }
        .input-group { margin: 30px 0; }
        .input-group input { width: 100%; padding: 15px; background: rgba(0, 240, 255, 0.1); border: 1px solid var(--cyan); color: var(--cyan); font-size: 20px; text-align: center; outline: none; box-sizing: border-box; }
        .btn-login { width: 100%; padding: 15px; background: var(--cyan); border: none; color: black; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; text-transform: uppercase; }
        .btn-login:hover { background: white; box-shadow: 0 0 25px var(--cyan); letter-spacing: 2px; }
        .footer-tag { position: absolute; bottom: 20px; color: #555; font-size: 12px; width: 100%; text-align: center; }
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
            <div id="msg" style="margin-top: 15px; font-size: 12px; color: #444; text-transform: uppercase;">AWAITING COMMAND...</div>
        </div>
    </div>
    <div class="footer-tag">DEDE BIMZ & RAHMAN © 2026 | STATION: CIKEMBAR_CORE_0210</div>
    <script>
        function checkAuth() {
            const pass = document.getElementById('pass').value;
            const msg = document.getElementById('msg');
            if (pass === "BIMZ2026") {
                msg.style.color = "#0f0";
                msg.innerText = "ACCESS GRANTED. SYNCING DATA...";
                setTimeout(() => { window.location.href = "/dashboard"; }, 1500);
            } else {
                msg.style.color = "#f00";
                msg.innerText = "INVALID ACCESS KEY!";
            }
        }
        document.getElementById('pass').addEventListener('keypress', function(e){ if(e.key === 'Enter') checkAuth(); });
    </script>
</body>
</html>
"""

# --- 2. HALAMAN DASHBOARD (Full Menu SIKEPAL) ---
dashboard_html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL - MAIN DASHBOARD</title>
    <style>
        :root { --neon: #00f0ff; --darker: #05050a; }
        body { margin: 0; background: var(--darker); color: white; font-family: 'Segoe UI', sans-serif; }
        nav { background: rgba(0,0,0,0.8); padding: 15px 40px; border-bottom: 2px solid var(--neon); display: flex; justify-content: space-between; align-items: center; }
        .logo { color: var(--neon); font-weight: bold; font-size: 24px; letter-spacing: 3px; }
        .container { padding: 40px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .card { background: rgba(0, 240, 255, 0.05); border: 1px solid #111; padding: 25px; text-align: center; transition: 0.3s; cursor: pointer; border-radius: 5px; }
        .card:hover { border-color: var(--neon); background: rgba(0, 240, 255, 0.1); transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 240, 255, 0.2); }
        .card i { font-size: 40px; color: var(--neon); margin-bottom: 15px; display: block; }
        .card h3 { margin: 10px 0; font-size: 18px; color: #fff; }
        .card p { font-size: 12px; color: #888; }
        .btn-logout { background: #f00; color: white; padding: 8px 15px; text-decoration: none; font-size: 12px; border-radius: 3px; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">SIKEPAL V.ULTRA</div>
        <a href="/" class="btn-logout">LOGOUT SYSTEM</a>
    </nav>
    <div style="padding: 40px 40px 0 40px;">
        <h1 style="margin: 0;">SELAMAT DATANG, KOMANDAN</h1>
        <p style="color: var(--neon);">SISTEM INFORMASI KELUARGA & PELAYANAN LAPORAN</p>
    </div>
    <div class="container">
        <div class="card" onclick="alert('Membuka Modul BKB...')">
            <h3>MODUL BKB</h3>
            <p>Bina Keluarga Balita</p>
        </div>
        <div class="card" onclick="alert('Membuka Modul BKR...')">
            <h3>MODUL BKR</h3>
            <p>Bina Keluarga Remaja</p>
        </div>
        <div class="card" onclick="alert('Membuka Modul BKL...')">
            <h3>MODUL BKL</h3>
            <p>Bina Keluarga Lansia</p>
        </div>
        <div class="card" onclick="alert('Membuka Modul UPPKA...')">
            <h3>MODUL UPPKA</h3>
            <p>Usaha Peningkatan Pendapatan Keluarga</p>
        </div>
        <div class="card" onclick="alert('Membuka Pelaporan SIGA...')">
            <h3>LAPORAN SIGA</h3>
            <p>Sinkronisasi Data Lapangan</p>
        </div>
        <div class="card" onclick="alert('Membuka Database...')">
            <h3>DATABASE</h3>
            <p>Penyimpanan Data Cikembar</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(login_html)

@app.route('/dashboard')
def dashboard():
    return render_template_string(dashboard_html)

if __name__ == '__main__':
    app.run()
