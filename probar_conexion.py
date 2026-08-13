from database.conexion import Conexion


def main():
    print("Probando conexión con MySQL...")
    conexion = Conexion.conectar()

    if conexion:
        print("Conexión correcta con la base de datos veterinaria.")
        conexion.close()
    else:
        print("No fue posible conectar.")
        print("Revisa que MySQL esté encendido en XAMPP.")
        print("Revisa también config.py y la base de datos veterinaria.")


if __name__ == "__main__":
    main()
