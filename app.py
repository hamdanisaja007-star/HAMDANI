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
    tmt_pangkat = db.Column(db.Date)
    tgl_lahir = db.Column(db.Date)
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

# MODEL BARU: Untuk Chat Dua Arah
class PesanChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) # ID Pengirim
    nama_pengirim = db.Column(db.String(100))
    role = db.Column(db.String(10)) # 'admin' atau 'user'
    isi_pesan = db.Column(db.Text, nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

# --- MIDDLEWARE ---
@app.context_processor
def inject_user():
    user_data = None
    if 'user_nip' in session and session['user_nip'] != 'ADMIN':
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
    return dict(user_now=user_data)

# --- ROUTES ---
@app.route('/')
def landing():
    if 'user_role' in session: return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def auth():
    u = request.form.get('username', '').strip()
    p = request.form.get('password', '').strip()

    if u == "admin" and p == "admin123":
        session.clear()
        session['user_role'] = 'admin'
        session['user_nip'] = 'ADMIN'
        session['user_id'] = 0 # ID khusus admin
        return redirect(url_for('dashboard'))
    
    user = Pegawai.query.filter_by(nip=u).first()
    if user and p == user.nip:
        session.clear()
        session['user_role'] = 'plkb'
        session['user_nip'] = user.nip
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    
    flash("NIP atau Password salah!", "danger")
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    notif_pangkat, notif_pensiun = [], []
    today = date.today()
    pegawai_list = Pegawai.query.all()
    
    if role == 'admin':
        for p in pegawai_list:
            if p.tmt_pangkat:
                diff = (today.year - p.tmt_pangkat.year)
                if diff >= 4: notif_pangkat.append(p)
            if p.tgl_lahir:
                age = today.year - p.tgl_lahir.year
                if age >= 57: notif_pensiun.append(p)

    return render_template('index.html', pegawai=pegawai_list, role=role, 
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun)

# --- FITUR CHAT & INFO (DIPERBARUI) ---
@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    
    # Ambil Pengumuman Resmi
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    
    # Ambil Percakapan Chat (Batas 50 pesan terakhir)
    all_messages = PesanChat.query.order_by(PesanChat.waktu.asc()).all()

    # Logika Log Baca untuk Admin
    if role != 'admin':
        user = Pegawai.query.filter_by(nip=session['user_nip']).first()
        for i in info:
            if not LogBaca.query.filter_by(pengumuman_id=i.id, nip_pembaca=user.nip).first():
                db.session.add(LogBaca(pengumuman_id=i.id, nip_pembaca=user.nip, nama_pembaca=user.nama))
        db.session.commit()
    
    logs = {i.id: LogBaca.query.filter_by(pengumuman_id=i.id).all() for i in info} if role == 'admin' else {}
    
    return render_template('chat_info.html', info_terkini=info, logs=logs, role=role, all_messages=all_messages)

@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    if 'user_role' not in session: return redirect(url_for('landing'))
    
    isi = request.form.get('pesan')
    role = session.get('user_role')
    user_id = session.get('user_id')
    
    # Cari nama pengirim
    if role == 'admin':
        nama = "ADMIN SIDALAP"
    else:
        user = Pegawai.query.get(user_id)
        nama = user.nama if user else "PLKB"

    if isi:
        baru = PesanChat(user_id=user_id, nama_pengirim=nama, role=role, isi_pesan=isi)
        db.session.add(baru)
        db.session.commit()
    
    return redirect(url_for('chat_info'))

@app.route('/kirim_info', methods=['POST'])
def kirim_info():
    if session.get('user_role') == 'admin':
        pesan, file = request.form.get('isi'), request.files.get('lampiran')
        fname = secure_filename(file.filename) if file and file.filename != '' else None
        if fname: file.save(os.path.join(app.config['CHAT_UPLOAD'], fname))
        db.session.add(Pengumuman(isi=pesan, file_lampiran=fname))
        db.session.commit()
        flash("Pengumuman berhasil disebarkan!", "success")
    return redirect(url_for('chat_info'))

# --- FUNGSI LAINNYA (PROFIL, BERKAS, DLL TETAP SAMA) ---
@app.route('/data_pegawai', methods=['GET', 'POST'])
def data_pegawai():
    if session.get('user_role') != 'admin': return redirect(url_for('landing'))
    if request.method == 'POST':
        nip = request.form.get('nip', '').strip()
        nama = request.form.get('nama')
        jenis = request.form.get('jenis_pegawai')
        if not Pegawai.query.filter_by(nip=nip).first():
            new_p = Pegawai(nip=nip, nama=nama, jenis_pegawai=jenis)
            db.session.add(new_p)
            db.session.commit()
            flash(f"PLKB {nama} berhasil didaftarkan!", "success")
        else:
            flash(f"NIP {nip} sudah ada!", "warning")
    pegawai = Pegawai.query.all()
    return render_template('data_pegawai.html', pegawai=pegawai)

@app.route('/profil')
def profil():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    return render_template('profil.html', user_now=user)

@app.route('/update_profil', methods=['POST'])
def update_profil():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    if user:
        try:
            user.jabatan = request.form.get('jabatan')
            user.pangkat_gol = request.form.get('pangkat_gol')
            user.kecamatan = request.form.get('kecamatan')
            user.desa_binaan = request.form.get('desa_binaan')
            user.no_hp = request.form.get('no_hp')
            tmt, tgl = request.form.get('tmt_pangkat'), request.form.get('tgl_lahir')
            if tmt: user.tmt_pangkat = datetime.strptime(tmt, '%Y-%m-%d').date()
            if tgl: user.tgl_lahir = datetime.strptime(tgl, '%Y-%m-%d').date()

            file_foto = request.files.get('foto_profil')
            if file_foto and allowed_file(file_foto.filename):
                ext = file_foto.filename.rsplit('.', 1)[1].lower()
                fname = f"foto_{user.nip}_{datetime.now().strftime('%M%S')}.{ext}"
                file_foto.save(os.path.join(app.config['PROFIL_UPLOAD'], fname))
                user.foto = fname
            db.session.commit()
            flash("Profil Berhasil Diperbarui!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Gagal update: {str(e)}", "danger")
    return redirect(url_for('profil'))

@app.route('/foto_profil/<filename>')
def serve_foto(filename):
    return send_from_directory(app.config['PROFIL_UPLOAD'], filename)

@app.route('/upload_berkas')
def berkas_saya():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session['user_nip']).first()
    path_user = os.path.join(app.config['UPLOAD_FOLDER'], user.nip)
    os.makedirs(path_user, exist_ok=True)
    files = os.listdir(path_user)
    return render_template('upload_plkb.html', files=files, user_now=user)

@app.route('/simpan_berkas', methods=['POST'])
def simpan_berkas():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user_nip = session.get('user_nip')
    file = request.files.get('file_berkas')
    kat = request.form.get('kategori')
    if file and file.filename != '':
        fname = f"{kat}_{user_nip}_{datetime.now().strftime('%Y%m%d%H%M')}_{secure_filename(file.filename)}"
        target = os.path.join(app.config['UPLOAD_FOLDER'], user_nip)
        os.makedirs(target, exist_ok=True)
        file.save(os.path.join(target, fname))
        flash(f"Berkas {kat} Berhasil Terkirim!", "success")
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

@app.route('/buka_berkas/<nip>/<filename>')
def download_file(nip, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], nip), filename)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/hapus_pegawai/<int:id>')
def hapus_pegawai(id):
    if session.get('user_role') == 'admin':
        p = Pegawai.query.get(id)
        if p:
            db.session.delete(p); db.session.commit()
            flash("Data Terhapus!", "info")
    return redirect(url_for('data_pegawai'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
