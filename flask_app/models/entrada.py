from datetime import datetime, date
from flask import flash
from flask_app.config.mysqlconnection import conectar_mysql

class Entrada:
    def __init__(self, datos):
        self.id = datos['id']
        self.titulo = datos['titulo']
        self.fecha = datos['fecha']
        self.notas = datos['notas']
        self.usuario_id = datos['usuario_id']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO entradas (titulo, fecha, notas, usuario_id)
            VALUES (%(titulo)s, %(fecha)s, %(notas)s, %(usuario_id)s);
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def obtener_por_usuario(cls, usuario_id):
        # Entradas ordenadas de mas reciente a mas antigua
        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s 
            ORDER BY fecha DESC, created_at DESC;
        """
        resultados = conectar_mysql().consultar_bd(query, {"usuario_id": usuario_id})
        lista = []
        if resultados:
            for fila in resultados:
                lista.append(cls(fila))
        return lista

    @classmethod
    def obtener_por_id(cls, entrada_id):
        query = "SELECT * FROM entradas WHERE id = %(id)s;"
        resultados = conectar_mysql().consultar_bd(query, {"id": entrada_id})
        if not resultados or len(resultados) == 0:
            return False
        return cls(resultados[0])

    @classmethod
    def buscar_por_notas(cls, usuario_id, termino):
        # Filtra por el contenido de notas enviadas en la URL
        query = """
            SELECT * FROM entradas 
            WHERE usuario_id = %(usuario_id)s AND notas LIKE %(termino)s 
            ORDER BY fecha DESC;
        """
        datos = {
            "usuario_id": usuario_id,
            "termino": f"%{termino}%"
        }
        resultados = conectar_mysql().consultar_bd(query, datos)
        lista = []
        if resultados:
            for fila in resultados:
                lista.append(cls(fila))
        return lista

    @classmethod
    def actualizar(cls, datos):
        query = """
            UPDATE entradas 
            SET titulo = %(titulo)s, fecha = %(fecha)s, notas = %(notas)s 
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return conectar_mysql().consultar_bd(query, datos)

    @classmethod
    def eliminar(cls, entrada_id, usuario_id):
        query = "DELETE FROM entradas WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return conectar_mysql().consultar_bd(query, {"id": entrada_id, "usuario_id": usuario_id})

    @staticmethod
    def validar_entrada(form):
        es_valido = True

        titulo = form.get("titulo", "").strip()
        fecha = form.get("fecha", "").strip()
        notas = form.get("notas", "").strip()

        # Validacion de campos no vacios
        if len(titulo) == 0:
            flash("El título no puede estar vacío.", "entrada")
            es_valido = False

        if len(notas) == 0:
            flash("Las notas no pueden estar vacías.", "entrada")
            es_valido = False

        # Validar formato de fecha y que no sea en el futuro
        if not fecha:
            flash("Debes ingresar una fecha válida.", "entrada")
            es_valido = False
        else:
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                if fecha_obj > date.today():
                    flash("La fecha no puede ser futura.", "entrada")
                    es_valido = False
            except ValueError:
                flash("Formato de fecha inválido.", "entrada")
                es_valido = False

        return es_valido