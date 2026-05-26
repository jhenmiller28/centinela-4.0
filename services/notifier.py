import os
import requests
from dotenv import load_dotenv

# 1 abrimos la caja fuerte de .env para leer los secretos
load_dotenv()


class TelegramNotifier:
    def __init__(self):
        # extraeremos el token y el chat id de telegram de la boveda
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        # CONSTRUIMOS LA URL QUE USARA LA API DE TELEGRAM PARA ENVIAR LAS ALERTAS
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def enviar_notificacion(self, ip_atacante, strikes):
        """se enviara un mensaje de alerta formateado a mi bot en telegram cada vez que se detecte un ataque
        Args:
            ip_atacante (str): la ip del atacante que se detecto
            strikes (int): el numero de intentos fallidos que se han registrado para esa ip
        """
        # DISEÑAMOS EL MENSAJE DE ALERTA CON PRINTS, FORMATO HTML Y ALGUN EMOJI PARA HACERLO MAS VISUAL
        mensaje = f"🖲️<b> ALERTA CENTINELA 4.0 </b> 🛡️\n\n"
        mensaje += f"🚨 <b>IP Atacante:</b> <code>{ip_atacante}</code>\n"
        mensaje += f"🔴<b>Strikes registrados:</b> <code>{strikes}</code>\n"
        mensaje += f"<i>El servidor AWS resistio y guardo el registro en postgreSQL</i>"

        # SE PREPARA LA CARGA DE DATOS PARA ENVIAR A LA API DE TELEGRAM
        payload = {
            "chat_id": self.chat_id,
            "text": mensaje,
            "parse_mode": "HTML",  # ES PARA PERMITIR A TELEGRAM LEER LAS ETIQUETAS HTML
        }
        # AHORA ENVIAREMOS EL MENSAJE A TELEGRAM USANDO LA LIBRERIA REQUESTS PARA HACER UNA SOLICITUD POST A LA API DE TELEGRAM
        try:
            respuesta = requests.post(self.api_url, data=payload)

            if respuesta.status_code == 200:
                print(
                    f"[TELEGRAM]Notificación enviada con éxito sobre la ip {ip_atacante}"
                )
            else:
                print(
                    f"[TELEGRAM] ERRO DE API: codigo {respuesta.status_code} - {respuesta.text}"
                )
        except Exception as e:
            print(f"[TELEGRAM]falla critica en la conexion a internet: {e}")


# BLOQUE DE PRUEBA PARA VER SI EL NOTIFICADOR FUNCIONA CORRECTAMENTE CUANDO SE EJEC
if __name__ == "__main__":
    bot = TelegramNotifier()
    print("probando la conexion con telegram...")
    bot.enviar_notificacion("192.168.1.999", 3)
