import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta
from video_club.services.alquiler_service import AlquilerService
from video_club.models.alquiler import Alquiler


@pytest.fixture
def mocks():
    return {
        "multa_svc": MagicMock(),
        "peli_repo": MagicMock(),
        "clie_repo": MagicMock(),
        "alqu_repo": MagicMock()
    }


@pytest.fixture
def alquiler_service(mocks):
    return AlquilerService(
        mocks["multa_svc"],
        mocks["peli_repo"],
        mocks["clie_repo"],
        mocks["alqu_repo"]
    )


def test_alquilar_pelicula_caso_normal(alquiler_service, mocks):
    mocks["peli_repo"].obtener_por_codigo.return_value = {
        "codigo": "COD001",
        "copias_disponibles": 2
    }
    mocks["clie_repo"].existe.return_value = True
    mocks["alqu_repo"].crear.return_value = 100

    resultado = alquiler_service.alquilar_pelicula(1, "COD001", 3)

    assert isinstance(resultado, Alquiler)
    assert resultado.codigo_pelicula == "COD001"
    assert resultado.id_alquiler == 100
    mocks["peli_repo"].reducir_stock.assert_called_once_with("COD001")


def test_alquilar_pelicula_sin_copias_lanza_error(alquiler_service, mocks):
    mocks["peli_repo"].obtener_por_codigo.return_value = {
        "codigo": "COD002",
        "copias_disponibles": 0
    }

    with pytest.raises(ValueError, match="No hay copias disponibles"):
        alquiler_service.alquilar_pelicula(1, "COD002", 3)


def test_alquilar_pelicula_pelicula_no_encontrada(alquiler_service, mocks):
    mocks["peli_repo"].obtener_por_codigo.return_value = None

    with pytest.raises(ValueError, match="Película no encontrada"):
        alquiler_service.alquilar_pelicula(1, "COD999", 3)


def test_alquilar_pelicula_cliente_no_encontrado(alquiler_service, mocks):
    mocks["peli_repo"].obtener_por_codigo.return_value = {
        "codigo": "COD001",
        "copias_disponibles": 2
    }
    mocks["clie_repo"].existe.return_value = False

    with pytest.raises(ValueError, match="Cliente no encontrado"):
        alquiler_service.alquilar_pelicula(999, "COD001", 3)


def test_alquilar_pelicula_dias_invalidos(alquiler_service, mocks):
    with pytest.raises(ValueError, match="Los días deben ser positivos"):
        alquiler_service.alquilar_pelicula(1, "COD001", 0)

    with pytest.raises(ValueError, match="Los días deben ser positivos"):
        alquiler_service.alquilar_pelicula(1, "COD001", -1)


def test_devolver_con_retraso_calcula_multa_correctamente(alquiler_service, mocks):
    fecha_vencimiento = date.today() - timedelta(days=3)
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 123,
        "codigo_pelicula": "COD001",
        "fecha_devolucion_prevista": fecha_vencimiento.isoformat(),
        "fecha_devolucion_real": None
    }

    resultado = alquiler_service.devolver_pelicula(123, date.today())

    assert resultado["dias_retraso"] == 3
    assert resultado["importe_multa"] > 0
    mocks["multa_svc"].calcular_y_guardar_multa.assert_called_once_with(123, 3)
    mocks["alqu_repo"].actualizar_devolucion.assert_called_once()
    mocks["peli_repo"].aumentar_stock.assert_called_once_with("COD001")


def test_devolver_a_tiempo_sin_multa(alquiler_service, mocks):
    fecha_vencimiento = date.today() + timedelta(days=2)
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 124,
        "codigo_pelicula": "COD001",
        "fecha_devolucion_prevista": fecha_vencimiento.isoformat(),
        "fecha_devolucion_real": None
    }

    resultado = alquiler_service.devolver_pelicula(124, date.today())

    assert resultado["dias_retraso"] == 0
    assert resultado["importe_multa"] == 0.0
    mocks["multa_svc"].calcular_y_guardar_multa.assert_not_called()


def test_devolver_pelicula_ya_devuelta_lanza_error(alquiler_service, mocks):
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 888,
        "codigo_pelicula": "COD001",
        "fecha_devolucion_prevista": "2023-01-01",
        "fecha_devolucion_real": "2023-01-01"
    }

    with pytest.raises(ValueError, match="Alquiler ya devuelto"):
        alquiler_service.devolver_pelicula(888)


def test_devolver_pelicula_no_encontrada_lanza_error(alquiler_service, mocks):
    mocks["alqu_repo"].obtener_por_id.return_value = None

    with pytest.raises(ValueError, match="Alquiler no encontrado"):
        alquiler_service.devolver_pelicula(999)
