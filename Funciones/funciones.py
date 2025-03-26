from flask import Blueprint, jsonify, request
import pandas as pd
import io

funciones_bp = Blueprint('funciones', __name__)

@funciones_bp.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "¡Hola desde mi API!"})

@funciones_bp.route('/cargar_csv', methods=['POST'])
def cargar_csv():
    if 'archivo' not in request.files:
        return jsonify({'mensaje': 'No se proporcionó ningún archivo'}), 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return jsonify({'mensaje': 'No se seleccionó ningún archivo'}), 400

    if archivo and archivo.filename.endswith('.csv'):
        try:
            # Lee el archivo CSV directamente desde la memoria con ISO-8859-1 y separador ';'
            df = pd.read_csv(io.StringIO(archivo.stream.read().decode('ISO-8859-1')), sep=';')

            # Convierte la columna 'Esperanza de vida' a números
            df['Esperanza de vida'] = pd.to_numeric(df['Esperanza de vida'].str.replace(',', '.'), errors='coerce')

            # Convierte el DataFrame a una lista de diccionarios (objetos JSON)
            datos = df.to_dict(orient='records')

            # Agrega el conteo de elementos al JSON
            conteo_elementos = len(datos)
            respuesta = {'datos': datos, 'conteo': conteo_elementos}

            return jsonify(respuesta), 200

        except Exception as e:
            return jsonify({'mensaje': f'Error al procesar el archivo CSV: {str(e)}'}), 500

    return jsonify({'mensaje': 'El archivo no tiene el formato CSV correcto'}), 400