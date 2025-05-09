# 🛡️ Chat Cifrado Anónimo (Red Local)

Este proyecto implementa un sistema de **chat cifrado y anónimo** en red local usando Python, combinando técnicas de criptografía híbrida, compresión y verificación de integridad.

## Características

-  Envío y recepción de mensajes cifrados (RSA + Fernet)
-  Verificación de integridad con SHA-256
-  Compresión de mensajes con zlib
-  Claves públicas y privadas por usuario
-  Servidor Flask para reenviar mensajes
-  API para servir claves públicas
-  Emisores anónimos (UUID aleatorio por sesión)
-  Todo funciona en red local, sin conexión a internet

##  Estructura de componentes

| Archivo                  | Función |
|--------------------------|---------|
| `1_generarclaves.py`     | Generar claves públicas/privadas por usuario |
| `2_apiAnonima.py`        | Servidor Flask que expone claves públicas |
| `3_descargarClave.py`    | Cliente para descargar claves públicas de otros usuarios |
| `4_server.py`            | Servidor de mensajes cifrados |
| `5_client.py`            | Cliente CLI anónimo para enviar/recibir mensajes |
| `claves/`                | Carpeta donde se guardan las claves generadas |

##  Cómo usarlo

### 1. Genera claves para cada usuario

```bash
python 1_generarclaves.py alice
python 1_generarclaves.py bob
```

### 2. Inicia la API de claves públicas

```bash
python 2_apiAnonima.py
```

### 3. Inicia el servidor de mensajes

```bash
python 4_server.py
```

### 4. Descarga la clave pública del otro usuario

```bash
python 3_descargarClave.py bob
```

### 5. Ejecuta el cliente para chatear

```bash
python 5_client.py --usuario alice --destino bob --servidor http://localhost:5000
```

 Haz lo mismo en otra terminal para `bob` enviando a `alice`.

##  Mejoras futuras

- Añadir persistencia con SQLite o MongoDB
- Firmas digitales para autenticidad
- Cifrado de nombre de usuario para anonimato completo
- Interfaz gráfica (Tkinter o web)

##  Licencia

Este proyecto es libre para fines educativos y de aprendizaje.
