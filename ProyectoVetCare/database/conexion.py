import mysql.connector
from config import DB_CONFIG


class Conexion:
    @staticmethod
    def conectar():
        try:
            conexion = mysql.connector.connect(**DB_CONFIG)

            if conexion.is_connected():
                return conexion

            return None

        except mysql.connector.Error as error:
            print(f"Error de conexión con MySQL: {error}")
            return None
