-- Archivo: elsalvador.sql

-- Creación de la base de datos (si es necesario)
CREATE DATABASE IF NOT EXISTS sucursal_elsalvador;

USE sucursal_elsalvador;

-- Creación de las tablas
CREATE TABLE clientes (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE procuradores (
    procurador_id INT PRIMARY KEY,
    nombre VARCHAR(100),
    dni VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

CREATE TABLE abogados (
    abogado_id INT PRIMARY KEY,
    nombre VARCHAR(100),
    dni VARCHAR(20) UNIQUE,
    pais VARCHAR(50),
    correo VARCHAR(100)
);

CREATE TABLE asuntos (
    expediente_id INT PRIMARY KEY,
    cliente_id INT,
    descripcion TEXT,
    estado VARCHAR(50),
    fecha_inicio DATE,
    fecha_final DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

CREATE TABLE asunto_procurador (
    expediente_id INT,
    procurador_id INT,
    PRIMARY KEY (expediente_id, procurador_id),
    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id),
    FOREIGN KEY (procurador_id) REFERENCES procuradores(procurador_id)
);

CREATE TABLE audiencias (
    audiencia_id INT PRIMARY KEY,
    expediente_id INT,
    fecha DATE,
    abogado_id INT,
    observaciones TEXT,
    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id),
    FOREIGN KEY (abogado_id) REFERENCES abogados(abogado_id)
);

-- Inserción de datos ejemplo (ajustar a tus necesidades)
INSERT INTO clientes VALUES (1, 'Juan Pérez', 'San Salvador, El Salvador', '5555-1234', 'juanp@gmail.com');
INSERT INTO clientes VALUES (2, 'María López', 'Santa Tecla, El Salvador', '5555-6789', 'maria.lopez@hotmail.com');

INSERT INTO procuradores VALUES (1, 'Lic. Gómez', 'P001SV', '4444-5566', 'gomez@procuradores.com');
INSERT INTO procuradores VALUES (2, 'Lic. Rodríguez', 'P002SV', '6677-8899', 'rodriguez@procuradores.com');

INSERT INTO abogados VALUES (1, 'Dr. Salazar', 'A001GT', 'El Salvador', 'salazar@abogados.com');
INSERT INTO abogados VALUES (2, 'Dra. Morales', 'A002SV', 'El Salvador', 'morales@abogados.com');

INSERT INTO asuntos VALUES (1, 1, 'Demanda laboral', 'en trámite', '2023-01-10', NULL);
INSERT INTO asuntos VALUES (2, 2, 'Divorcio', 'finalizado', '2022-05-15', '2023-03-01');

INSERT INTO asunto_procurador VALUES (1, 1);
INSERT INTO asunto_procurador VALUES (1, 2);
INSERT INTO asunto_procurador VALUES (2, 2);

INSERT INTO audiencias VALUES (1, 1, '2023-05-01', 1, 'Primera audiencia con testigos.');
INSERT INTO audiencias VALUES (2, 2, '2023-07-10', 2, 'Cierre del caso.');
