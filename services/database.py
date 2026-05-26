# IMPRTAMOS LA LIBRERIA QUE NOS PERMITIRA LA COMUNICACION CON POSTGRESQL
import psycopg2

# ACA ES DONDE IMPORTAMOS LA RECETA BASE
# PYTHON BUSCA LA CARPETA "CONFIG" EL ARCHIVO "SETTINGS"
# Y NOS TRAE LA CLASE "CONFIG" PARA PODER USAR SUS ATRIBUTOS
from config.settings import Config


class DatabaseService:
    """es el sercicio dedicado a manejar la base de datos
    aplica el principio de responsabilidad unica SRP
    solo se encarga de la conexcioin de la base datos y consultas"""

    def __init__(self):
        # cuando se inicia este servcico la conexion "conn" empieza vacia(none)
        self.conn = None

    def conectar(self):
        """establece la conexion con la base de datos, usando las variables
        que se validan en setting.py"""
        try:
            # usamos los valores exactos que settings.py leyo en el archivo .env
            self.conn = psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
            )
            print("conexion a base de datos POSTGRESQL exitosa!!")
        except Exception as e:
            print(f"ERROR:no se puede conectar a la base de datos psotgresql:{e}")
            raise  # se detiene todo si es que no hay conexion a la base de datos

    def registrar_y_obtener_intentos(self, ip):
        """este metodo se encarga de registrar la ip atacante y las veces qye atacado (STRIKES)"""

        # sino hay conexion activa, la abriremos primero
        if not self.conn:
            self.conectar()

        try:
            cur = self.conn.cursor()
            # upser(combinar insert y update) para rehistar la ip atacante(si hay confivcto, la ip ya fue registrada)
            # ira actualizando y sumando +1
            query = """
            INSERT INTO intentos (ip, strikes)
            VALUES(%,1, CURRENT_TIMESTAMP)
            ON CONFLICT(IP)
            DO UPDATE SET intentos = ataques.intentos + 1, ultimo_ataque = CURRENT_TIMESTAMP
            RETURNING intentos:"""

            cur.execute(query, (ip,))
            # fetchone()[0] extrae el nrmero exacto que nos devolvio el returning intrntos
            intentos = cur.fetchone()[0]
            # guardamos los cambios de manera permanente en la db
            self.conn.commit()
            cur.close()
            return intentos

        except Exception as e:
            print(f"[DB] error registrando IP {ip}:{e}")
            self.conn.rollback()  # si algo falla se desahace la transaccion para no corronper datos
            return (
                1  # devolveremos 1 por seguridad y que al menos avise del primer strike
            )

    def cerrar(self):
        self.conn.close()
        print("[DB] conexion cerrada")
