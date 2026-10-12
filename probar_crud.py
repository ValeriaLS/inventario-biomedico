import asyncio
import uuid
import httpx

URL = "http://127.0.0.1:8000"


async def probar_crud():
    async with httpx.AsyncClient(timeout=30) as cliente:

        numero_serie = f"TEST-{uuid.uuid4().hex[:8]}"

        equipo = {
            "nombre": "Monitor de signos vitales",
            "marca": "Philips",
            "modelo": "MX450",
            "numero_serie": numero_serie,
            "ubicacion": "Laboratorio",
            "estado": "Disponible"
        }

        print("\n--- PRUEBA CRUD ---")

        # 1. Crear equipo
        respuesta = await cliente.post(
            f"{URL}/equipos",
            json=equipo
        )

        print("1. Crear equipo:", respuesta.status_code)
        assert respuesta.status_code == 201, respuesta.text

        equipo_id = respuesta.json()["equipo"]["id"]

        # 2. Consultar equipo
        respuesta = await cliente.get(
            f"{URL}/equipos/{equipo_id}"
        )

        print("2. Consultar equipo:", respuesta.status_code)
        assert respuesta.status_code == 200, respuesta.text

        # 3. Actualizar equipo
        equipo_actualizado = {
            **equipo,
            "ubicacion": "Área de mantenimiento"
        }

        respuesta = await cliente.put(
            f"{URL}/equipos/{equipo_id}",
            json=equipo_actualizado
        )

        print("3. Actualizar equipo:", respuesta.status_code)
        assert respuesta.status_code == 200, respuesta.text

        # 4. Verificar actualización
        respuesta = await cliente.get(
            f"{URL}/equipos/{equipo_id}"
        )

        assert respuesta.status_code == 200, respuesta.text
        assert respuesta.json()["ubicacion"] == "Área de mantenimiento"

        print("4. Verificar actualización: correcto")

        # 5. Eliminar equipo de prueba
        respuesta = await cliente.delete(
            f"{URL}/equipos/{equipo_id}"
        )

        print("5. Eliminar equipo:", respuesta.status_code)
        assert respuesta.status_code == 200, respuesta.text

        # 6. Confirmar eliminación
        respuesta = await cliente.get(
            f"{URL}/equipos/{equipo_id}"
        )

        print("6. Confirmar eliminación:", respuesta.status_code)
        assert respuesta.status_code == 404, respuesta.text

        print("\n¡Todas las pruebas CRUD finalizaron correctamente!")


if __name__ == "__main__":
    asyncio.run(probar_crud())