# servidor_chat_cifrado.py
from flask import Flask, request, jsonify
from collections import defaultdict

app = Flask(__name__)

# Mensajes en memoria: {receptor: [ {"mensaje": ..., "clave": ..., "hash": ...} ]}
bandejas = defaultdict(list)

@app.route("/send", methods=["POST"])
def enviar():
    data = request.json
    receptor = data.get("receptor")
    mensaje = data.get("mensaje")
    clave = data.get("clave")
    hash_mensaje = data.get("hash")

    if not receptor or not mensaje or not clave or not hash_mensaje:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    bandejas[receptor].append({
        "mensaje": mensaje,
        "clave": clave,
        "hash": hash_mensaje
    })
    return jsonify({"estado": "Mensaje enviado"}), 200

@app.route("/receive/<usuario>", methods=["GET"])
def recibir(usuario):
    mensajes = bandejas[usuario]
    bandejas[usuario] = []  # Limpiar bandeja después de enviar
    return jsonify(mensajes)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
