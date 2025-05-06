import oracledb

def get_oracle_data():
    try:
        conn = oracledb.connect(
            user="system",
            password="oracle123",
            dsn="oracle_guatemala:1521/FREE"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asuntos")
        rows = cursor.fetchall()
        return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_cliente_data(id=None):
    try:
        conn = oracledb.connect(
            user="system",
            password="oracle123",
            dsn="oracle_guatemala:1521/FREE"
        )
        cursor = conn.cursor()
        if id:
            cursor.execute("SELECT * FROM clientes WHERE cliente_id = :id", {"id": id})
        else:
            cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_procurador_data(id=None):
    try:
        conn = oracledb.connect(
            user="system",
            password="oracle123",
            dsn="oracle_guatemala:1521/FREE"
        )
        cursor = conn.cursor()
        if id:
            cursor.execute("SELECT * FROM procuradores WHERE procurador_id = :id", {"id": id})
        else:
            cursor.execute("SELECT * FROM procuradores")
        rows = cursor.fetchall()
        return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def get_audiencia_data(id=None):
    try:
        conn = oracledb.connect(
            user="system",
            password="oracle123",
            dsn="oracle_guatemala:1521/FREE"
        )
        cursor = conn.cursor()
        if id:
            cursor.execute("SELECT * FROM audiencias WHERE audiencia_id = :id", {"id": id})
        else:
            cursor.execute("SELECT * FROM audiencias")
        rows = cursor.fetchall()
        return [dict(zip([d[0] for d in cursor.description], row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()
