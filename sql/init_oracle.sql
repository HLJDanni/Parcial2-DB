CREATE USER app_user IDENTIFIED BY oracle123;

GRANT CONNECT, RESOURCE TO app_user;

--  Asignar espacio en el tablespace USERS
ALTER USER app_user QUOTA UNLIMITED ON USERS;

ALTER SESSION SET CURRENT_SCHEMA = app_user;
CREATE TABLE asuntos (
    expediente_id NUMBER PRIMARY KEY,
    cliente_nombre VARCHAR2(100),
    descripcion CLOB,
    estado VARCHAR2(50),
    fecha_inicio DATE,
    fecha_final DATE
);

INSERT INTO asuntos (expediente_id, cliente_nombre, descripcion, estado, fecha_inicio, fecha_final) VALUES
(1, 'Juan Pérez', 'Demanda laboral', 'en trámite', TO_DATE('2023-01-10', 'YYYY-MM-DD'), NULL);

INSERT INTO asuntos (expediente_id, cliente_nombre, descripcion, estado, fecha_inicio, fecha_final) VALUES
(2, 'María López', 'Divorcio', 'finalizado', TO_DATE('2022-05-15', 'YYYY-MM-DD'), TO_DATE('2023-03-01', 'YYYY-MM-DD'));

INSERT INTO asuntos (expediente_id, cliente_nombre, descripcion, estado, fecha_inicio, fecha_final) VALUES
(3, 'Carlos Méndez', 'Amparo constitucional', 'amparo provisional', TO_DATE('2024-02-20', 'YYYY-MM-DD'), NULL);

CREATE TABLE clientes (
    cliente_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    direccion VARCHAR2(150),
    telefono VARCHAR2(20),
    correo VARCHAR2(100)
);

CREATE TABLE procuradores (
    procurador_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    dni VARCHAR2(20) UNIQUE,
    telefono VARCHAR2(20),
    correo VARCHAR2(100)
);

CREATE TABLE abogados (
    abogado_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100),
    dni VARCHAR2(20) UNIQUE,
    pais VARCHAR2(50),
    correo VARCHAR2(100)
);

CREATE TABLE asuntos (
    expediente_id NUMBER PRIMARY KEY,
    cliente_id NUMBER,
    descripcion CLOB,
    estado VARCHAR2(50),
    fecha_inicio DATE,
    fecha_final DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

CREATE TABLE asunto_procurador (
    expediente_id NUMBER,
    procurador_id NUMBER,
    PRIMARY KEY (expediente_id, procurador_id),
    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id),
    FOREIGN KEY (procurador_id) REFERENCES procuradores(procurador_id)
);

CREATE TABLE audiencias (
    audiencia_id NUMBER PRIMARY KEY,
    expediente_id NUMBER,
    fecha DATE,
    abogado_id NUMBER,
    observaciones CLOB,
    FOREIGN KEY (expediente_id) REFERENCES asuntos(expediente_id),
    FOREIGN KEY (abogado_id) REFERENCES abogados(abogado_id)
);


INSERT INTO clientes VALUES (1, 'Juan Pérez', 'Zona 10, Guatemala', '5555-1234', 'juanp@gmail.com');
INSERT INTO clientes VALUES (2, 'María López', 'CDMX, México', '5566-7788', 'maria.lopez@hotmail.com');

INSERT INTO procuradores VALUES (1, 'Lic. Gómez', 'P001GT', '4444-5566', 'gomez@procuradores.com');
INSERT INTO procuradores VALUES (2, 'Lic. Rodríguez', 'P002MX', '6677-8899', 'rodriguez@procuradores.com');

INSERT INTO abogados VALUES (1, 'Dr. Salazar', 'A001GT', 'Guatemala', 'salazar@abogados.com');
INSERT INTO abogados VALUES (2, 'Dra. Morales', 'A002SV', 'El Salvador', 'morales@abogados.com');

INSERT INTO asuntos VALUES (1, 1, 'Demanda laboral', 'en trámite', TO_DATE('2023-01-10', 'YYYY-MM-DD'), NULL);
INSERT INTO asuntos VALUES (2, 2, 'Divorcio', 'finalizado', TO_DATE('2022-05-15', 'YYYY-MM-DD'), TO_DATE('2023-03-01', 'YYYY-MM-DD'));

INSERT INTO asunto_procurador VALUES (1, 1);
INSERT INTO asunto_procurador VALUES (1, 2);
INSERT INTO asunto_procurador VALUES (2, 2);

INSERT INTO audiencias VALUES (1, 1, TO_DATE('2023-05-01', 'YYYY-MM-DD'), 1, 'Primera audiencia con testigos.');
INSERT INTO audiencias VALUES (2, 2, TO_DATE('2023-07-10', 'YYYY-MM-DD'), 2, 'Cierre del caso.');
