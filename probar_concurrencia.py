import asyncio
import time
import httpx

URL = "http://127.0.0.1:8000"


async def probar_calculo(cliente):
    inicio = time.perf_counter()

    respuesta = await cliente.get(
        f"{URL}/procesamiento/cpu",
        params={"numero": 10000000}
    )

    duracion = time.perf_counter() - inicio

    print(
        f"Cálculo: estado {respuesta.status_code}, "
        f"tiempo {duracion:.2f} segundos"
    )


async def consultar_equipos(cliente):
    inicio = time.perf_counter()

    respuesta = await cliente.get(f"{URL}/equipos")

    duracion = time.perf_counter() - inicio

    print(
        f"Consulta de equipos: estado {respuesta.status_code}, "
        f"tiempo {duracion:.2f} segundos"
    )


async def main():
    async with httpx.AsyncClient(timeout=120) as cliente:

        print("Iniciando prueba de concurrencia...\n")

        await asyncio.gather(
            probar_calculo(cliente),
            consultar_equipos(cliente)
        )

        print("\nPrueba finalizada.")


if __name__ == "__main__":
    asyncio.run(main())
    