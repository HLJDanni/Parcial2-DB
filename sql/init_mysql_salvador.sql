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

USE sucursal_elsalvador; -- o sucursal_elsalvador

ALTER TABLE clientes ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE procuradores ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE abogados ADD COLUMN LAST_MODIFIED DATETIME;
ALTER TABLE asuntos ADD COLUMN LAST_MODIFIED DATETIME;
