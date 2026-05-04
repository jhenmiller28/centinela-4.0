# IMPORTAMOS EL MODULO OS (OPERATING SYSTEM)
# ES LA LIBRERIA NATIVA DE PYTHON QUE NOS PREMITE HABLAR CON EL SERVIDOR UBUUNTU
# PARA PODER LEER ARCHIVOS Y EN ESTE CASO, LEER LAS VARIABLES DE ENTORNO

import os


class Config:
    """ " clase  centralizada para poder gestiionar
    las variables de entorno de centinela 4.0
    agurpar esto en una clase ecita que tengamos variables sueltas
    por todo el proyecto
    """

    # 1archivos
    # getenv = " get enviroment variable" obtener variabbale de entorno
    # funciona asi: os.getenv("nombre de variable", "valor por defecto")
    # sino encuentra log_path en el archivo .env usar" /var/log/auth.log" por seguridad
    LOG_PATH = os.getenv("LOG_PATH", "/var/log/auth.log")

    # 2 seguridad
    MI_IP_SEGURA = os.getenv("MI_IP_SEGURA")

    # BASE DE DATOS(EN POSTGRESQL)
    # DB = DATEBASE. LEEMOS LAS CREDENCIALES PARA CONECTAR EL CONTENEDOR DE PYTHON CO EL DE POSTGERSQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    # alertas (telegran)
    # TOKEN ES LA LLAVE EDL BOT , CHAT ID ES ELNUMERO DEL CHAT DE TELEGRAM
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    @classmethod
    def validar_configuracion(cls):
        """cls es la abreviatura de class. representa a la clase config asi misma
        principio de fail fast(falla rapida ):si llega a faltar algo critico, el sistema no arranca
        """

        # crearemos una lista vacia donde crearemos donode guaardaremos los nombres de las variables de entorno
        faltantes = []

        # verificamos si la variable es nula(not) o si olvidaste cambiar ek texto de relleno
        if not cls.MI_IP_SEGURA or cls.MI_IP_SEGURA == "TU_IP_DE_ATE_O_MOVIL":
            faltantes.append("MI_IP_SEGURA")

        if not cls.DB_NAME:
            faltantes.append("POSTGRES_DB")

        # si la lista faltante tiene contenido...es decir algo fallo
        if faltantes:
            # raise detiene la ejecucion del script de inmediato
            # value error es el tipo de error qye le indica al sistema qye un valor es invalido
            # .join() toma la lista de faltantes y los une en un solo texto separado por comas
            raise ValueError(
                f"ERROR FATAL: Faltan las siguientes variables de entorno: {', '.join(faltantes)}"
            )

        # si el codigo llega hasta aqui, significa qye todo esta bien y no se detuvo
        print("[CONFIG] Configuracion valida correctamente.")
