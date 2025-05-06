import mysql.connector

def get_salvador_data():
    try:
        conn = mysql.connector.connect(
            host="mysql_salvador",
            user="root",
            password="root",
            database="legaldb",
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asuntos")
        rows = cursor.fetchall()
        return [dict(zip(cursor.column_names, row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
