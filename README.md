# VetCare moderno

## Instalación
1. Importa `actualizar_sistema.sql` en phpMyAdmin.
2. Revisa `config.py`.
3. Abre esta carpeta directamente en VS Code.
4. Ejecuta:

```powershell
py -m pip install -r requirements.txt
py app.py
```

## Accesos iniciales
- Administrador: `admin` / `admin123`
- Recepcionista: `recepcion` / `recepcion123`

Los clientes y veterinarios usan el usuario y contraseña escritos al registrarlos.

## Permisos
- Administrador: crear clientes y veterinarios.
- Recepcionista: crear clientes, citas, revisar disponibilidad, historial y vacunas.
- Veterinario: agenda propia, estados de citas, historial y vacunas.
- Cliente: citas, horarios ocupados y alertas de vacunas.

Las alertas son internas dentro del sistema; no se envían por correo o WhatsApp.


## Logo ya integrado

El logo está guardado en:

```text
assets/logo.png
```

Aparece automáticamente en:

- Pantalla de inicio de sesión.
- Menú lateral.
- Icono de la ventana.

No cambies el nombre ni la ubicación de ese archivo.

## Compatibilidad con Python 3.14

Esta versión no utiliza Pillow. El logo se carga con `tkinter.PhotoImage`.

```powershell
py -m pip install -r requirements.txt
py app.py
```


## Corrección de congelamiento

Esta versión utiliza:

- `connection_timeout=5` para evitar esperas largas.
- Un hilo secundario para validar el inicio de sesión.
- El archivo `probar_conexion.py` para comprobar MySQL.

Antes de abrir el programa:

```powershell
py probar_conexion.py
py app.py
```

