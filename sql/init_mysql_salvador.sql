-- Archivo: elsalvador.sql

-- Creación de la base de datos (si es necesario)
CREATE DATABASE IF NOT EXISTS sucursal_elsalvador;

USE sucursal_elsalvador;
CREATE TABLE clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE procuradores (
    procurador_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    dni VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE abogados (
    abogado_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    dni VARCHAR(20) UNIQUE,
    pais VARCHAR(50),
    correo VARCHAR(100)
);

CREATE TABLE asuntos (
    expediente_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    descripcion TEXT,
    estado VARCHAR(50),
    fecha_inicio DATE,
    fecha_final DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id) ON DELETE CASCADE
);

CREATE TABLE audiencia (
    audiencia_id INT AUTO_INCREMENT PRIMARY KEY,
    expediente_id INT NOT NULL,
    abogado_id INT NOT NULL,
    procurador_id INT,
    fecha_audiencia TIMESTAMP NOT NULL,
    tipo VARCHAR(50) NOT NULL COMMENT 'Ej: Preliminar, Vista, Juicio',
    resultado VARCHAR(200),
    observaciones VARCHAR(500),

    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id) ON DELETE CASCADE,
    FOREIGN KEY (abogado_id) REFERENCES abogados(abogado_id),
    FOREIGN KEY (procurador_id) REFERENCES procuradores(procurador_id)
);

USE sucursal_elsalvador; -- o sucursal_elsalvador

ALTER TABLE clientes ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE procuradores ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE abogados ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE asuntos ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE audiencia ADD COLUMN LAST_MODIFIED DATETIME;
