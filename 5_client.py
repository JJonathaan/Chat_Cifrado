

# cliente_chat_cifrado.py (versión con argparse)
import requests
import zlib
import hashlib
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import os
import sys
CLAVES_DIR = "claves"
# -----------------------------
# Cargar clave pública del receptor

def cargar_clave_publica(destino):
    archivo = f"clave_publica_{destino}.pem"
    if not os.path.exists(archivo):
        print(f" No se encuentra la clave pública de {destino} ({archivo})")
        sys.exit(1)
    with open(archivo, "rb") as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

# -----------------------------
# Enviar mensaje cifrado

def enviar_mensaje(args):
    mensaje = input(" Mensaje a enviar: ").strip()
    if not mensaje:
        print(" Mensaje vacío")
        return

    # Comprimir y cifrar con Fernet
    comprimido = zlib.compress(mensaje.encode())
    clave_fernet = Fernet.generate_key()
    fernet = Fernet(clave_fernet)
    cifrado = fernet.encrypt(comprimido)
    hash_mensaje = hashlib.sha256(comprimido).hexdigest()

    # Encriptar clave Fernet con clave pública del receptor
    clave_pub = cargar_clave_publica(args.destino)
    clave_cifrada = clave_pub.encrypt(
        clave_fernet,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Enviar al servidor
    data = {
        "receptor": args.destino,
        "mensaje": base64.b64encode(cifrado).decode(),
        "clave": base64.b64encode(clave_cifrada).decode(),
        "hash": hash_mensaje
    }
    r = requests.post(f"{args.servidor}/send", json=data)
    print(f" Estado del envio: {r.status_code} {r.text}")

# -----------------------------
# Recibir y descifrar mensajes

def recibir_mensajes(args):
    archivo_clave_priv = os.path.join(CLAVES_DIR, f"clave_privada_{args.usuario}.pem")

    if not os.path.exists(archivo_clave_priv):
        print(" Clave privada local no encontrada")
        return

    with open(archivo_clave_priv, "rb") as f:
        clave_privada = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    r = requests.get(f"{args.servidor}/receive/{args.usuario}")
    mensajes = r.json()
    if not mensajes:
        print(" No hay mensajes nuevos.")
        return

    print(f" {len(mensajes)} mensaje(s) nuevo(s):")
    for i, msg in enumerate(mensajes, 1):
        try:
            cifrado = base64.b64decode(msg["mensaje"])
            clave_cifrada = base64.b64decode(msg["clave"])
            hash_original = msg["hash"]

            clave_fernet = clave_privada.decrypt(
                clave_cifrada,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            fernet = Fernet(clave_fernet)
            comprimido = fernet.decrypt(cifrado)
            hash_actual = hashlib.sha256(comprimido).hexdigest()

            if hash_actual != hash_original:
                print(f"{i}.  Hash no coincide. Mensaje puede estar dañado.")
                continue

            texto = zlib.decompress(comprimido).decode()
            print(f"{i}.  {texto}")
        except Exception as e:
            print(f"{i}.  Error al procesar mensaje: {e}")

# -----------------------------
# Menú interactivo con argparse

def main():
    parser = argparse.ArgumentParser(description="Cliente de chat cifrado")
    parser.add_argument("--usuario", required=True, help="Tu nombre de usuario")
    parser.add_argument("--destino", required=True, help="Usuario receptor")
    parser.add_argument("--servidor", default="http://localhost:5000", help="URL del servidor")
    args = parser.parse_args()

    print(f"\n💬 CLIENTE DE CHAT CIFRADO ({args.usuario})")
    while True:
        print("\n1. Enviar mensaje")
        print("2. Recibir mensajes")
        print("0. Salir")
        op = input("Elige una opción: ")

        if op == "1":
            enviar_mensaje(args)
        elif op == "2":
            recibir_mensajes(args)
        elif op == "0":
            print(" Saliendo...")
            break
        else:
            print(" Opcion invalida")

if __name__ == "__main__":
    main()