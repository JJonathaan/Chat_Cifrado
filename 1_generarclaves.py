# generar_claves_usuario.py
import os
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

CARPETA_CLAVES = "claves"


def generar_claves(usuario):
    # Crear carpeta si no existe
    os.makedirs(CARPETA_CLAVES, exist_ok=True)

    priv_path = os.path.join(CARPETA_CLAVES, f"clave_privada_{usuario}.pem")
    pub_path = os.path.join(CARPETA_CLAVES, f"clave_publica_{usuario}.pem")

    if os.path.exists(priv_path) or os.path.exists(pub_path):
        print(f"⚠️ Las claves para '{usuario}' ya existen en la carpeta '{CARPETA_CLAVES}'. Borra los archivos si deseas regenerarlas.")
        return

    print(f"🔐 Generando claves RSA para '{usuario}'...")
    clave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    clave_publica = clave_privada.public_key()

    with open(priv_path, "wb") as f:
        f.write(clave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(pub_path, "wb") as f:
        f.write(clave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"✅ Claves generadas y guardadas en '{CARPETA_CLAVES}':")
    print(f"  - {priv_path}")
    print(f"  - {pub_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de claves RSA para usuarios")
    parser.add_argument("usuario", help="Nombre del usuario para quien generar las claves")
    args = parser.parse_args()

    generar_claves(args.usuario)