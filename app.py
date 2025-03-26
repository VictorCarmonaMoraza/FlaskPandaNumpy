from flask import Flask, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from Funciones.funciones import funciones_bp  # Importa el Blueprint

app = Flask(__name__)

# Configuración de Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mi API Flask"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(funciones_bp)  # Registra el Blueprint con prefijo /funciones

# Ruta de inicio (raíz) que redirige a Swagger UI
@app.route('/')
def index():
    return redirect(url_for('swagger_ui.show'))  # Corrección: usa 'swagger_ui.show'

if __name__ == '__main__':
    ## app.run(debug=True, port=5001)
    app.run(debug=True)