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
app.config['PRODUK_UPLOAD'] = os.path.join(BASE_TMP, 'produk_foto')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Pastikan semua folder siap
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

class PesanChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    nama_pengirim = db.Column(db.String(100))
    role = db.Column(db.String(10)) 
    isi_pesan = db.Column(db.Text, nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)

# MODEL BARU: SIDALAP MART
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
        session['user_role'] = 'admin'
        session['user_nip'] = 'ADMIN'
        session['user_id'] = 0
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

# --- DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    notif_pangkat, notif_pensiun = [], []
    today = date.today()
    pegawai_list = Pegawai.query.all()
    
    # Hitung Statistik untuk Admin
    stat = {
        'total': len(pegawai_list),
        'pns': Pegawai.query.filter_by(jenis_pegawai='PNS').count(),
        'pppk': Pegawai.query.filter_by(jenis_pegawai='PPPK').count()
    }

    if role == 'admin':
        for p in pegawai_list:
            if p.tmt_pangkat:
                if (today.year - p.tmt_pangkat.year) >= 4: notif_pangkat.append(p)
            if p.tgl_lahir:
                if (today.year - p.tgl_lahir.year) >= 57: notif_pensiun.append(p)

    return render_template('index.html', pegawai=pegawai_list, role=role, 
                           notif_pangkat=notif_pangkat, notif_pensiun=notif_pensiun, stat=stat)

# --- FITUR BERKAS MASUK (ADMIN ONLY) ---
@app.route('/admin/berkas_masuk')
def berkas_masuk():
    if session.get('user_role') != 'admin':
        return redirect(url_for('dashboard'))
    
    list_masuk = []
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for nip_folder in os.listdir(app.config['UPLOAD_FOLDER']):
            p = Pegawai.query.filter_by(nip=nip_folder).first()
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], nip_folder)
            
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    list_masuk.append({
                        'nama': p.nama if p else "User Tidak Dikenal",
                        'nip': nip_folder,
                        'file': file_name,
                        'kategori': file_name.split('_')[0] if '_' in file_name else "Lainnya"
                    })
    return render_template('admin_berkas.html', data=list_masuk)

# --- FITUR TOKO (SIDALAP MART) ---
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
    desc = request.form.get('deskripsi')
    file = request.files.get('foto')
    
    # Ambil info penjual dari session
    user = Pegawai.query.get(session.get('user_id')) if session.get('user_role') != 'admin' else None
    
    fname = "default_item.png"
    if file and allowed_file(file.filename):
        fname = f"item_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['PRODUK_UPLOAD'], fname))

    baru = Produk(
        nama_barang=nama,
        harga=harga,
        deskripsi=desc,
        foto_produk=fname,
        penjual_id=session.get('user_id'),
        nama_penjual=user.nama if user else "ADMIN",
        wa_penjual=user.no_hp if user else "62812345678"
    )
    db.session.add(baru)
    db.session.commit()
    flash("Produk berhasil diposting di SIDALAP Mart!", "success")
    return redirect(url_for('toko'))

@app.route('/hapus_produk/<int:id>')
def hapus_produk(id):
    p = Produk.query.get(id)
    if p and (session.get('user_role') == 'admin' or p.penjual_id == session.get('user_id')):
        db.session.delete(p)
        db.session.commit()
        flash("Produk berhasil dihapus!", "info")
    return redirect(url_for('toko'))

@app.route('/produk_foto/<filename>')
def serve_produk(filename):
    return send_from_directory(app.config['PRODUK_UPLOAD'], filename)

# --- KOMUNIKASI ---
@app.route('/chat_info')
def chat_info():
    if 'user_role' not in session: return redirect(url_for('landing'))
    role = session['user_role']
    info = Pengumuman.query.order_by(Pengumuman.tanggal.desc()).all()
    all_messages = PesanChat.query.order_by(PesanChat.waktu.asc()).all()

    if role != 'admin':
        user = Pegawai.query.get(session['user_id'])
        for i in info:
            if not LogBaca.query.filter_by(pengumuman_id=i.id, nip_pembaca=user.nip).first():
                db.session.add(LogBaca(pengumuman_id=i.id, nip_pembaca=user.nip, nama_pembaca=user.nama))
        db.session.commit()
    
    logs = {i.id: LogBaca.query.filter_by(pengumuman_id=i.id).all() for i in info} if role == 'admin' else {}
    return render_template('chat_info.html', info_terkini=info, logs=logs, role=role, all_messages=all_messages)

@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    isi = request.form.get('pesan')
    if isi:
        user = Pegawai.query.get(session.get('user_id')) if session.get('user_role') != 'admin' else None
        nama = "ADMIN SIDALAP" if session.get('user_role') == 'admin' else user.nama
        baru = PesanChat(user_id=session.get('user_id'), nama_pengirim=nama, role=session.get('user_role'), isi_pesan=isi)
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
    return redirect(url_for('chat_info'))

# --- DATA PEGAWAI ---
@app.route('/data_pegawai', methods=['GET', 'POST'])
def data_pegawai():
    if session.get('user_role') != 'admin': return redirect(url_for('landing'))
    if request.method == 'POST':
        nip = request.form.get('nip', '').strip()
        nama = request.form.get('nama')
        if not Pegawai.query.filter_by(nip=nip).first():
            db.session.add(Pegawai(nip=nip, nama=nama, jenis_pegawai=request.form.get('jenis_pegawai')))
            db.session.commit()
            flash(f"PLKB {nama} Terdaftar!", "success")
    pegawai = Pegawai.query.all()
    return render_template('data_pegawai.html', pegawai=pegawai)

# --- PROFIL & BERKAS ---
@app.route('/profil')
def profil():
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
        flash("Profil Update!", "success")
    return redirect(url_for('profil'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
