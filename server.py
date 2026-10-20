
import os
from flask import Flask
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()


# Creamos la aplicación
def crear_app():
    app = Flask(
        __name__,
        template_folder='flask_app/templates',
        static_folder='flask_app/static'
    )

    # Protegemos las sesiones
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    if not app.config['SECRET_KEY']:
        raise RuntimeError('Falta SECRET_KEY en el archivo .env')

    # Importamos las rutas
    from flask_app.controllers.usuarios import usuarios
    from flask_app.controllers.entradas import entradas

    # Activamos las rutas
    app.register_blueprint(usuarios)
    app.register_blueprint(entradas)

    return app


# Creamos el sitio
app = crear_app()


# Iniciamos el servidor
if __name__ == '__main__':
    app.run(debug=True)
