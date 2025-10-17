from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, flash
import json
import sqlite3
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

# Flask-Login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
# Configuración de aplicación
ENV = os.environ.get('FLASK_ENV', 'development')
# En producción requerimos una secret key explícita
app.secret_key = os.environ.get('APP_SECRET_KEY') or (None if ENV == 'production' else 'dev-secret-key')

# Si estamos en producción y no hay secret, no arrancamos
if ENV == 'production' and not app.secret_key:
    raise SystemExit('APP_SECRET_KEY is required in production environment')

# DEBUG controlado por variable de entorno (valor '1' para true)
DEBUG = os.environ.get('FLASK_DEBUG', '1' if ENV != 'production' else '0') == '1'

# Credenciales de administrador (usar variables de entorno en producción)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'password')

# Seguridad mínima: en producción requerimos una contraseña de administrador razonable
if ENV == 'production':
    if not ADMIN_PASS or len(ADMIN_PASS) < 8:
        raise SystemExit('En producción ADMIN_PASS debe estar definida y tener al menos 8 caracteres')

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Usuario simple en memoria. Para una app real, usar una base de datos.
class User(UserMixin):
    def __init__(self, id_, username):
        self.id = id_
        self.username = username


# Creamos un único usuario administrador a partir de las variables de entorno
_ADMIN_USER_OBJ = User(1, ADMIN_USER)


@login_manager.user_loader
def load_user(user_id):
    # Sólo soportamos el usuario administrador en esta implementación simple
    try:
        uid = int(user_id)
    except Exception:
        return None
    if uid == _ADMIN_USER_OBJ.id:
        return _ADMIN_USER_OBJ
    return None


# Forzar HTTPS en producción si se desea (simple redirección).
@app.before_request
def enforce_https_in_production():
    # Si la variable de entorno FORCE_HTTPS está activada, y la petición no es segura, redirigir a https
    from flask import request, redirect
    if os.environ.get('FORCE_HTTPS', '0') == '1':
        # en servidores detrás de proxy, asegúrate de configurar X-Forwarded-Proto
        proto = request.headers.get('X-Forwarded-Proto', request.scheme)
        if proto != 'https':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

# Configuración del archivo JSON para los mensajes (puede sobrescribirse via env var para tests)
MENSAJES_FILE = os.environ.get('MENSAJES_FILE', 'data/mensajes.json')
MENSAJES_DB = os.environ.get('MENSAJES_DB', 'data/mensajes.db')


def get_db_connection():
    conn = sqlite3.connect(MENSAJES_DB)
    conn.row_factory = sqlite3.Row
    return conn


# Logging rotativo a file
def setup_logging():
    log_dir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(os.path.join(log_dir, 'flask.log'), maxBytes=10*1024*1024, backupCount=5)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


setup_logging()


def init_db():
    """Inicializa la base de datos SQLite y migra datos desde mensajes.json si procede."""
    if not os.path.exists('data'):
        os.makedirs('data')

    # Crear tabla si no existe
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT,
            email TEXT,
            telefono TEXT,
            servicio TEXT,
            empleados TEXT,
            mensaje TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()

    # Si hay un JSON con mensajes y la tabla está vacía, migrar
    cur.execute('SELECT COUNT(*) as cnt FROM mensajes')
    row = cur.fetchone()
    count = row['cnt'] if row else 0
    if count == 0 and os.path.exists(MENSAJES_FILE) and os.path.getsize(MENSAJES_FILE) > 0:
        try:
            with open(MENSAJES_FILE, 'r', encoding='utf-8') as f:
                mensajes = json.load(f)
        except Exception:
            mensajes = []

        # Ordenar por fecha asc para mantener consistencia
        try:
            mensajes.sort(key=lambda x: x.get('fecha', ''))
        except Exception:
            pass

        for m in mensajes:
            cur.execute(
                'INSERT INTO mensajes (empresa,email,telefono,servicio,empleados,mensaje,fecha) VALUES (?,?,?,?,?,?,?)',
                (
                    m.get('empresa',''), m.get('email',''), m.get('telefono',''),
                    m.get('servicio',''), m.get('empleados',''), m.get('mensaje',''), m.get('fecha','')
                )
            )
        conn.commit()
    conn.close()

def init_json_file():
    """Inicializa el archivo JSON si no existe"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Crear el archivo JSON si no existe
    if not os.path.exists(MENSAJES_FILE):
        with open(MENSAJES_FILE, 'w') as f:
            json.dump([], f)


## DB-backed message storage; previous JSON helpers replaced by DB functions

@app.route('/')
def index():
    """Ruta principal que renderiza el formulario"""
    return render_template('index.html')

@app.route('/api/guardar-mensaje', methods=['POST'])
def guardar_mensaje():
    """API para guardar los mensajes en un archivo JSON"""
    try:
        # Obtener los datos del formulario
        datos = request.json
        
        # Validar que todos los campos requeridos estén presentes
        campos_requeridos = ['empresa', 'email', 'telefono', 'servicio', 'empleados', 'mensaje']
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        # Guardar en la base de datos SQLite
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO mensajes (empresa,email,telefono,servicio,empleados,mensaje,fecha) VALUES (?,?,?,?,?,?,?)',
            (datos['empresa'], datos['email'], datos['telefono'], datos['servicio'], datos['empleados'], datos['mensaje'], fecha_actual)
        )
        conn.commit()
        # Obtener el id asignado por la DB
        last_id = cur.lastrowid
        conn.close()

        # Nota: ahora usamos SQLite como fuente única de verdad.
        # Si necesitas regenerar el archivo JSON legacy, usa el script `scripts/sync_db_to_json.py`.
        
        return jsonify({'success': True, 'message': 'Mensaje guardado correctamente'}), 200
    
    except Exception as e:
        print(f"Error al guardar el mensaje: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

# (deleted JSON write helper — DB is used)

@app.route('/admin/mensajes')
@login_required
def ver_mensajes():
    """Ruta para ver todos los mensajes (solo para administradores)"""
    try:
        # Leer desde la DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, empresa, email, telefono, servicio, empleados, mensaje, fecha FROM mensajes ORDER BY fecha DESC')
        rows = cur.fetchall()
        mensajes = [dict(r) for r in rows]
        conn.close()

        # Paginación simple
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        per_page = int(request.args.get('per_page', 20))
        total = len(mensajes)
        start = (page - 1) * per_page
        end = start + per_page
        page_items = mensajes[start:end]

        return render_template('admin/mensajes.html', mensajes=page_items, page=page, per_page=per_page, total=total)
    
    except Exception as e:
        print(f"Error al obtener los mensajes: {e}")
        return "Error al cargar los mensajes", 500


@app.route('/admin/mensajes/export.csv')
@login_required
def export_mensajes_csv():
    """Exportar todos los mensajes como CSV"""
    try:
        # Leer desde DB
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, fecha, empresa, email, telefono, servicio, empleados, mensaje FROM mensajes ORDER BY fecha DESC')
        rows = cur.fetchall()
        headers = ['id', 'fecha', 'empresa', 'email', 'telefono', 'servicio', 'empleados', 'mensaje']
        def generate():
            yield ','.join(headers) + '\n'
            for r in rows:
                m = dict(r)
                row = [str(m.get(h, '')).replace('"', '""') for h in headers]
                row = ['"' + rr + '"' if ',' in rr or '"' in rr else rr for rr in row]
                yield ','.join(row) + '\n'
        conn.close()

        return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=mensajes.csv"})
    except Exception as e:
        print(f"Error exportando CSV: {e}")
        return "Error exportando CSV", 500


@app.route('/healthz')
def healthz():
    return jsonify({'status':'ok'}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Formulario de login que autentica contra ADMIN_USER/ADMIN_PASS."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            # Autenticar el usuario administrador
            login_user(_ADMIN_USER_OBJ)
            flash('Inicio de sesión correcto.', 'success')
            next_page = request.args.get('next') or url_for('ver_mensajes')
            return redirect(next_page)
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Inicializar base de datos y migrar desde JSON si procede
    init_db()
    app.run(debug=DEBUG)