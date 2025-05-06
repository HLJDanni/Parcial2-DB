from flask import Flask, jsonify, request
from db_oracle import get_oracle_data, get_cliente_data, get_procurador_data, get_audiencia_data
from db_mysql_mexico import get_mexico_data
from db_mysql_salvador import get_salvador_data

app = Flask(__name__)
app.config['DEBUG'] = True  # Activa el modo de depuración
@app.route("/")
def index():
    return "Microservicio Flask para replicación distribuida"

@app.route("/replicados", methods=["GET"])
def get_all_data():
    oracle = get_oracle_data()
    mexico = get_mexico_data()
    salvador = get_salvador_data()

    return jsonify({
        "guatemala_oracle": oracle,
        "mexico_mysql": mexico,
        "salvador_mysql": salvador
    })

# Endpoint para obtener todos los clientes
@app.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = get_cliente_data()
    return jsonify(clientes)

# Endpoint para obtener un cliente por ID
@app.route("/clientes/<int:id>", methods=["GET"])
def get_cliente(id):
    cliente = get_cliente_data(id)
    return jsonify(cliente)

# Endpoint para obtener todos los procuradores
@app.route("/procuradores", methods=["GET"])
def get_procuradores():
    procuradores = get_procurador_data()
    return jsonify(procuradores)

# Endpoint para obtener un procurador por ID
@app.route("/procuradores/<int:id>", methods=["GET"])
def get_procurador(id):
    procurador = get_procurador_data(id)
    return jsonify(procurador)

# Endpoint para obtener todas las audiencias
@app.route("/audiencias", methods=["GET"])
def get_audiencias():
    audiencias = get_audiencia_data()
    return jsonify(audiencias)

# Endpoint para obtener una audiencia por ID
@app.route("/audiencias/<int:id>", methods=["GET"])
def get_audiencia(id):
    audiencia = get_audiencia_data(id)
    return jsonify(audiencia)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)