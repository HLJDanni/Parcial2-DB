CREATE USER app_user IDENTIFIED BY oracle123;

GRANT CONNECT, RESOURCE TO app_user;
ALTER USER app_user QUOTA UNLIMITED ON USERS;
ALTER SESSION SET CURRENT_SCHEMA = app_user;

-- Tablas principales con columna LAST_MODIFIED
CREATE TABLE clientes (
    cliente_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100),
    direccion VARCHAR2(150),
    telefono VARCHAR2(20),
    correo VARCHAR2(100),
    LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE procuradores (
    procurador_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100),
    dni VARCHAR2(20) UNIQUE,
    telefono VARCHAR2(20),
    correo VARCHAR2(100),
    LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE abogados (
    abogado_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100),
    dni VARCHAR2(20) UNIQUE,
    pais VARCHAR2(50),
    correo VARCHAR2(100),
    LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE TABLE asuntos (
    expediente_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    cliente_id NUMBER,
    descripcion CLOB,
    estado VARCHAR2(50),
    fecha_inicio DATE,
    fecha_final DATE,
    LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id) ON DELETE CASCADE
);

CREATE TABLE audiencia (
    audiencia_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    expediente_id NUMBER NOT NULL,
    abogado_id NUMBER NOT NULL,
    procurador_id NUMBER,
    fecha_audiencia TIMESTAMP NOT NULL,
    tipo VARCHAR2(50) NOT NULL, -- Ej: 'Preliminar', 'Vista', 'Juicio'
    resultado VARCHAR2(200),
    observaciones VARCHAR2(500),
    LAST_MODIFIED TIMESTAMP DEFAULT SYSTIMESTAMP,
    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id) ON DELETE CASCADE,
    FOREIGN KEY (abogado_id) REFERENCES abogados(abogado_id),
    FOREIGN KEY (procurador_id) REFERENCES procuradores(procurador_id)
);

-- Tabla para registrar eliminaciones
CREATE TABLE deleted_records (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY,
    table_name VARCHAR2(50),
    record_id NUMBER,
    deletion_time TIMESTAMP,
    PRIMARY KEY (id)
);