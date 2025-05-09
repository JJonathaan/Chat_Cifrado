# descargar_clave_publica.py
import requests
import sys
import os


def descargar_clave(usuario, host="http://localhost:5001"):
    url = f"{host}/public_key/{usuario}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            nombre_archivo = f"clave_publica_{usuario}.pem"
            with open(nombre_archivo, "wb") as f:
                f.write(r.content)
            print(f" Clave pública de '{usuario}' guardada en '{nombre_archivo}'")
        else:
            print(f" Error {r.status_code}: {r.text}")
    except Exception as e:
        print(f" No se pudo conectar al servidor: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python descargar_clave_publica.py <usuario> [host]")
    else:
        usuario = sys.argv[1]
        host = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:5001"
        descargar_clave(usuario, host)