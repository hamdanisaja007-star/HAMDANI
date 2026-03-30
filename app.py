import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sidallap_sukabumi_2026_secure"

# --- KONFIGURASI (Vercel & Local) ---
BASE_TMP = "/tmp"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_TMP, "sidalap_v3.db")}'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_TMP, 'loker_berkas')
app.config['CHAT_UPLOAD'] = os.path.join(BASE_TMP, 'chat_files')
app.config['PROFIL_UPLOAD'] = os.path.join(BASE_TMP, 'foto_profil')
app.config['PRODUK_UPLOAD'] = os.path.join(BASE_TMP, 'produk_foto')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pastikan folder sistem siap di /tmp
for folder in [app.config['UPLOAD_FOLDER'], app.config['CHAT_UPLOAD'], app.config['PROFIL_UPLOAD'], app.config['PRODUK_UPLOAD']]:
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
    jenis_pegawai = db.Column(db.String(10)) 
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

class PesanChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    nama_pengirim = db.Column(db.String(100))
    role = db.Column(db.String(10)) 
    isi_pesan = db.Column(db.Text, nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

class Produk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.String(50))
    deskripsi = db.Column(db.Text)
    foto_produk = db.Column(db.String(200))
    penjual_id = db.Column(db.Integer)
    nama_penjual = db.Column(db.String(100))
    wa_penjual = db.Column(db.String(20))
    tanggal_post = db.Column(db.DateTime, default=datetime.now)

# --- MIDDLEWARE ---
@app.context_processor
def inject_user():
    user_data = None
    if 'user_nip' in session and session['user_nip'] != 'ADMIN':
        user_data = Pegawai.query.filter_by(nip=session['user_nip']).first()
    return dict(user_now=user_data)

# --- ROUTES AUTH ---
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
        session.update({'user_role': 'admin', 'user_nip': 'ADMIN', 'user_id': 0})
        return redirect(url_for('dashboard'))
    user = Pegawai.query.filter_by(nip=u).first()
    if user and p == user.nip:
        session.clear()
        session.update({'user_role': 'plkb', 'user_nip': user.nip, 'user_id': user.id})
        return redirect(url_for('dashboard'))
    flash("NIP atau Password salah!", "danger")
    return redirect(url_for('landing'))

# --- DASHBOARD (KEMBALI KE ASLI + FIX PROTEKSI) ---
@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    
    # Ambil data pegawai
    if role == 'admin':
        pegawai_list = Pegawai.query.all()
    else:
        # Jika PLKB, hanya ambil data dirinya sendiri
        user_self = Pegawai.query.filter_by(nip=session['user_nip']).first()
        pegawai_list = [user_self] if user_self else []

    notif_pangkat, notif_pensiun = [], []
    today = date.today()
    
    # Statistik selalu tampil untuk Admin
    stat = {
        'total': Pegawai.query.count(),
        'pns': Pegawai.query.filter_by(jenis_pegawai='PNS').count(),
        'pppk': Pegawai.query.filter_by(jenis_pegawai='PPPK').count()
    }
    
    # Notifikasi Pangkat & Pensiun HANYA untuk Admin
    if role == 'admin':
        all_pegawai = Pegawai.query.all()
        for p in all_pegawai:
            if p.tmt_pangkat and (today.year - p.tmt_pangkat.year) >= 4: notif_pangkat.append(p)
            if p.tgl_lahir and (today.year - p.tgl_lahir.year) >= 57: notif_pensiun.append(p)
            
    return render_template('index.html', pegawai=pegawai_list, role=role, 
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun, stat=stat)

# --- LOKER BERKAS ---
@app.route('/upload_berkas')
def upload_berkas():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    nip = session['user_nip']
    target_dir = os.path.join(app.config['UPLOAD_FOLDER'], nip)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    user_files = os.listdir(target_dir)
    return render_template('upload.html', files=user_files)

@app.route('/simpan_berkas', methods=['POST'])
def simpan_berkas():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    file = request.files.get('file_berkas')
    kat = request.form.get('kategori', 'LAINNYA').upper()
    nip = session['user_nip']
    if file and file.filename != '' and allowed_file(file.filename):
        target_dir = os.path.join(app.config['UPLOAD_FOLDER'], nip)
        os.makedirs(target_dir, exist_ok=True)
        fname = f"{kat}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
        file.save(os.path.join(target_dir, fname))
        flash(f"Berkas {kat} Berhasil dikirim!", "success")
    else:
        flash("Gagal! Pastikan file dipilih dan formatnya PDF/JPG/PNG.", "danger")
    return redirect(url_for('upload_berkas'))

# --- ADMIN BERKAS MASUK (FIX ERROR 500) ---
@app.route('/admin/berkas_masuk')
def berkas_masuk():
    if session.get('user_role') != 'admin': return redirect(url_for('dashboard'))
    list_masuk = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        try:
            for nip_f in os.listdir(app.config['UPLOAD_FOLDER']):
                path = os.path.join(app.config['UPLOAD_FOLDER'], nip_f)
                if os.path.isdir(path):
                    p = Pegawai.query.filter_by(nip=nip_f).first()
                    files = os.listdir(path)
                    for fn in files:
                        list_masuk.append({
                            'nama': p.nama if p else nip_f, 
                            'nip': nip_f, 
                            'file': fn, 
                            'kat': fn.split('_')[0]
                        })
        except:
            pass
    return render_template('admin_berkas.html', data=list_masuk)

# --- DATA PEGAWAI (ADMIN) ---
@app.route('/data_pegawai', methods=['GET', 'POST'])
def data_pegawai():
    if session.get('user_role') != 'admin': return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nip = request.form.get('nip')
        nama = request.form.get('nama')
        jenis = request.form.get('jenis_pegawai')
        db.session.add(Pegawai(nip=nip, nama=nama, jenis_pegawai=jenis))
        db.session.commit()
        flash("Data pegawai berhasil ditambahkan!", "success")
    return render_template('data_pegawai.html', pegawai=Pegawai.query.all())

# --- PROFIL ---
@app.route('/profil')
def profil():
    if 'user_nip' not in session: return redirect(url_for('landing'))
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    return render_template('profil.html', user_now=user)

@app.route('/update_profil', methods=['POST'])
def update_profil():
    user = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    if user:
        user.jabatan = request.form.get('jabatan')
        user.no_hp = request.form.get('no_hp')
        user.kecamatan = request.form.get('kecamatan')
        file_foto = request.files.get('foto_profil')
        if file_foto and allowed_file(file_foto.filename):
            fname = f"foto_{user.nip}.jpg"
            file_foto.save(os.path.join(app.config['PROFIL_UPLOAD'], fname))
            user.foto = fname
        db.session.commit()
        flash("Profil berhasil diperbarui!", "success")
    return redirect(url_for('profil'))

# --- TOKO & CHAT TETAP SAMA ---
@app.route('/toko')
def toko():
    if 'user_role' not in session: return redirect(url_for('landing'))
    semua_produk = Produk.query.order_by(Produk.tanggal_post.desc()).all()
    return render_template('toko.html', produk=semua_produk, role=session.get('user_role'))

@app.route('/tambah_produk', methods=['POST'])
def tambah_produk():
    if 'user_role' not in session: return redirect(url_for('landing'))
    nama = request.form.get('nama_barang')
    harga = request.form.get('harga')
    wa = request.form.get('wa_penjual')
    deskripsi = request.form.get('deskripsi')
    file = request.files.get('foto_produk')
    fname = "default_produk.png"
    if file and allowed_file(file.filename):
        fname = f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['PRODUK_UPLOAD'], fname))
    user_now = Pegawai.query.filter_by(nip=session.get('user_nip')).first()
    baru = Produk(nama_barang=nama, harga=harga, wa_penjual=wa, deskripsi=deskripsi, 
                  foto_produk=fname, nama_penjual=user_now.nama if user_now else "ADMIN", penjual_id=session.get('user_id'))
    db.session.add(baru)
    db.session.commit()
    return redirect(url_for('toko'))

@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    msg = PesanChat.query.order_by(PesanChat.waktu.asc()).all()
    return render_template('chat_info.html', info_terkini=info, role=session['user_role'], all_messages=msg)

@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    user = Pegawai.query.get(session.get('user_id')) if session.get('user_role') != 'admin' else None
    db.session.add(PesanChat(user_id=session.get('user_id'), nama_pengirim=user.nama if user else "ADMIN", role=session.get('user_role'), isi_pesan=request.form.get('pesan')))
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
