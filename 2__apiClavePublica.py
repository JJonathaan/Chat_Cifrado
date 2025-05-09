# Extensión para el servidor: api_clave_publica.py
from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

CLAVES_DIR = "claves"  # Directorio donde están almacenadas las claves públicas

@app.route("/public_key/<usuario>", methods=["GET"])
def obtener_clave_publica(usuario):
    ruta = os.path.join(CLAVES_DIR, f"clave_publica_{usuario}.pem")
    if not os.path.exists(ruta):
        return jsonify({"error": "Clave pública no encontrada"}), 404
    return send_file(ruta, mimetype="application/x-pem-file")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
