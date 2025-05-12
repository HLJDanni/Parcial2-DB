import oracledb
from flask import Flask, jsonify, request, render_template
from db_oracle import (
    get_asuntos, get_asunto, create_asunto, update_asunto, delete_asunto, get_cliente, create_cliente, update_cliente,
    delete_cliente, get_cliente, get_clientes, ORACLE_USER, ORACLE_PASSWORD, DSN
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
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)