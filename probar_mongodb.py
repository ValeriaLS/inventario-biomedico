import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la cadena de conexión
uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError(
        "No se encontró MONGODB_URI en el archivo .env"
    )

try:
    # Conectar con MongoDB Atlas
    cliente = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )

    # Comprobar la conexión
    print("Respuesta de MongoDB:", cliente.admin.command("ping"))

    # Seleccionar la base de datos
    db = cliente["inventario_biomedico"]

    # Seleccionar la colección
    coleccion = db["productos"]

    # Mostrar las colecciones disponibles
    print("Colecciones:", db.list_collection_names())

    # Contar los documentos existentes
    print("Cantidad de productos:", coleccion.count_documents({}))

    print("¡Conexión y acceso a la base de datos exitosos!")

except Exception as error:
    print("Ocurrió un error:", error)

finally:
    if "cliente" in locals():
        cliente.close()