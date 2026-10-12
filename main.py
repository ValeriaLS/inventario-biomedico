from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
import uuid
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# Cargar variables de entorno
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "inventario_biomedico")

if not MONGODB_URL:
    raise RuntimeError("Falta configurar MONGODB_URL en el archivo .env")

# Conexión con MongoDB
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
equipos_collection = database["equipos"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()


app = FastAPI(
    title="API de Inventario Biomédico",
    description="Sistema para gestionar equipos biomédicos",
    version="1.0.0",
    lifespan=lifespan
)

#Conexión con los archivos de la interfaz
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# Modelo de datos con validaciones estrictas
class Equipo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=1, max_length=100)
    marca: str = Field(min_length=1, max_length=100)
    modelo: str = Field(min_length=1, max_length=100)
    numero_serie: str = Field(min_length=1, max_length=100)
    ubicacion: str = Field(min_length=1, max_length=150)
    estado: str = "Disponible"

    @field_validator(
        "nombre",
        "marca",
        "modelo",
        "numero_serie",
        "ubicacion"
    )
    @classmethod
    def validar_textos(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo no puede estar vacío")

        return valor

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor: str) -> str:
        estados_permitidos = {
            "Disponible",
            "En mantenimiento",
            "Fuera de servicio"
        }

        valor = valor.strip()

        if valor not in estados_permitidos:
            raise ValueError(
                "El estado debe ser Disponible, "
                "En mantenimiento o Fuera de servicio"
            )

        return valor


# Verificar que la API funciona
@app.get("/")
async def inicio():
    return FileResponse(STATIC_DIR / "index.html")

# Registrar un equipo
@app.post("/equipos", status_code=201)
async def registrar_equipo(equipo: Equipo):
    existente = await equipos_collection.find_one({
        "numero_serie": equipo.numero_serie
    })

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un equipo con ese número de serie"
        )

    nuevo_equipo = equipo.model_dump()
    nuevo_equipo["id"] = str(uuid.uuid4())

    await equipos_collection.insert_one(nuevo_equipo)
    nuevo_equipo.pop("_id", None)

    return {
        "mensaje": "Equipo registrado correctamente",
        "equipo": nuevo_equipo
    }

# Consultar todos los equipos
@app.get("/equipos")
async def consultar_equipos():
    equipos = await equipos_collection.find(
        {},
        {"_id": 0}
    ).to_list(length=1000)

    return equipos


# Consultar un equipo por su identificador
@app.get("/equipos/{equipo_id}")
async def consultar_equipo(equipo_id: str):
    equipo = await equipos_collection.find_one(
        {"id": equipo_id},
        {"_id": 0}
    )

    if not equipo:
        raise HTTPException(
            status_code=404,
            detail="Equipo no encontrado"
        )

    return equipo


# Editar un equipo
@app.put("/equipos/{equipo_id}")
async def editar_equipo(equipo_id: str, equipo: Equipo):
    existente = await equipos_collection.find_one({
        "id": equipo_id
    })

    if not existente:
        raise HTTPException(
            status_code=404,
            detail="Equipo no encontrado"
        )

    duplicado = await equipos_collection.find_one({
        "numero_serie": equipo.numero_serie,
        "id": {"$ne": equipo_id}
    })

    if duplicado:
        raise HTTPException(
            status_code=409,
            detail="El número de serie ya pertenece a otro equipo"
        )

    await equipos_collection.update_one(
        {"id": equipo_id},
        {"$set": equipo.model_dump()}
    )

    return {
        "mensaje": "Equipo actualizado correctamente",
        "id": equipo_id
    }


# Eliminar un equipo
@app.delete("/equipos/{equipo_id}")
async def eliminar_equipo(equipo_id: str):
    resultado = await equipos_collection.delete_one({
        "id": equipo_id
    })

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Equipo no encontrado"
        )

    return {"mensaje": "Equipo eliminado correctamente"}



# Generar un reporte simulado de forma asíncrona
@app.post("/reportes/simulado")
async def generar_reporte():
    await asyncio.sleep(5)

    total = await equipos_collection.count_documents({})

    disponibles = await equipos_collection.count_documents({
        "estado": "Disponible"
    })

    mantenimiento = await equipos_collection.count_documents({
        "estado": "En mantenimiento"
    })

    fuera_de_servicio = await equipos_collection.count_documents({
        "estado": "Fuera de servicio"
    })

    return {
        "mensaje": "Reporte generado correctamente",
        "total_equipos": total,
        "disponibles": disponibles,
        "en_mantenimiento": mantenimiento,
        "fuera_de_servicio": fuera_de_servicio
    }
# Realizar un cálculo intensivo de CPU
def calcular_carga(numero: int) -> int:
    resultado = 0

    for i in range(numero):
        resultado += i * i

    return resultado


# Ejecutar el cálculo sin bloquear la API
@app.get("/procesamiento/cpu")
async def procesamiento_cpu(numero: int = 1000000):
    if numero < 1 or numero > 50000000:
        raise HTTPException(
            status_code=400,
            detail="El número debe estar entre 1 y 50000000"
        )

    resultado = await asyncio.to_thread(
        calcular_carga,
        numero
    )

    return {
        "mensaje": "Cálculo completado correctamente",
        "numero_iteraciones": numero,
        "resultado": resultado
    }