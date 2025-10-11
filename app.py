from flask import Flask, render_template, request, jsonify, Response
import functools
import json
from datetime import datetime
import os

app = Flask(__name__)

# Credenciales de administrador (usar variables de entorno en producción)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'password')

def require_auth(f):
    """Decorator simple de HTTP Basic Auth para rutas de administración."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == ADMIN_USER and auth.password == ADMIN_PASS):
            return Response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


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

def init_json_file():
    """Inicializa el archivo JSON si no existe"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Crear el archivo JSON si no existe
    if not os.path.exists(MENSAJES_FILE):
        with open(MENSAJES_FILE, 'w') as f:
            json.dump([], f)

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
        
        # Generar un ID único basado en timestamp
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.now().timestamp()
        
        # Preparar el mensaje para guardar
        mensaje = {
            'id': int(timestamp * 1000),  # ID único basado en timestamp
            'empresa': datos['empresa'],
            'email': datos['email'],
            'telefono': datos['telefono'],
            'servicio': datos['servicio'],
            'empleados': datos['empleados'],
            'mensaje': datos['mensaje'],
            'fecha': fecha_actual
        }
        
        # Guardar en el archivo JSON
        guardar_en_archivo(mensaje)
        
        return jsonify({'success': True, 'message': 'Mensaje guardado correctamente'}), 200
    
    except Exception as e:
        print(f"Error al guardar el mensaje: {e}")
        return jsonify({'error': 'Error al procesar la solicitud'}), 500

def guardar_en_archivo(mensaje):
    """Guarda el mensaje en el archivo JSON"""
    try:
        # Leer los mensajes existentes
        if os.path.exists(MENSAJES_FILE) and os.path.getsize(MENSAJES_FILE) > 0:
            with open(MENSAJES_FILE, 'r', encoding='utf-8') as f:
                mensajes = json.load(f)
        else:
            mensajes = []
    except (json.JSONDecodeError, FileNotFoundError):
        mensajes = []
    
    # Añadir el nuevo mensaje
    mensajes.append(mensaje)
    
    # Guardar todos los mensajes
    with open(MENSAJES_FILE, 'w', encoding='utf-8') as f:
        json.dump(mensajes, f, indent=4, ensure_ascii=False)

@app.route('/admin/mensajes')
@require_auth
def ver_mensajes():
    """Ruta para ver todos los mensajes (solo para administradores)"""
    try:
        # Verificar si el archivo de mensajes existe
        if os.path.exists(MENSAJES_FILE) and os.path.getsize(MENSAJES_FILE) > 0:
            with open(MENSAJES_FILE, 'r', encoding='utf-8') as f:
                mensajes = json.load(f)
        else:
            mensajes = []
        
        # Ordenar mensajes por fecha (más reciente primero)
        mensajes.sort(key=lambda x: x.get('fecha', ''), reverse=True)

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
@require_auth
def export_mensajes_csv():
    """Exportar todos los mensajes como CSV"""
    try:
        if os.path.exists(MENSAJES_FILE) and os.path.getsize(MENSAJES_FILE) > 0:
            with open(MENSAJES_FILE, 'r', encoding='utf-8') as f:
                mensajes = json.load(f)
        else:
            mensajes = []

        # Cabeceras CSV
        headers = ['id', 'fecha', 'empresa', 'email', 'telefono', 'servicio', 'empleados', 'mensaje']
        def generate():
            yield ','.join(headers) + '\n'
            for m in mensajes:
                row = [str(m.get(h, '')).replace('"', '""') for h in headers]
                # Encerrar campos que contienen comas
                row = ['"' + r + '"' if ',' in r or '"' in r else r for r in row]
                yield ','.join(row) + '\n'

        return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=mensajes.csv"})
    except Exception as e:
        print(f"Error exportando CSV: {e}")
        return "Error exportando CSV", 500







if __name__ == '__main__':
    init_json_file()  # Inicializar el archivo JSON si no existe
    app.run(debug=True)