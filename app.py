from flask import Flask, render_template_string

app = Flask(__name__)

# --- TAMPILAN DASHBOARD MAS HAMDANI ---
# Saya masukkan kode asli Mas Hamdani di sini
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>SIKEPAL V.ULTRA - COMMAND CENTER</title>
    <style>
        :root { --cyan: #00f0ff; --pink: #ff00ff; --dark: #020205; --green: #0f0; }
        body {
            background: var(--dark); color: white; font-family: 'Consolas', monospace;
            margin: 0; padding: 20px;
            background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
            background-size: 30px 30px;
        }
        .header { border: 2px solid var(--cyan); padding: 15px; text-align: center; box-shadow: 0 0 20px var(--cyan); margin-bottom: 20px; background: rgba(0,0,0,0.9); }
        .header h1 { margin: 0; font-size: 40px; color: var(--cyan); text-shadow: 0 0 15px var(--cyan); font-family: 'Impact'; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
        .panel { background: rgba(5, 5, 10, 0.95); border: 1px solid #333; border-top: 4px solid var(--cyan); padding: 20px; }
        .btn-cyber { display: block; width: 100%; padding: 12px; margin-bottom: 8px; background: rgba(0, 240, 255, 0.05); border: 1px solid var(--cyan); color: white; cursor: pointer; text-align: left; text-decoration: none; font-size: 13px; box-sizing: border-box; }
        .btn-cyber:hover { background: var(--cyan); color: black; }
        .ticker { background: rgba(255, 0, 255, 0.1); color: var(--pink); padding: 10px; border: 1px solid var(--pink); margin-bottom: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SIKEPAL V.ULTRA</h1>
        <div style="font-size: 13px; color: var(--pink);">STATION: CIKEMBAR_CORE_0210</div>
    </div>
    <div class="ticker">● SYSTEM ONLINE - READY TO ACCESS MODULES</div>
    <div class="main-grid">
        <div class="panel">
            <h3 style="color:var(--cyan)">📂 MODULE SIGA</h3>
            <a href="https://newsiga-siga.bkkbn.go.id" target="_blank" class="btn-cyber">🏥 PELAYANAN KB</a>
            <a href="#" class="btn-cyber">👤 DATA PPKBD</a>
            <a href="#" class="btn-cyber">👶 KELOMPOK BKB</a>
        </div>
        <div class="panel">
            <h3 style="color:var(--pink)">📺 MONITOR</h3>
            <div style="height:120px; background:black; border:1px solid var(--pink); display:flex; align-items:center; justify-content:center; color:var(--pink);">
                [ STREAM ACTIVE ]
            </div>
        </div>
        <div class="panel">
            <h3 style="color:var(--cyan)">🌐 HUB</h3>
            <a href="https://kinerja.bkn.go.id" target="_blank" class="btn-cyber">🔗 E-KINERJA</a>
            <a href="https://evisum4.bkkbn.go.id" target="_blank" class="btn-cyber">🔗 E-VISUM</a>
            <a href="https://google.com" target="_blank" class="btn-cyber">🔗 GOOGLE</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML)

# Hapus route lain untuk sementara agar tidak crash
