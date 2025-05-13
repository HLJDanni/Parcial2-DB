import oracledb
import os

ORACLE_USER = os.getenv("ORACLE_USER", "app_user")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "oracle123")
ORACLE_HOST = os.getenv("DB_ORACLE_HOST", "oracle-db")
ORACLE_PORT = os.getenv("DB_ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "XE")

DSN = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

def get_asuntos():
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.expediente_id, c.nombre as cliente, a.descripcion, a.estado, a.fecha_inicio, a.fecha_final
            FROM asuntos a
            JOIN clientes c ON a.cliente_id = c.cliente_id
            ORDER BY a.expediente_id
        """)
        rows = cursor.fetchall()
        cols = [d[0].lower() for d in cursor.description]
        asuntos = []
        for row in rows:
            row_dict = dict(zip(cols, row))
            # Convierte CLOB a string si es necesario
            if hasattr(row_dict['descripcion'], 'read'):
                row_dict['descripcion'] = row_dict['descripcion'].read()
            asuntos.append(row_dict)
        return asuntos



    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_asunto(expediente_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.expediente_id, a.cliente_id, c.nombre as cliente, a.descripcion, a.estado, a.fecha_inicio, a.fecha_final
            FROM asuntos a
            JOIN clientes c ON a.cliente_id = c.cliente_id
            WHERE a.expediente_id = :id
        """, {"id": expediente_id})
        row = cursor.fetchone()
        if row:
            cols = [d[0].lower() for d in cursor.description]
            return dict(zip(cols, row))
        return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

from datetime import datetime

def create_asunto(data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        # Convertir fechas si vienen como string
        fecha_inicio = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d").date()
        fecha_final = datetime.strptime(data['fecha_final'], "%Y-%m-%d").date()

        cursor.execute("""
            INSERT INTO asuntos (cliente_id, descripcion, estado, fecha_inicio, fecha_final)
            VALUES (:cliente_id, :descripcion, :estado, :fecha_inicio, :fecha_final)
        """, {
            "cliente_id": data["cliente_id"],
            "descripcion": data["descripcion"],
            "estado": data["estado"],
            "fecha_inicio": fecha_inicio,
            "fecha_final": fecha_final
        })
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()



def update_asunto(expediente_id, data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        # Convertir fechas desde string
        fecha_inicio = datetime.strptime(data['fecha_inicio'], "%Y-%m-%d").date()
        fecha_final = datetime.strptime(data['fecha_final'], "%Y-%m-%d").date()

        cursor.execute("""
            UPDATE asuntos
            SET cliente_id = :cliente_id,
                descripcion = :descripcion,
                estado = :estado,
                fecha_inicio = :fecha_inicio,
                fecha_final = :fecha_final
            WHERE expediente_id = :expediente_id
        """, {
            "cliente_id": data["cliente_id"],
            "descripcion": data["descripcion"],
            "estado": data["estado"],
            "fecha_inicio": fecha_inicio,
            "fecha_final": fecha_final,
            "expediente_id": expediente_id
        })
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()



def delete_asunto(expediente_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM asuntos WHERE expediente_id = :id", {"id": expediente_id})
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

#CLIENTES

def create_cliente(data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, direccion, telefono, correo)
            VALUES (:nombre, :direccion, :telefono, :correo)
        """, data)  # 'data' debe tener las claves adecuadas
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_clientes():
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("SELECT cliente_id, nombre, direccion, telefono, correo FROM clientes ORDER BY cliente_id")
        rows = cursor.fetchall()
        return [{"cliente_id": r[0], "nombre": r[1], "direccion": r[2], "telefono": r[3], "correo": r[4]} for r in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_cliente(cliente_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("SELECT cliente_id, nombre, direccion, telefono, correo FROM clientes WHERE cliente_id = :id", {"id": cliente_id})
        row = cursor.fetchone()
        if row:
            cols = [d[0].lower() for d in cursor.description]
            return dict(zip(cols, row))
        return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def update_cliente(cliente_id, data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre=:nombre, direccion=:direccion, telefono=:telefono, correo=:correo
            WHERE cliente_id=:cliente_id
        """, {**data, "cliente_id": cliente_id})
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def delete_cliente(cliente_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE cliente_id = :id", {"id": cliente_id})
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()


def get_abogados():
    """
    Obtiene todos los abogados de la base de datos
    :return: Lista de diccionarios con los abogados o diccionario de error
    """
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT abogado_id,
                              nombre,
                              dni,
                              pais,
                              correo,
                              TO_CHAR(last_modified, 'YYYY-MM-DD HH24:MI:SS') as last_modified
                       FROM abogados
                       ORDER BY nombre
                       """)

        # Convertir resultados a lista de diccionarios
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def create_abogado(data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        # Validar campos requeridos
        required_fields = ['nombre', 'dni', 'pais', 'correo']
        if not all(field in data for field in required_fields):
            return {"error": "Faltan campos requeridos"}

        # Preparar variable de salida
        abogado_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute("""
            INSERT INTO abogados (nombre, dni, pais, correo)
            VALUES (:nombre, :dni, :pais, :correo) 
            RETURNING abogado_id INTO :id
        """, {
            "nombre": data["nombre"],
            "dni": data["dni"],
            "pais": data["pais"],
            "correo": data["correo"],
            "id": abogado_id_var
        })

        # Obtener el ID insertado
        abogado_id = abogado_id_var.getvalue()
        if isinstance(abogado_id, list):
            abogado_id = abogado_id[0]
        abogado_id = int(abogado_id)

        conn.commit()
        return {"success": True, "abogado_id": abogado_id}

    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1:  # Violación de constraint única (DNI duplicado)
            return {"error": "El DNI ya está registrado"}
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()



def get_abogado(abogado_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT abogado_id, nombre, dni, pais, correo,
                   TO_CHAR(last_modified, 'YYYY-MM-DD HH24:MI:SS') as last_modified
            FROM abogados
            WHERE abogado_id = :id
        """, {"id": abogado_id})

        row = cursor.fetchone()
        if row:
            columns = [col[0].lower() for col in cursor.description]
            return dict(zip(columns, row))
        return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def update_abogado(abogado_id, data):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM abogados WHERE abogado_id = :id", {"id": abogado_id})
        if not cursor.fetchone():
            return {"error": "Abogado no encontrado"}

        cursor.execute("""
            UPDATE abogados
            SET nombre = :nombre, dni = :dni, pais = :pais, correo = :correo
            WHERE abogado_id = :abogado_id
        """, {**data, "abogado_id": abogado_id})

        conn.commit()
        return {"success": True}
    except oracledb.DatabaseError as e:
        error, = e.args
        return {"error": error.message}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()


def delete_abogado(abogado_id):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()

        # Verificar existencia primero (ya lo haces, correcto)
        cursor.execute("SELECT 1 FROM abogados WHERE abogado_id = :id", {"id": abogado_id})
        if not cursor.fetchone():
            return {"error": "Abogado no encontrado"}

        cursor.execute("DELETE FROM abogados WHERE abogado_id = :id", {"id": abogado_id})
        conn.commit()

        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()



#PROCURADORES

def get_procuradores():
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("SELECT procurador_id, nombre, dni, telefono, correo FROM procuradores ORDER BY nombre")
        rows = cursor.fetchall()
        return [{"procurador_id": r[0], "nombre": r[1], "dni": r[2], "telefono": r[3], "correo": r[4]} for r in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def get_procurador(procurador_id):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("SELECT procurador_id, nombre, dni, telefono, correo FROM procuradores WHERE procurador_id = :id", {"id": procurador_id})
        row = cursor.fetchone()
        if row:
            return {"procurador_id": row[0], "nombre": row[1], "dni": row[2], "telefono": row[3], "correo": row[4]}
        return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def create_procurador(data):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        procurador_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute("""
            INSERT INTO procuradores (nombre, dni, telefono, correo)
            VALUES (:nombre, :dni, :telefono, :correo)
            RETURNING procurador_id INTO :id
        """, {
            "nombre": data["nombre"],
            "dni": data["dni"],
            "telefono": data["telefono"],
            "correo": data["correo"],
            "id": procurador_id_var
        })
        procurador_id = procurador_id_var.getvalue()
        if isinstance(procurador_id, list):
            procurador_id = procurador_id[0]
        conn.commit()
        return {"procurador_id": int(procurador_id)}
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 1:
            return {"error": "El DNI ya está registrado"}
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def update_procurador(procurador_id, data):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE procuradores SET nombre = :nombre, dni = :dni, telefono = :telefono, correo = :correo
            WHERE procurador_id = :id
        """, {**data, "id": procurador_id})
        conn.commit()
        return {"updated": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def delete_procurador(procurador_id):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM procuradores WHERE procurador_id = :id", {"id": procurador_id})
        conn.commit()
        return {"deleted": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()




# ---------- BASE DE DATOS AUDIENCIA----------

def get_audiencias():
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT audiencia_id, expediente_id, abogado_id, procurador_id,
                   TO_CHAR(fecha_audiencia, 'YYYY-MM-DD"T"HH24:MI') as fecha_audiencia,
                   tipo, resultado, observaciones
            FROM audiencia
            ORDER BY fecha_audiencia DESC
        """)
        cols = [c[0].lower() for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def get_audiencia(audiencia_id):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT audiencia_id, expediente_id, abogado_id, procurador_id,
                   TO_CHAR(fecha_audiencia, 'YYYY-MM-DD"T"HH24:MI') as fecha_audiencia,
                   tipo, resultado, observaciones
            FROM audiencia
            WHERE audiencia_id = :id
        """, {"id": audiencia_id})
        row = cursor.fetchone()
        if row:
            cols = [c[0].lower() for c in cursor.description]
            return dict(zip(cols, row))
        return None
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def create_audiencia(data):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audiencia (expediente_id, abogado_id, procurador_id,
                                   fecha_audiencia, tipo, resultado, observaciones)
            VALUES (:expediente_id, :abogado_id, :procurador_id,
                    TO_TIMESTAMP(:fecha_audiencia, 'YYYY-MM-DD"T"HH24:MI'),
                    :tipo, :resultado, :observaciones)
        """, data)
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def update_audiencia(audiencia_id, data):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE audiencia
            SET expediente_id = :expediente_id,
                abogado_id = :abogado_id,
                procurador_id = :procurador_id,
                fecha_audiencia = TO_TIMESTAMP(:fecha_audiencia, 'YYYY-MM-DD"T"HH24:MI'),
                tipo = :tipo,
                resultado = :resultado,
                observaciones = :observaciones
            WHERE audiencia_id = :audiencia_id
        """, {**data, "audiencia_id": audiencia_id})
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

def delete_audiencia(audiencia_id):
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=DSN)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM audiencia WHERE audiencia_id = :id", {"id": audiencia_id})
        conn.commit()
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals(): conn.close()
