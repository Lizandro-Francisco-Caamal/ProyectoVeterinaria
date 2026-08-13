from database.conexion import Conexion


class BaseRepositorio:
    def ejecutar(self, sql, parametros=(), obtener=False, uno=False):
        conexion = Conexion.conectar()

        if not conexion:
            return None if uno else ([] if obtener else False)

        cursor = None

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, parametros)

            if obtener:
                return cursor.fetchone() if uno else cursor.fetchall()

            conexion.commit()
            return cursor.lastrowid or True

        except Exception as error:
            print(f"Error SQL: {error}")

            if conexion.is_connected():
                conexion.rollback()

            return None if uno else ([] if obtener else False)

        finally:
            if cursor is not None:
                cursor.close()

            if conexion.is_connected():
                conexion.close()
