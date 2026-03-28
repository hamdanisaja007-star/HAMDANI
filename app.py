import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sidallap_sukabumi_2026_secure"

# --- KONFIGURASI (Vercel & Local) ---
BASE_TMP = "/tmp"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_TMP, "sidalap_v2.db")}'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_TMP, 'loker_berkas')
app.config['CHAT_UPLOAD'] = os.path.join(BASE_TMP, 'chat_files')
app.config['PROFIL_UPLOAD'] = os.path.join(BASE_TMP, 'foto_profil')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pastikan semua folder siap
for folder in [app.config['UPLOAD_FOLDER'], app.config['CHAT_UPLOAD'], app.config['PROFIL_UPLOAD']]:
    os.makedirs(folder, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# --- MODELS ---
class Pegawai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100))
    jenis_pegawai = db.Column(db.String(10)) # PNS / PPPK
    pangkat_gol = db.Column(db.String(50))
    kecamatan = db.Column(db.String(50))
    desa_binaan = db.Column(db.String(200))
    no_hp = db.Column(db.String(20))
    tmt_pangkat = db.Column(db.Date) # Format: YYYY-MM-DD
    tgl_lahir = db.Column(db.Date)   # Format: YYYY-MM-DD
    foto = db.Column(db.String(200), default='default_user.png')

class Pengumuman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    file_lampiran = db.Column(db.String(200))
    tanggal = db.Column(db.DateTime, default=datetime.now)

class LogBaca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengumuman_id = db.Column(db.Integer, db.ForeignKey('pengumuman.id'))
    nip_pembaca = db.Column(db.String(20))
    nama_pembaca = db.Column(db.String(100))
    waktu_baca = db.Column(db.DateTime, default=datetime.now)

# --- MIDDLEWARE ---
@app.context_processor
def inject_user():
    user_data = None
    if 'user_nip' in session:
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
    return dict(user_now=user_data)

# --- ROUTES ---
@app.route('/')
def landing():
    if 'user_role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    u, p = request.form.get('username'), request.form.get('password')
    if u == "admin" and p == "admin123":
        session.clear()
        session['user_role'] = 'admin'
        session['user_nip'] = 'ADMIN'
        return redirect(url_for('dashboard'))
    
    user = Pegawai.query.filter_by(nip=u).first()
    if user: # Password sementara pakai NIP juga agar mudah
        session.clear()
        session['user_role'] = 'plkb'
        session['user_nip'] = u
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    
    flash("NIP atau Password salah!", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    pegawai = Pegawai.query.all()
    
    notif_pangkat, notif_pensiun = [], []
    today = date.today()
    
    if role == 'admin':
        for p in pegawai:
            # Notif Pangkat: Jika sudah 4 tahun (1460 hari) dari TMT
            if p.jenis_pegawai == 'PNS' and p.tmt_pangkat:
                diff_years = (today.year - p.tmt_pangkat.year)
                if diff_years >= 4: notif_pangkat.append(p)
            
            # Notif Pensiun: Jika umur sudah 58 tahun
            if p.tgl_lahir:
                age = today.year - p.tgl_lahir.year
                if age >= 57: # Munculkan peringatan sejak umur 57
                    notif_pensiun.append(p)

    return render_template('index.html', pegawai=pegawai, role=role, 
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun)

@app.route('/data_pegawai', methods=['GET', 'POST'])
def data_pegawai():
    if session.get('user_role') != 'admin': return redirect(url_for('landing'))
    if request.method == 'POST':
        nip = request.form.get('nip')
        nama = request.form.get('nama')
        if not Pegawai.query.filter_by(nip=nip).first():
            new_p = Pegawai(nip=nip, nama=nama, jenis_pegawai=request.form.get('jenis_pegawai'))
            db.session.add(new_p)
            db.session.commit()
            flash(f"Pegawai {nama} berhasil didaftarkan!", "success")
        else:
            flash("NIP sudah terdaftar!", "warning")
    
    pegawai = Pegawai.query.all()
    return render_template('data_pegawai.html', pegawai=pegawai)

# --- FITUR INPUT MANDIRI PLKB ---
@app.route('/profil')
def profil():
    if 'user_role' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    return render_template('profil.html', user_now=user)

@app.route('/update_profil', methods=['POST'])
def update_profil():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    if user:
        user.jabatan = request.form.get('jabatan')
        user.pangkat_gol = request.form.get('pangkat_gol')
        user.kecamatan = request.form.get('kecamatan')
        user.desa_binaan = request.form.get('desa_binaan')
        
        # Konversi String Tanggal dari Form ke Object Date Python
        tmt = request.form.get('tmt_pangkat')
        tgl = request.form.get('tgl_lahir')
        if tmt: user.tmt_pangkat = datetime.strptime(tmt, '%Y-%m-%d').date()
        if tgl: user.tgl_lahir = datetime.strptime(tgl, '%Y-%m-%d').date()

        # Fitur Upload Foto
        file_foto = request.files.get('foto_profil')
        if file_foto and allowed_file(file_foto.filename):
            ext = file_foto.filename.rsplit('.', 1)[1].lower()
            fname = f"foto_{user.nip}.{ext}"
            file_foto.save(os.path.join(app.config['PROFIL_UPLOAD'], fname))
            user.foto = fname

        db.session.commit()
        flash("Profil Anda Berhasil Diperbarui!", "success")
    return redirect(url_for('profil'))

@app.route('/foto_profil/<filename>')
def serve_foto(filename):
    return send_from_directory(app.config['PROFIL_UPLOAD'], filename)

@app.route('/hapus_pegawai/<int:id>')
def hapus_pegawai(id):
    if session.get('user_role') == 'admin':
        p = Pegawai.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
            flash("Data Terhapus!", "info")
    return redirect(url_for('data_pegawai'))

# --- FITUR BERKAS & CHAT ---
@app.route('/berkas_saya')
def berkas_saya():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session['user_nip']).first()
    path_user = os.path.join(app.config['UPLOAD_FOLDER'], user.nip)
    os.makedirs(path_user, exist_ok=True)
    files = os.listdir(path_user)
    return render_template('upload_plkb.html', files=files)

@app.route('/simpan_berkas', methods=['POST'])
def simpan_berkas():
    user_nip = session.get('user_nip')
    file = request.files.get('file_berkas')
    kat = request.form.get('kategori')
    if file and user_nip:
        fname = f"{kat}_{datetime.now().strftime('%Y%m%d%H%M')}_{secure_filename(file.filename)}"
        target = os.path.join(app.config['UPLOAD_FOLDER'], user_nip)
        os.makedirs(target, exist_ok=True)
        file.save(os.path.join(target, fname))
        flash("Berkas Berhasil Terkirim!", "success")
    return redirect(url_for('berkas_saya'))

@app.route('/admin/berkas_masuk')
def berkas_masuk():
    if session.get('user_role') != 'admin': return redirect(url_for('dashboard'))
    list_masuk = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for nip in os.listdir(app.config['UPLOAD_FOLDER']):
            p = Pegawai.query.filter_by(nip=nip).first()
            p_path = os.path.join(app.config['UPLOAD_FOLDER'], nip)
            if os.path.isdir(p_path):
                for f in os.listdir(p_path):
                    list_masuk.append({'nama': p.nama if p else nip, 'nip': nip, 'file': f, 'kat': f.split('_')[0]})
    return render_template('admin_berkas.html', data=list_masuk)

@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    logs = {i.id: LogBaca.query.filter_by(pengumuman_id=i.id).all() for i in info} if role == 'admin' else {}
    return render_template('chat_info.html', info_terkini=info, logs=logs, role=role)

@app.route('/kirim_info', methods=['POST'])
def kirim_info():
    if session.get('user_role') == 'admin':
        pesan, file = request.form.get('isi'), request.files.get('lampiran')
        fname = None
        if file and file.filename != '':
            fname = secure_filename(file.filename)
            file.save(os.path.join(app.config['CHAT_UPLOAD'], fname))
        db.session.add(Pengumuman(isi=pesan, file_lampiran=fname))
        db.session.commit()
    return redirect(url_for('chat_info'))

@app.route('/download/<nip>/<filename>')
def download_file(nip, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], nip), filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
