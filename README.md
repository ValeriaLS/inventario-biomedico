# Inventario Biomédico

## 1. Descripción del proyecto

Inventario Biomédico es una aplicación web diseñada para gestionar equipos biomédicos. Permite registrar, consultar, actualizar y eliminar equipos, además de generar reportes y ejecutar un proceso de cálculo intensivo.

El proyecto integra una API REST, persistencia de datos en la nube y una interfaz web que se comunica con el backend.

## 2. Objetivo

Desarrollar una aplicación web funcional que integre persistencia de datos en la nube, validación de datos, procesamiento asíncrono y concurrencia mediante tareas ejecutadas en un hilo secundario.

## 3. Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- MongoDB Atlas
- Motor para operaciones asíncronas con MongoDB
- HTML5
- CSS3
- JavaScript
- Uvicorn
- Git y GitHub

## 4. Funcionalidades

- Registrar equipos biomédicos.
- Consultar los equipos registrados.
- Consultar un equipo por su identificador.
- Actualizar la información de un equipo.
- Eliminar equipos.
- Validar los datos de entrada.
- Evitar registros con números de serie duplicados.
- Generar reportes del inventario.
- Ejecutar un cálculo intensivo mediante `asyncio.to_thread()`.
- Consultar la documentación interactiva de la API.

## 5. Estructura del proyecto

```text
inventario_biomedico/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── test_validaciones.py
├── probar_crud.py
├── probar_concurrencia.py
├── probar_mongodb.py
└── static/
    ├── index.html
    ├── styles.css
    └── app.js
```

## 6. Requisitos previos

Para ejecutar el proyecto se necesita:

- Python instalado.
- Una cuenta y una base de datos configurada en MongoDB Atlas.
- Git.
- Las dependencias indicadas en `requirements.txt`.

## 7. Configuración

### Clonar el repositorio

```bash
git clone https://github.com/ValeriaLS/inventario-biomedico.git
cd inventario-biomedico
```

### Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### Configurar las variables de entorno

Crear un archivo `.env` en la carpeta principal, tomando como referencia `.env.example`.

Configurar las variables necesarias:

```dotenv
MONGODB_URL=TU_CADENA_DE_CONEXION
DATABASE_NAME=inventario_biomedico
```

Sustituir `TU_CADENA_DE_CONEXION` por la cadena de conexión correspondiente a MongoDB Atlas.

No publicar el archivo `.env` ni compartir las credenciales de la base de datos.

## 8. Ejecutar la aplicación

Con el entorno virtual activado y las variables de entorno configuradas, ejecutar:

```powershell
uvicorn main:app --reload
```

La aplicación estará disponible localmente en:

- Aplicación web: `http://127.0.0.1:8000/`
- Documentación de la API: `http://127.0.0.1:8000/docs`

## 9. Endpoints principales

| Método | Endpoint | Función |
|---|---|---|
| POST | `/equipos` | Registrar un equipo |
| GET | `/equipos` | Consultar todos los equipos |
| GET | `/equipos/{equipo_id}` | Consultar un equipo específico |
| PUT | `/equipos/{equipo_id}` | Actualizar un equipo |
| DELETE | `/equipos/{equipo_id}` | Eliminar un equipo |
| POST | `/reportes/simulado` | Generar un reporte |
| GET | `/procesamiento/cpu` | Ejecutar el cálculo intensivo |

## 10. Procesamiento y concurrencia

El endpoint `/procesamiento/cpu` utiliza `asyncio.to_thread()` para ejecutar una función de cálculo síncrona en un hilo secundario, evitando que dicha función bloquee directamente el bucle de eventos de la aplicación.

El proyecto también incluye una prueba de concurrencia para comprobar que se pueden realizar solicitudes durante la ejecución del cálculo.

## 11. Pruebas

El proyecto incluye archivos destinados a comprobar las validaciones, las operaciones CRUD, la conexión con MongoDB y la concurrencia.

Para ejecutar las pruebas de validación:

```powershell
python -m pytest test_validaciones.py -v
```

Las demás pruebas se pueden ejecutar con sus respectivos archivos de Python.

## 12. Seguridad

- Las credenciales se configuran mediante variables de entorno.
- El archivo `.env` se excluye del repositorio mediante `.gitignore`.
- El archivo `.env.example` proporciona una referencia para configurar la aplicación sin exponer credenciales reales.

## 13. Autora

Desarrollado como proyecto académico de programación.