
import re

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

from flask_app.models import usuario

# Creamos las rutas de usuarios
usuarios = Blueprint('usuarios', __name__)


# Registro e inicio de sesión
@usuarios.route('/', methods=['GET', 'POST'])
def inicio():

    # Si ya inició sesión, entramos al diario
    if session.get('usuario_id'):
        return redirect(url_for('entradas.panel'))

    if request.method == 'POST':
        accion = request.form.get('accion')

        # Registramos una cuenta
        if accion == 'registro':
            nombre = request.form.get('nombre', '').strip()
            apellido = request.form.get('apellido', '').strip()
            email = request.form.get('email', '').strip().lower()
            edad = request.form.get('edad', '').strip()
            clave = request.form.get('clave', '')
            confirmar = request.form.get('confirmar', '')

            errores = []

            # Validamos los nombres
            if len(nombre) < 2 or len(apellido) < 2:
                errores.append(
                    'Nombre y apellido deben tener al menos 2 caracteres.'
                )

            # Validamos el correo
            patron_email = r'[^@\s]+@[^@\s]+\.[^@\s]+'

            if not re.fullmatch(patron_email, email):
                errores.append('Escribe un correo válido.')

            # Validamos la edad sin convertir texto inválido
            edad_numero = None

            if not edad.isdigit():
                errores.append('Ingresa una edad válida.')
            else:
                edad_numero = int(edad)

                if not 18 <= edad_numero <= 120:
                    errores.append('Debes tener entre 18 y 120 años.')

            # Validamos la contraseña
            if len(clave) < 8:
                errores.append(
                    'La contraseña debe tener al menos 8 caracteres.'
                )

            # Comprobamos que las contraseñas coincidan
            if clave != confirmar:
                errores.append('Las contraseñas no coinciden.')

            # Revisamos si el correo ya existe
            if not errores:
                existente = usuario.buscar_email(email)

                if existente:
                    errores.append('Ese correo ya está registrado.')

            # Mostramos los errores
            if errores:
                for error in errores:
                    flash(error, 'error')

            # Guardamos la cuenta
            elif usuario.crear(
                nombre, apellido, email, edad_numero, clave
            ):
                persona = usuario.validar(email, clave)

                # Iniciamos sesión si se creó correctamente
                if persona:
                    session.clear()
                    session['usuario_id'] = persona['id']
                    session['nombre'] = persona['nombre']

                    flash('¡Bienvenida a QueridoDiario! ♡', 'ok')
                    return redirect(url_for('entradas.panel'))

                flash(
                    'La cuenta se guardó, pero no se pudo iniciar sesión.',
                    'error'
                )

            else:
                flash(
                    'No se pudo crear la cuenta. Revisa MySQL.',
                    'error'
                )

        # Iniciamos sesión con una cuenta existente
        elif accion == 'login':
            email = request.form.get(
                'email_login', ''
            ).strip().lower()

            clave = request.form.get('clave_login', '')

            persona = usuario.validar(email, clave)

            if persona:
                session.clear()
                session['usuario_id'] = persona['id']
                session['nombre'] = persona['nombre']

                return redirect(url_for('entradas.panel'))

            flash('Correo o contraseña incorrectos.', 'error')

        else:
            flash('Selecciona una acción válida.', 'error')

    # Mostramos el formulario
    return render_template('inicio.html')


# Cerramos la sesión
@usuarios.route('/salir', methods=['POST'])
def salir():
    session.clear()
    flash('Sesión cerrada correctamente.', 'ok')

    return redirect(url_for('usuarios.inicio'))
