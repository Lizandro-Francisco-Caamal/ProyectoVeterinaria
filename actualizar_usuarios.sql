USE veterinaria;
CREATE TABLE IF NOT EXISTS usuarios(id_usuario INT AUTO_INCREMENT PRIMARY KEY,usuario VARCHAR(50) UNIQUE NOT NULL,password VARCHAR(64) NOT NULL,rol ENUM('administrador','recepcionista','veterinario','cliente') NOT NULL,activo TINYINT(1) DEFAULT 1);
INSERT IGNORE INTO usuarios(usuario,password,rol,activo) VALUES ('admin',SHA2('123456',256),'administrador',1),('recepcion',SHA2('123456',256),'recepcionista',1),('veterinario1',SHA2('123456',256),'veterinario',1),('cliente1',SHA2('123456',256),'cliente',1);
