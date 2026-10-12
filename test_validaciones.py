from pydantic import ValidationError
from main import Equipo


def test_equipo_valido():
    equipo = Equipo(
        nombre="Monitor de signos vitales",
        marca="Philips",
        modelo="MX450",
        numero_serie="TEST-001",
        ubicacion="Hospital",
        estado="Disponible"
    )

    assert equipo.nombre == "Monitor de signos vitales"
    assert equipo.estado == "Disponible"


def test_nombre_vacio():
    try:
        Equipo(
            nombre="   ",
            marca="Philips",
            modelo="MX450",
            numero_serie="TEST-002",
            ubicacion="Hospital",
            estado="Disponible"
        )
        assert False, "Se esperaba un error de validación"

    except ValidationError:
        pass


def test_estado_invalido():
    try:
        Equipo(
            nombre="Monitor de signos vitales",
            marca="Philips",
            modelo="MX450",
            numero_serie="TEST-003",
            ubicacion="Hospital",
            estado="Excelente"
        )
        assert False, "Se esperaba un error de validación"

    except ValidationError:
        pass


def test_campo_extra():
    try:
        Equipo(
            nombre="Monitor de signos vitales",
            marca="Philips",
            modelo="MX450",
            numero_serie="TEST-004",
            ubicacion="Hospital",
            estado="Disponible",
            color="Azul"
        )
        assert False, "Se esperaba un error por un campo adicional"

    except ValidationError:
        pass