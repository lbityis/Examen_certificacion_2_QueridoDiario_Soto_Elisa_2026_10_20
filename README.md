# QueridoDiario

QueridoDiario es una aplicación hecha con Flask y MySQL para guardar recuerdos personales.

## Requisitos
- Python 3.10 o superior
- MySQL 8

## Instalación
1. Descomprime el proyecto y abre una terminal dentro de la carpeta.
2. Crea un entorno virtual: `python -m venv venv`
3. Actívalo en Windows: `venv\Scripts\activate` (Mac/Linux: `source venv/bin/activate`).
4. Instala las dependencias: `pip install -r requirements.txt`.
5. Copia `.env.example` como `.env` y completa la contraseña de MySQL y una `SECRET_KEY` larga y aleatoria.
6. En MySQL Workbench, abre y ejecuta `resources/DB/querido_diario.sql`. Esto crea la base de datos y las tablas.
7. Ejecuta la aplicación: `python server.py`.
8. Abre `http://127.0.0.1:5000`.

## Seguridad y validaciones
- Las contraseñas se guardan con hash, nunca como texto normal.
- Las páginas privadas requieren sesión y las consultas de entradas comprueban el usuario dueño.
- Borrar usa POST, no GET.
- La fecha debe tener formato válido, no puede estar vacía ni ser futura.
- Los errores de consulta se revisan y se muestran mensajes sencillos en pantalla.
- No compartas el archivo `.env`; contiene datos privados. No se incluye en Git.

## Archivos importantes
- `server.py`: inicia la aplicación.
- `flask_app/controllers`: rutas y validaciones.
- `flask_app/models`: consultas a MySQL.
- `flask_app/templates`: HTML sin Bootstrap.
- `flask_app/static/css/style.css`: estilos separados y adaptables.
- `resources/DB/querido_diario.sql`: estructura de la base de datos.
- `resources/DB/ERD.md`: diagrama de relaciones.
