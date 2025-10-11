from flask import Flask, render_template, request, jsonify, send_from_directory
import json
from datetime import datetime
import os

app = Flask(__name__)

# Configuración del archivo JSON para los mensajes
MENSAJES_FILE = 'data/mensajes.json'

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
        
        return render_template('admin/mensajes.html', mensajes=mensajes)
    
    except Exception as e:
        print(f"Error al obtener los mensajes: {e}")
        return "Error al cargar los mensajes", 500







if __name__ == '__main__':
    init_json_file()  # Inicializar el archivo JSON si no existe
    app.run(debug=True)