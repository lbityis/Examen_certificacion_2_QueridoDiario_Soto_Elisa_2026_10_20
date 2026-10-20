import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

class ConexionMySQL:
    def __init__(self, bd):
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        
        self.conexion = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=bd,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def consultar_bd(self, consulta, datos=None):
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute(consulta, datos or {})
                sql = consulta.strip().lower()

                if sql.startswith("select"):
                    res = cursor.fetchall()
                    # Manejo de error si la consulta retorna None
                    return res if res is not None else []
                if sql.startswith("insert"):
                    return cursor.lastrowid
                return cursor.rowcount
        except Exception as e:
            # Imprime y retorna False para controlar fallos de MySQL
            print("Error en base de datos:", e)
            return False
        finally:
            self.conexion.close()

def conectar_mysql(bd=None):
    if bd is None:
        bd = os.getenv("MYSQL_DB", "esquema_diario")
    return ConexionMySQL(bd)