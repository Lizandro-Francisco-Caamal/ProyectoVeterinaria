-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-08-2026 a las 15:17:37
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `veterinaria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alertas`
--

CREATE TABLE `alertas` (
  `id_alerta` int(11) NOT NULL,
  `id_dueno` int(11) NOT NULL,
  `id_mascota` int(11) DEFAULT NULL,
  `titulo` varchar(120) NOT NULL,
  `mensaje` text NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `fecha_alerta` date NOT NULL,
  `leida` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alertas`
--

INSERT INTO `alertas` (`id_alerta`, `id_dueno`, `id_mascota`, `titulo`, `mensaje`, `tipo`, `fecha_alerta`, `leida`) VALUES
(1, 1, 1, 'Vacuna próxima', 'Max necesita su refuerzo de vacuna antirrábica el 20 de agosto de 2026.', 'Vacuna', '2026-08-20', 0),
(2, 2, 2, 'Vacuna próxima', 'Luna tiene una vacuna próxima programada.', 'Vacuna', '2026-09-01', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id_cita` int(11) NOT NULL,
  `id_mascota` int(11) NOT NULL,
  `id_veterinario` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `motivo` varchar(250) NOT NULL,
  `estado` enum('Pendiente','Atendida','Cancelada') DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id_cita`, `id_mascota`, `id_veterinario`, `fecha`, `hora`, `motivo`, `estado`) VALUES
(1, 1, 1, '2026-08-15', '10:00:00', 'Consulta general', 'Pendiente'),
(2, 2, 2, '2026-08-16', '12:00:00', 'Revisión preventiva', 'Pendiente'),
(3, 3, 3, '2026-08-17', '11:00:00', 'Revisión de piel', 'Pendiente'),
(4, 1, 4, '2026-07-20', '09:30:00', 'Vacunación', 'Atendida');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultas`
--

CREATE TABLE `consultas` (
  `id_consulta` int(11) NOT NULL,
  `id_cita` int(11) NOT NULL,
  `diagnostico` text DEFAULT NULL,
  `tratamiento` text DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consultas`
--

INSERT INTO `consultas` (`id_consulta`, `id_cita`, `diagnostico`, `tratamiento`, `observaciones`, `costo`) VALUES
(1, 4, 'Mascota en buen estado general', 'Aplicación de vacuna y vitaminas', 'Regresar a revisión preventiva.', 550.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `duenos`
--

CREATE TABLE `duenos` (
  `id_dueno` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `correo` varchar(120) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `duenos`
--

INSERT INTO `duenos` (`id_dueno`, `nombre`, `correo`, `telefono`, `direccion`) VALUES
(1, 'Luis Pérez', 'luis@email.com', '9813000001', 'Campeche, Campeche'),
(2, 'Sofía Rodríguez', 'sofia@email.com', '9813000002', 'Campeche, Campeche');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mascotas`
--

CREATE TABLE `mascotas` (
  `id_mascota` int(11) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `especie` varchar(50) NOT NULL,
  `raza` varchar(80) DEFAULT NULL,
  `sexo` enum('Macho','Hembra') NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `peso` decimal(6,2) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `id_dueno` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mascotas`
--

INSERT INTO `mascotas` (`id_mascota`, `nombre`, `especie`, `raza`, `sexo`, `fecha_nacimiento`, `peso`, `color`, `id_dueno`) VALUES
(1, 'Max', 'Perro', 'Labrador', 'Macho', '2022-04-10', 28.50, 'Dorado', 1),
(2, 'Luna', 'Gato', 'Siamés', 'Hembra', '2023-08-15', 4.30, 'Crema', 2),
(3, 'Rocky', 'Perro', 'Pug', 'Macho', '2024-01-10', 8.20, 'Beige', 1),
(4, 'Nala', 'Gato', 'Europeo', 'Hembra', '2024-05-20', 3.80, 'Gris', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `rol` enum('administrador','recepcionista','veterinario','cliente') NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `referencia_id` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `usuario`, `password`, `rol`, `nombre`, `referencia_id`, `activo`) VALUES
(1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'administrador', 'Administrador VetCare', NULL, 1),
(2, 'recepcion', 'e7af7bf39dbc423a5e12298ae05f86bb3b227d8b9d7c3656b9990ffeb0015219', 'recepcionista', 'Recepcionista VetCare', NULL, 1),
(3, 'vet1', '95668df3d5465c0efe2bddca0ae448bb213dfdcd7ed446039003e693c22284b1', 'veterinario', 'Dra. Ana López', 1, 1),
(4, 'vet2', '95668df3d5465c0efe2bddca0ae448bb213dfdcd7ed446039003e693c22284b1', 'veterinario', 'Dr. Carlos Hernández', 2, 1),
(5, 'vet3', '95668df3d5465c0efe2bddca0ae448bb213dfdcd7ed446039003e693c22284b1', 'veterinario', 'Dra. Mariana Gómez', 3, 1),
(6, 'vet4', '95668df3d5465c0efe2bddca0ae448bb213dfdcd7ed446039003e693c22284b1', 'veterinario', 'Dr. José Martínez', 4, 1),
(7, 'cliente1', '09a31a7001e261ab1e056182a71d3cf57f582ca9a29cff5eb83be0f0549730a9', 'cliente', 'Luis Pérez', 1, 1),
(8, 'cliente2', '09a31a7001e261ab1e056182a71d3cf57f582ca9a29cff5eb83be0f0549730a9', 'cliente', 'Sofía Rodríguez', 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacunas`
--

CREATE TABLE `vacunas` (
  `id_vacuna` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacunas`
--

INSERT INTO `vacunas` (`id_vacuna`, `nombre`, `descripcion`) VALUES
(1, 'Antirrábica', 'Previene la rabia en perros y gatos.'),
(2, 'Séxtuple canina', 'Vacuna múltiple para perros.'),
(3, 'Bordetella', 'Prevención de tos de las perreras.'),
(4, 'Triple felina', 'Vacuna preventiva para gatos.'),
(5, 'Leucemia felina', 'Prevención de leucemia felina.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacunas_mascotas`
--

CREATE TABLE `vacunas_mascotas` (
  `id` int(11) NOT NULL,
  `id_mascota` int(11) NOT NULL,
  `id_vacuna` int(11) NOT NULL,
  `fecha_aplicacion` date NOT NULL,
  `proxima_dosis` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacunas_mascotas`
--

INSERT INTO `vacunas_mascotas` (`id`, `id_mascota`, `id_vacuna`, `fecha_aplicacion`, `proxima_dosis`) VALUES
(1, 1, 1, '2025-08-20', '2026-08-20'),
(2, 1, 2, '2025-08-20', '2026-08-20'),
(3, 2, 4, '2025-09-01', '2026-09-01');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `veterinarios`
--

CREATE TABLE `veterinarios` (
  `id_veterinario` int(11) NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `correo` varchar(120) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `veterinarios`
--

INSERT INTO `veterinarios` (`id_veterinario`, `nombre`, `especialidad`, `correo`, `telefono`) VALUES
(1, 'Dra. Ana López', 'Medicina General', 'ana@vetcare.com', '9812000001'),
(2, 'Dr. Carlos Hernández', 'Cirugía Veterinaria', 'carlos@vetcare.com', '9812000002'),
(3, 'Dra. Mariana Gómez', 'Dermatología Veterinaria', 'mariana@vetcare.com', '9812000003'),
(4, 'Dr. José Martínez', 'Medicina Preventiva', 'jose@vetcare.com', '9812000004');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD PRIMARY KEY (`id_alerta`),
  ADD KEY `id_dueno` (`id_dueno`),
  ADD KEY `id_mascota` (`id_mascota`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD UNIQUE KEY `horario_veterinario` (`id_veterinario`,`fecha`,`hora`),
  ADD KEY `fk_cita_mascota` (`id_mascota`);

--
-- Indices de la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD PRIMARY KEY (`id_consulta`),
  ADD KEY `id_cita` (`id_cita`);

--
-- Indices de la tabla `duenos`
--
ALTER TABLE `duenos`
  ADD PRIMARY KEY (`id_dueno`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `mascotas`
--
ALTER TABLE `mascotas`
  ADD PRIMARY KEY (`id_mascota`),
  ADD KEY `fk_mascota_dueno` (`id_dueno`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- Indices de la tabla `vacunas`
--
ALTER TABLE `vacunas`
  ADD PRIMARY KEY (`id_vacuna`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `vacunas_mascotas`
--
ALTER TABLE `vacunas_mascotas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_mascota` (`id_mascota`),
  ADD KEY `id_vacuna` (`id_vacuna`);

--
-- Indices de la tabla `veterinarios`
--
ALTER TABLE `veterinarios`
  ADD PRIMARY KEY (`id_veterinario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alertas`
--
ALTER TABLE `alertas`
  MODIFY `id_alerta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id_cita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `consultas`
--
ALTER TABLE `consultas`
  MODIFY `id_consulta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `duenos`
--
ALTER TABLE `duenos`
  MODIFY `id_dueno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `mascotas`
--
ALTER TABLE `mascotas`
  MODIFY `id_mascota` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `vacunas`
--
ALTER TABLE `vacunas`
  MODIFY `id_vacuna` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `vacunas_mascotas`
--
ALTER TABLE `vacunas_mascotas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `veterinarios`
--
ALTER TABLE `veterinarios`
  MODIFY `id_veterinario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alertas`
--
ALTER TABLE `alertas`
  ADD CONSTRAINT `alertas_ibfk_1` FOREIGN KEY (`id_dueno`) REFERENCES `duenos` (`id_dueno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `alertas_ibfk_2` FOREIGN KEY (`id_mascota`) REFERENCES `mascotas` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_cita_mascota` FOREIGN KEY (`id_mascota`) REFERENCES `mascotas` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_cita_veterinario` FOREIGN KEY (`id_veterinario`) REFERENCES `veterinarios` (`id_veterinario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD CONSTRAINT `consultas_ibfk_1` FOREIGN KEY (`id_cita`) REFERENCES `citas` (`id_cita`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `mascotas`
--
ALTER TABLE `mascotas`
  ADD CONSTRAINT `fk_mascota_dueno` FOREIGN KEY (`id_dueno`) REFERENCES `duenos` (`id_dueno`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `vacunas_mascotas`
--
ALTER TABLE `vacunas_mascotas`
  ADD CONSTRAINT `vacunas_mascotas_ibfk_1` FOREIGN KEY (`id_mascota`) REFERENCES `mascotas` (`id_mascota`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vacunas_mascotas_ibfk_2` FOREIGN KEY (`id_vacuna`) REFERENCES `vacunas` (`id_vacuna`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
