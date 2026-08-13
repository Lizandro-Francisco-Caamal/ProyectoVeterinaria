import hashlib
from repositorios.base import BaseRepositorio

class SistemaRepositorio(BaseRepositorio):
    def login(self, usuario, password):
        clave = hashlib.sha256(password.encode()).hexdigest()
        return self.ejecutar(
            '''SELECT id_usuario, usuario, rol, nombre, referencia_id
               FROM usuarios
               WHERE usuario=%s AND password=%s AND activo=1''',
            (usuario, clave), obtener=True, uno=True
        )

    def usuario_existe(self, usuario):
        return self.ejecutar(
            "SELECT id_usuario FROM usuarios WHERE usuario=%s",
            (usuario,), obtener=True, uno=True
        ) is not None

    def crear_usuario(self, usuario, password, rol, nombre, referencia_id):
        clave = hashlib.sha256(password.encode()).hexdigest()
        return self.ejecutar(
            '''INSERT INTO usuarios(usuario,password,rol,nombre,referencia_id,activo)
               VALUES(%s,%s,%s,%s,%s,1)''',
            (usuario, clave, rol, nombre, referencia_id)
        )

    def crear_cliente_con_mascota(self, datos):
        id_cliente = self.ejecutar(
            '''INSERT INTO duenos(nombre,correo,telefono,direccion)
               VALUES(%s,%s,%s,%s)''',
            (datos["nombre"], datos["correo"], datos["telefono"], datos["direccion"])
        )
        if not id_cliente:
            return False

        id_mascota = self.ejecutar(
            '''INSERT INTO mascotas(nombre,especie,raza,sexo,fecha_nacimiento,peso,color,id_dueno)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (
                datos["mascota"], datos["especie"], datos["raza"], datos["sexo"],
                datos["fecha_nacimiento"] or None, datos["peso"] or None,
                datos["color"], id_cliente
            )
        )
        if not id_mascota:
            return False

        return self.crear_usuario(
            datos["usuario"], datos["password"], "cliente",
            datos["nombre"], id_cliente
        )

    def crear_veterinario(self, datos):
        id_vet = self.ejecutar(
            '''INSERT INTO veterinarios(nombre,especialidad,correo,telefono)
               VALUES(%s,%s,%s,%s)''',
            (datos["nombre"], datos["especialidad"], datos["correo"], datos["telefono"])
        )
        if not id_vet:
            return False
        return self.crear_usuario(
            datos["usuario"], datos["password"], "veterinario",
            datos["nombre"], id_vet
        )

    def listar_clientes(self):
        return self.ejecutar(
            "SELECT id_dueno,nombre FROM duenos ORDER BY nombre", obtener=True
        )

    def listar_mascotas(self):
        return self.ejecutar(
            '''SELECT m.id_mascota, CONCAT(m.nombre," - ",d.nombre) descripcion
               FROM mascotas m JOIN duenos d ON d.id_dueno=m.id_dueno
               ORDER BY m.nombre''', obtener=True
        )

    def listar_mascotas_cliente(self, id_dueno):
        return self.ejecutar(
            "SELECT id_mascota,nombre FROM mascotas WHERE id_dueno=%s ORDER BY nombre",
            (id_dueno,), obtener=True
        )

    def listar_veterinarios(self):
        return self.ejecutar(
            "SELECT id_veterinario,nombre,especialidad FROM veterinarios ORDER BY nombre",
            obtener=True
        )

    def veterinario_ocupado(self, id_vet, fecha, hora):
        return self.ejecutar(
            '''SELECT id_cita FROM citas
               WHERE id_veterinario=%s AND fecha=%s AND hora=%s
               AND estado<>"Cancelada"''',
            (id_vet, fecha, hora), obtener=True, uno=True
        ) is not None

    def horarios_ocupados(self, id_vet, fecha):
        return self.ejecutar(
            '''SELECT hora,motivo,estado FROM citas
               WHERE id_veterinario=%s AND fecha=%s AND estado<>"Cancelada"
               ORDER BY hora''',
            (id_vet, fecha), obtener=True
        )

    def crear_cita(self, id_mascota, id_vet, fecha, hora, motivo):
        if self.veterinario_ocupado(id_vet, fecha, hora):
            return "ocupado"
        return self.ejecutar(
            '''INSERT INTO citas(id_mascota,id_veterinario,fecha,hora,motivo,estado)
               VALUES(%s,%s,%s,%s,%s,"Pendiente")''',
            (id_mascota, id_vet, fecha, hora, motivo)
        )

    def citas_todas(self):
        return self.ejecutar(
            '''SELECT c.id_cita,c.fecha,c.hora,m.nombre mascota,d.nombre cliente,
                      v.nombre veterinario,c.motivo,c.estado
               FROM citas c
               JOIN mascotas m ON m.id_mascota=c.id_mascota
               JOIN duenos d ON d.id_dueno=m.id_dueno
               JOIN veterinarios v ON v.id_veterinario=c.id_veterinario
               ORDER BY c.fecha DESC,c.hora DESC''', obtener=True
        )

    def citas_cliente(self, id_dueno):
        return self.ejecutar(
            '''SELECT c.fecha,c.hora,m.nombre mascota,v.nombre veterinario,
                      c.motivo,c.estado
               FROM citas c
               JOIN mascotas m ON m.id_mascota=c.id_mascota
               JOIN veterinarios v ON v.id_veterinario=c.id_veterinario
               WHERE m.id_dueno=%s ORDER BY c.fecha DESC,c.hora DESC''',
            (id_dueno,), obtener=True
        )

    def agenda_veterinario(self, id_vet):
        return self.ejecutar(
            '''SELECT c.id_cita,c.fecha,c.hora,m.nombre mascota,d.nombre cliente,
                      c.motivo,c.estado
               FROM citas c
               JOIN mascotas m ON m.id_mascota=c.id_mascota
               JOIN duenos d ON d.id_dueno=m.id_dueno
               WHERE c.id_veterinario=%s ORDER BY c.fecha DESC,c.hora DESC''',
            (id_vet,), obtener=True
        )

    def cambiar_estado(self, id_cita, estado):
        return self.ejecutar(
            "UPDATE citas SET estado=%s WHERE id_cita=%s", (estado, id_cita)
        )

    def historial_cliente(self, id_dueno):
        return self.ejecutar(
            '''SELECT m.nombre mascota,c.fecha,c.motivo,c.estado,
                      co.diagnostico,co.tratamiento,v.nombre veterinario
               FROM mascotas m
               LEFT JOIN citas c ON c.id_mascota=m.id_mascota
               LEFT JOIN consultas co ON co.id_cita=c.id_cita
               LEFT JOIN veterinarios v ON v.id_veterinario=c.id_veterinario
               WHERE m.id_dueno=%s ORDER BY c.fecha DESC''',
            (id_dueno,), obtener=True
        )

    def catalogo_vacunas(self):
        return self.ejecutar(
            "SELECT id_vacuna,nombre FROM vacunas ORDER BY nombre", obtener=True
        )

    def registrar_vacuna(self, id_mascota, id_vacuna, aplicacion, proxima):
        resultado = self.ejecutar(
            '''INSERT INTO vacunas_mascotas
               (id_mascota,id_vacuna,fecha_aplicacion,proxima_dosis)
               VALUES(%s,%s,%s,%s)''',
            (id_mascota,id_vacuna,aplicacion,proxima)
        )
        if resultado:
            self.ejecutar(
                '''INSERT INTO alertas(id_dueno,id_mascota,titulo,mensaje,tipo,fecha_alerta,leida)
                   SELECT id_dueno,id_mascota,"Próxima vacuna",
                   CONCAT("La mascota ",nombre," necesita una vacuna el ",%s),
                   "Vacuna",%s,0 FROM mascotas WHERE id_mascota=%s''',
                (proxima,proxima,id_mascota)
            )
        return resultado

    def alertas_cliente(self, id_dueno):
        return self.ejecutar(
            '''SELECT titulo,mensaje,fecha_alerta,leida FROM alertas
               WHERE id_dueno=%s ORDER BY leida,fecha_alerta''',
            (id_dueno,), obtener=True
        )

    def vacunas_proximas(self, id_dueno):
        return self.ejecutar(
            '''SELECT m.nombre mascota,v.nombre vacuna,vm.proxima_dosis,
                      DATEDIFF(vm.proxima_dosis,CURDATE()) dias
               FROM vacunas_mascotas vm
               JOIN mascotas m ON m.id_mascota=vm.id_mascota
               JOIN vacunas v ON v.id_vacuna=vm.id_vacuna
               WHERE m.id_dueno=%s
               AND vm.proxima_dosis<=DATE_ADD(CURDATE(),INTERVAL 30 DAY)
               ORDER BY vm.proxima_dosis''',
            (id_dueno,), obtener=True
        )
