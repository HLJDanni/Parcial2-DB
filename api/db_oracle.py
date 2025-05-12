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