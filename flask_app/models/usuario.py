
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

from flask_app.config.mysqlconnection import conectar


# Modelo para administrar los usuarios
class Usuario:

    # Registramos un usuario nuevo
    @staticmethod
    def crear(nombre, apellido, email, edad, clave):
        conexion = conectar()

        if conexion is None:
            return False

        try:
            # Guardamos la contraseña como hash, nunca como texto normal
            clave_hash = generate_password_hash(clave)

            with conexion.cursor() as cursor:
                sql = """
                    INSERT INTO usuarios
                    (nombre, apellido, email, edad, clave)
                    VALUES (%s, %s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    (nombre, apellido, email, edad, clave_hash)
                )

            conexion.commit()
            return True

        except pymysql.MySQLError as error:
            conexion.rollback()
            print("Error al crear usuario:", error)
            return False

        finally:
            conexion.close()

    # Buscamos un usuario por su correo
    @staticmethod
    def buscar_email(email):
        conexion = conectar()

        if conexion is None:
            return None

        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT id, nombre, apellido, email, edad, clave
                    FROM usuarios
                    WHERE email = %s
                    LIMIT 1
                """

                cursor.execute(sql, (email,))
                return cursor.fetchone()

        except pymysql.MySQLError as error:
            print("Error al buscar usuario:", error)
            return None

        finally:
            conexion.close()

    # Comprobamos el correo y la contraseña
    @staticmethod
    def validar(email, clave):
        persona = Usuario.buscar_email(email)

        if not persona:
            return None

        # Verificamos la contraseña con el hash guardado
        try:
            if check_password_hash(persona['clave'], clave):
                return {
                    'id': persona['id'],
                    'nombre': persona['nombre'],
                    'apellido': persona['apellido'],
                    'email': persona['email'],
                    'edad': persona['edad']
                }

        except (ValueError, TypeError) as error:
            print("Error al verificar contraseña:", error)

        return None


# Dejamos disponibles las funciones para los controladores
crear = Usuario.crear
buscar_email = Usuario.buscar_email
validar = Usuario.validar
