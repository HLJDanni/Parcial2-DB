import oracledb
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


if __name__ == '__main__':
    app.run(debug=True)