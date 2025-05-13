import oracledb

import mysql.connector
from flask import Flask, jsonify, request, render_template
from db_oracle import (
    get_asuntos, get_asunto, create_asunto, update_asunto, delete_asunto, get_cliente, create_cliente, update_cliente,
    delete_cliente, get_cliente, get_clientes, get_abogados, get_abogado,
    create_abogado, update_abogado, delete_abogado, get_procuradores, get_procurador, create_procurador,
    update_procurador, delete_procurador, get_audiencias, get_audiencia, create_audiencia, update_audiencia,
    delete_audiencia
)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/SedeCentral.html")
def sede_central():
    return render_template("SedeCentral.html")

@app.route("/AS_Guatemala.html")
def asuntos_guatemala():
    return render_template("AS_Guatemala.html")

@app.route("/Clientes.html")
def clientes():
    return render_template("Clientes.html")


@app.route("/Abogados.html")
def abogados():
    return render_template("Abogados.html")

@app.route("/Procuradores.html")
def procuradores():
    return render_template("Procuradores.html")

@app.route("/Audiencias.html")
def audiencias():
    return render_template("Audiencias.html")

@app.route("/SedeMéxico.html")
def sede_mexico():
        return render_template("SedeMéxico.html")

@app.route("/SedeElSalvador.html")
def sede_elsalvador():
        return render_template("SedeElSalvador.html")

# API para AS_Guatemala.html
@app.route("/api/asuntos", methods=["GET"])
def api_get_asuntos():
    return jsonify(get_asuntos())

@app.route("/api/asuntos/<int:expediente_id>", methods=["GET"])
def api_get_asunto(expediente_id):
    asunto = get_asunto(expediente_id)
    return jsonify(asunto) if asunto else jsonify({"error": "No encontrado"}), 404

@app.route("/api/asuntos", methods=["POST"])
def api_create_asunto():
    data = request.json
    result = create_asunto(data)
    return jsonify(result)

@app.route("/api/asuntos/<int:expediente_id>", methods=["PUT"])
def api_update_asunto(expediente_id):
    data = request.json
    result = update_asunto(expediente_id, data)
    return jsonify(result)

@app.route("/api/asuntos/<int:expediente_id>", methods=["DELETE"])
def api_delete_asunto(expediente_id):
    result = delete_asunto(expediente_id)
    return jsonify(result)

@app.route("/api/clientes", methods=["GET"])
def api_get_clientes():
    return jsonify(get_clientes())  # Correcto: obtiene todos los clientes


@app.route("/api/clientes", methods=["POST"])
def api_create_cliente():
    data = request.json  # Asegúrate de usar JSON
    if not data:
        return jsonify({"error": "Datos no proporcionados"}), 400

    # Verifica que los datos tengan las claves necesarias
    required_keys = ["nombre", "direccion", "telefono", "correo"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    return create_cliente(data)  # Pasa el data a la función


@app.route("/api/clientes/<int:cliente_id>", methods=["GET"])
def api_get_cliente(cliente_id):
    cliente = get_cliente(cliente_id)  # Correcto: obtiene un cliente por ID
    return jsonify(cliente) if cliente else jsonify({"error": "No encontrado"}), 404
@app.route("/api/clientes/<int:cliente_id>", methods=["PUT"])
def api_update_cliente(cliente_id):
    data = request.json
    result = update_cliente(cliente_id, data)
    return jsonify(result)

@app.route("/api/clientes/<int:cliente_id>", methods=["DELETE"])
def api_delete_cliente(cliente_id):
    result = delete_cliente(cliente_id)
    return jsonify(result)

# RUTAS ABOGADOS
@app.route('/api/abogados', methods=['GET'])
def list_abogados():
        try:
            result = get_abogados()
            if isinstance(result, list):
                return jsonify({"data": result, "success": True}), 200
            return jsonify({"error": result.get("error", "Error al obtener abogados"), "success": False}), 500
        except Exception as e:
            return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/abogados/<int:abogado_id>', methods=['GET'])
def get_abogado_route(abogado_id):
        try:
            abogado = get_abogado(abogado_id)
            if abogado is None:
                return jsonify({"error": "Abogado no encontrado", "success": False}), 404
            if isinstance(abogado, dict) and 'error' in abogado:
                return jsonify({"error": abogado["error"], "success": False}), 400
            return jsonify({"data": abogado, "success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/abogados', methods=['POST'])
def create_abogado_route():
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type debe ser application/json", "success": False}), 400

            data = request.get_json()

            required_fields = ['nombre', 'dni', 'pais', 'correo']
            if not all(field in data for field in required_fields):
                return jsonify({
                    "error": f"Faltan campos requeridos: {required_fields}",
                    "received": list(data.keys()),
                    "success": False
                }), 400

            result = create_abogado(data)
            if 'error' in result:
                return jsonify({"error": result["error"], "success": False}), 400
            return jsonify({"data": result, "success": True}), 201
        except Exception as e:
            return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/abogados/<int:abogado_id>', methods=['PUT'])
def update_abogado_route(abogado_id):
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type debe ser application/json", "success": False}), 400

            data = request.get_json()
            if not data:
                return jsonify({"error": "No se proporcionaron datos para actualizar", "success": False}), 400

            result = update_abogado(abogado_id, data)
            if 'error' in result:
                return jsonify({"error": result["error"], "success": False}), 400
            return jsonify({"data": result, "success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/abogados/<int:abogado_id>', methods=['DELETE'])
def delete_abogado_route(abogado_id):
        try:
            result = delete_abogado(abogado_id)
            if 'error' in result:
                if result['error'] == "Abogado no encontrado":
                    return jsonify({"error": result["error"], "success": False}), 404
                return jsonify({"error": result["error"], "success": False}), 400
            return jsonify({"data": result, "success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e), "success": False}), 500

#APIS PROCURADORES
@app.route('/api/procuradores', methods=['GET'])
def list_procuradores():
    result = get_procuradores()
    if isinstance(result, list):
        return jsonify({"data": result, "success": True}), 200
    return jsonify({"error": result.get("error", "Error al obtener procuradores"), "success": False}), 500

@app.route('/api/procuradores/<int:procurador_id>', methods=['GET'])
def get_procurador_route(procurador_id):
    result = get_procurador(procurador_id)
    if result is None:
        return jsonify({"error": "No encontrado", "success": False}), 404
    return jsonify({"data": result, "success": True})

@app.route('/api/procuradores', methods=['POST'])
def create_procurador_route():
    data = request.get_json()
    result = create_procurador(data)
    if 'error' in result:
        return jsonify({"error": result["error"], "success": False}), 400
    return jsonify({"data": result, "success": True}), 201

@app.route('/api/procuradores/<int:procurador_id>', methods=['PUT'])
def update_procurador_route(procurador_id):
    data = request.get_json()
    result = update_procurador(procurador_id, data)
    if 'error' in result:
        return jsonify({"error": result["error"], "success": False}), 400
    return jsonify({"data": result, "success": True})

@app.route('/api/procuradores/<int:procurador_id>', methods=['DELETE'])
def delete_procurador_route(procurador_id):
    result = delete_procurador(procurador_id)
    if 'error' in result:
        return jsonify({"error": result["error"], "success": False}), 400
    return jsonify({"data": result, "success": True})


@app.route("/api/audiencias", methods=["GET"])
def api_get_audiencias():
    return jsonify(get_audiencias())

@app.route("/api/audiencias/<int:audiencia_id>", methods=["GET"])
def api_get_audiencia(audiencia_id):
    data = get_audiencia(audiencia_id)
    return jsonify(data) if data else (jsonify({"error": "No encontrado"}), 404)

@app.route("/api/audiencias", methods=["POST"])
def api_create_audiencia():
    data = request.get_json()
    return jsonify(create_audiencia(data))

@app.route("/api/audiencias/<int:audiencia_id>", methods=["PUT"])
def api_update_audiencia(audiencia_id):
    data = request.get_json()
    return jsonify(update_audiencia(audiencia_id, data))

@app.route("/api/audiencias/<int:audiencia_id>", methods=["DELETE"])
def api_delete_audiencia(audiencia_id):
    return jsonify(delete_audiencia(audiencia_id))




#FUNCI[ON UNION

@app.route('/clientesGlobales.html')
def unionclientes_page():
    return render_template("clientesGlobales.html")

@app.route('/abogadosGlobales.html')
def unionabogados_page():
    return render_template("abogadosGlobales.html")

@app.route('/asuntosGloables.html')
def unionasuntos_page():
    return render_template("asuntosGlobales.html")

@app.route('/procuradoresGlobales.html')
def unionprocurados_page():
    return render_template("procuradoresGlobales.html")

@app.route('/audienciasGlobales.html')
def unionaudiencias_page():
    return render_template("audienciasGlobales.html")

@app.route('/combined_tables.html')
def union_page():
    return render_template("combined_tables.html")




# Configuración de conexiones (importa tus configuraciones desde los respectivos archivos)
from db_mysql_mexico import mysql_config_mexico
from db_mysql_salvador import mysql_config_salvador
import os
ORACLE_USER = os.getenv("ORACLE_USER", "app_user")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "oracle123")
ORACLE_HOST = os.getenv("DB_ORACLE_HOST", "oracle-db")
ORACLE_PORT = os.getenv("DB_ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "XE")

DSN = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"
# Definición de funciones para ejecutar consultas
def execute_oracle_query(query):
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DSN
        )
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [d[0].lower() for d in cursor.description]
        results = []
        for row in rows:
            row_dict = dict(zip(cols, row))
            # Convierte CLOB a string si es necesario
            if hasattr(row_dict.get('descripcion'), 'read'):
                row_dict['descripcion'] = row_dict['descripcion'].read()
            results.append(row_dict)
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

def execute_mysql_query(config, query):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Rutas para cada tabla combinada
@app.route('/clientes-globales')
def clientes_globales():
    return render_template('clientesGlobales.html')

@app.route('/combined/clientes')
def combined_clientes():
    # Consulta Oracle
    oracle_query = """
        SELECT 'Sede Central' as fuente, cliente_id, nombre, direccion, telefono, correo,
        TO_CHAR(LAST_MODIFIED, 'YYYY-MM-DD HH24:MI:SS') as ultima_modificacion
        FROM clientes
    """
    oracle_data = execute_oracle_query(oracle_query)

    # Consulta MySQL El Salvador
    mysql_sv_query = """
        SELECT 'Sucursal El Salvador' as fuente, cliente_id, nombre, direccion, telefono, correo,
        DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
        FROM clientes
    """
    mysql_sv_data = execute_mysql_query(mysql_config_salvador, mysql_sv_query)

    # Consulta MySQL México
    mysql_mx_query = """
        SELECT 'Sucursal México' as fuente, cliente_id, nombre, direccion, telefono, correo,
        DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
        FROM clientes
    """
    mysql_mx_data = execute_mysql_query(mysql_config_mexico, mysql_mx_query)

    # Combinar todo
    combined_data = oracle_data + mysql_sv_data + mysql_mx_data
    return jsonify(combined_data)






# Rutas para cada tabla combinada
@app.route('/combined/procuradores')
def combined_procuradores():
    oracle_query = """
                   SELECT 'Sede Central' as fuente, procurador_id, nombre, dni, telefono, correo,
                   TO_CHAR(LAST_MODIFIED, 'YYYY-MM-DD HH24:MI:SS') as ultima_modificacion
                   FROM procuradores
                   """
    oracle_data = execute_oracle_query(oracle_query)

    mysql_sv_query = """
                     SELECT 'Sucursal El Salvador' as fuente, procurador_id, nombre, dni, telefono, correo,
                     DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM procuradores
                     """
    mysql_sv_data = execute_mysql_query(mysql_config_salvador, mysql_sv_query)

    mysql_mx_query = """
                     SELECT 'Sucursal México' as fuente, procurador_id, nombre, dni, telefono, correo,
                     DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM procuradores
                     """
    mysql_mx_data = execute_mysql_query(mysql_config_mexico, mysql_mx_query)

    combined_data = oracle_data + mysql_sv_data + mysql_mx_data
    return render_template('procuradoresGlobales.html',
                           data=combined_data,
                           title="Procuradores Combinados",
                           columns=["fuente", "procurador_id", "nombre", "dni", "telefono", "correo", "ultima_modificacion"],
                           headers=["Fuente", "ID", "Nombre", "DNI", "Teléfono", "Correo", "Última Modificación"])

@app.route('/combined/abogados')
def combined_abogados():
    oracle_query = """
                   SELECT 'Sede Central' as fuente, abogado_id, nombre, dni, pais, correo,
                   TO_CHAR(LAST_MODIFIED, 'YYYY-MM-DD HH24:MI:SS') as ultima_modificacion
                   FROM abogados
                   """
    oracle_data = execute_oracle_query(oracle_query)

    mysql_sv_query = """
                     SELECT 'Sucursal El Salvador' as fuente, abogado_id, nombre, dni, pais, correo,
                     DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM abogados
                     """
    mysql_sv_data = execute_mysql_query(mysql_config_salvador, mysql_sv_query)

    mysql_mx_query = """
                     SELECT 'Sucursal México' as fuente, abogado_id, nombre, dni, pais, correo,
                     DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM abogados
                     """
    mysql_mx_data = execute_mysql_query(mysql_config_mexico, mysql_mx_query)

    combined_data = oracle_data + mysql_sv_data + mysql_mx_data
    return render_template('abogadosGlobales.html',
                           data=combined_data,
                           title="Abogados Combinados",
                           columns=["fuente", "abogado_id", "nombre", "dni", "pais", "correo", "ultima_modificacion"],
                           headers=["Fuente", "ID", "Nombre", "DNI", "País", "Correo", "Última Modificación"])

@app.route('/combined/asuntos')
def combined_asuntos():
    oracle_query = """
                   SELECT 'Sede Central' as fuente, expediente_id, cliente_id,
                          SUBSTR(descripcion, 1, 100) || CASE WHEN LENGTH(descripcion) > 100 THEN '...' ELSE '' END as descripcion,
                          estado, TO_CHAR(fecha_inicio, 'YYYY-MM-DD') as fecha_inicio,
                          TO_CHAR(fecha_final, 'YYYY-MM-DD') as fecha_final,
                          TO_CHAR(LAST_MODIFIED, 'YYYY-MM-DD HH24:MI:SS') as ultima_modificacion
                   FROM asuntos
                   """
    oracle_data = execute_oracle_query(oracle_query)

    mysql_sv_query = """
                     SELECT 'Sucursal El Salvador' as fuente, expediente_id, cliente_id,
                            CONCAT(SUBSTRING(descripcion, 1, 100), IF(LENGTH(descripcion) > 100, '...', '')) as descripcion,
                            estado, DATE_FORMAT(fecha_inicio, '%Y-%m-%d') as fecha_inicio,
                            DATE_FORMAT(fecha_final, '%Y-%m-%d') as fecha_final,
                            DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM asuntos
                     """
    mysql_sv_data = execute_mysql_query(mysql_config_salvador, mysql_sv_query)

    mysql_mx_query = """
                     SELECT 'Sucursal México' as fuente, expediente_id, cliente_id,
                            CONCAT(SUBSTRING(descripcion, 1, 100), IF(LENGTH(descripcion) > 100, '...', '')) as descripcion,
                            estado, DATE_FORMAT(fecha_inicio, '%Y-%m-%d') as fecha_inicio,
                            DATE_FORMAT(fecha_final, '%Y-%m-%d') as fecha_final,
                            DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM asuntos
                     """
    mysql_mx_data = execute_mysql_query(mysql_config_mexico, mysql_mx_query)

    combined_data = oracle_data + mysql_sv_data + mysql_mx_data
    return render_template('asuntosGlobales.html',
                           data=combined_data,
                           title="Asuntos Combinados",
                           columns=["fuente", "expediente_id", "cliente_id", "descripcion", "estado", "fecha_inicio", "fecha_final", "ultima_modificacion"],
                           headers=["Fuente", "Expediente ID", "Cliente ID", "Descripción", "Estado", "Fecha Inicio", "Fecha Final", "Última Modificación"])

@app.route('/combined/audiencias')
def combined_audiencias():
    oracle_query = """
                   SELECT 'Sede Central' as fuente, audiencia_id, expediente_id, abogado_id, procurador_id,
                          TO_CHAR(fecha_audiencia, 'YYYY-MM-DD HH24:MI:SS') as fecha_audiencia,
                          tipo, resultado,
                          SUBSTR(observaciones, 1, 50) || CASE WHEN LENGTH(observaciones) > 50 THEN '...' ELSE '' END as observaciones,
                          TO_CHAR(LAST_MODIFIED, 'YYYY-MM-DD HH24:MI:SS') as ultima_modificacion
                   FROM audiencia
                   """
    oracle_data = execute_oracle_query(oracle_query)

    mysql_sv_query = """
                     SELECT 'Sucursal El Salvador' as fuente, audiencia_id, expediente_id, abogado_id, procurador_id,
                            DATE_FORMAT(fecha_audiencia, '%Y-%m-%d %H:%i:%s') as fecha_audiencia,
                            tipo, resultado,
                            CONCAT(SUBSTRING(observaciones, 1, 50), IF(LENGTH(observaciones) > 50, '...', '')) as observaciones,
                            DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM audiencia
                     """
    mysql_sv_data = execute_mysql_query(mysql_config_salvador, mysql_sv_query)

    mysql_mx_query = """
                     SELECT 'Sucursal México' as fuente, audiencia_id, expediente_id, abogado_id, procurador_id,
                            DATE_FORMAT(fecha_audiencia, '%Y-%m-%d %H:%i:%s') as fecha_audiencia,
                            tipo, resultado,
                            CONCAT(SUBSTRING(observaciones, 1, 50), IF(LENGTH(observaciones) > 50, '...', '')) as observaciones,
                            DATE_FORMAT(LAST_MODIFIED, '%Y-%m-%d %H:%i:%s') as ultima_modificacion
                     FROM audiencia
                     """
    mysql_mx_data = execute_mysql_query(mysql_config_mexico, mysql_mx_query)

    combined_data = oracle_data + mysql_sv_data + mysql_mx_data
    return render_template('audienciasGlobales.html',
                           data=combined_data,
                           title="Audiencias Combinadas",
                           columns=["fuente", "audiencia_id", "expediente_id", "abogado_id", "procurador_id", "fecha_audiencia", "tipo", "resultado", "observaciones", "ultima_modificacion"],
                           headers=["Fuente", "Audiencia ID", "Expediente ID", "Abogado ID", "Procurador ID", "Fecha Audiencia", "Tipo", "Resultado", "Observaciones", "Última Modificación"])

if __name__ == '__main__':
    app.run(debug=True)