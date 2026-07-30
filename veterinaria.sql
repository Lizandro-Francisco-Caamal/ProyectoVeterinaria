CREATE DATABASE IF NOT EXISTS veterinaria;
USE veterinaria;

CREATE TABLE duenos (
    id_dueno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100),
    direccion VARCHAR(200)
);

CREATE TABLE mascotas (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especie VARCHAR(30),
    raza VARCHAR(50),
    sexo ENUM('Macho','Hembra'),
    edad INT,
    peso DECIMAL(5,2),
    color VARCHAR(30),
    fecha_nacimiento DATE,
    id_dueno INT,
    FOREIGN KEY (id_dueno) REFERENCES duenos(id_dueno)
);

CREATE TABLE veterinarios (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(50),
    telefono VARCHAR(15),
    correo VARCHAR(100)
);

CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT,
    id_veterinario INT,
    fecha DATE,
    hora TIME,
    motivo VARCHAR(200),
    estado ENUM('Pendiente','Atendida','Cancelada'),
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota),
    FOREIGN KEY (id_veterinario) REFERENCES veterinarios(id_veterinario)
);

CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    costo DECIMAL(10,2),
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
);

CREATE TABLE vacunas (
    id_vacuna INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE vacunas_mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT,
    id_vacuna INT,
    fecha_aplicacion DATE,
    proxima_dosis DATE,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota),
    FOREIGN KEY (id_vacuna) REFERENCES vacunas(id_vacuna)
);

INSERT INTO duenos(nombre,telefono,correo,direccion) VALUES
('Juan Pérez','9811234567','juan@gmail.com','Col. Centro'),
('María López','9814567890','maria@gmail.com','Santa Ana'),
('Carlos Gómez','9819876543','carlos@gmail.com','San Román');

INSERT INTO mascotas(nombre,especie,raza,sexo,edad,peso,color,fecha_nacimiento,id_dueno) VALUES
('Max','Perro','Labrador','Macho',4,28.50,'Negro','2022-05-10',1),
('Luna','Gato','Persa','Hembra',2,4.20,'Blanco','2024-01-18',2),
('Rocky','Perro','Pastor Alemán','Macho',6,34.00,'Café','2020-08-15',3);

INSERT INTO veterinarios(nombre,especialidad,telefono,correo) VALUES
('Dra. Ana Torres','Medicina General','9811111111','ana@vet.com'),
('Dr. Pedro Castillo','Cirugía','9812222222','pedro@vet.com');

INSERT INTO citas(id_mascota,id_veterinario,fecha,hora,motivo,estado) VALUES
(1,1,'2026-07-15','10:00:00','Vacunación','Pendiente'),
(2,2,'2026-07-16','12:30:00','Consulta General','Pendiente');

INSERT INTO consultas(id_cita,diagnostico,tratamiento,observaciones,costo) VALUES
(1,'Mascota sana','Aplicar vacuna anual','Sin complicaciones',450.00);

INSERT INTO vacunas(nombre,descripcion) VALUES
('Antirrábica','Previene la rabia'),
('Triple Felina','Protege contra enfermedades felinas'),
('Parvovirus','Vacuna para perros');

INSERT INTO vacunas_mascotas(id_mascota,id_vacuna,fecha_aplicacion,proxima_dosis) VALUES
(1,1,'2026-07-15','2027-07-15'),
(2,2,'2026-07-16','2027-07-16');
