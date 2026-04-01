import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta
from video_club.services.alquiler_service import AlquilerService
from video_club.models.alquiler import Alquiler

# --- 1. Fixtures con Mocks ---

@pytest.fixture
def mocks():
    """Crea y agrupa todos los mocks necesarios."""
    return {
        "multa_svc": MagicMock(),
        "peli_repo": MagicMock(),
        "clie_repo": MagicMock(),
        "alqu_repo": MagicMock()
    }

@pytest.fixture
def alquiler_service(mocks):
    """Inyecta los mocks en el servicio."""
    return AlquilerService(
        mocks["multa_svc"], 
        mocks["peli_repo"], 
        mocks["clie_repo"], 
        mocks["alqu_repo"]
    )

# --- 2. Tests de Alquilar ---

def test_alquilar_pelicula_caso_normal(alquiler_service, mocks):
    # Configurar Mocks: Simular que la película y el cliente existen
    mocks["peli_repo"].obtener_por_codigo.return_value = {
        "codigo": "COD001", 
        "copias_disponibles": 2
    }
    mocks["clie_repo"].existe.return_value = True
    mocks["alqu_repo"].crear.return_value = 100

    # Ejecutar
    resultado = alquiler_service.alquilar_pelicula(1, "COD001", 3)

    # Validar: El servicio ahora devuelve un objeto Alquiler, no un dict
    assert resultado.codigo_pelicula == "COD001"
    assert resultado.id_alquiler == 100
    mocks["peli_repo"].reducir_stock.assert_called_once_with("COD001")

def test_alquilar_pelicula_sin_copias_lanza_error(alquiler_service, mocks):
    # Simular que no hay copias disponibles
    mocks["peli_repo"].obtener_por_codigo.return_value = {
        "codigo": "COD002", 
        "copias_disponibles": 0
    }
    
    with pytest.raises(ValueError, match="No hay copias disponibles"):
        alquiler_service.alquilar_pelicula(1, "COD002", 3)

# --- 3. Tests de Devolución ---

def test_devolver_con_retraso_calcula_multa_correctamente(alquiler_service, mocks):
    # Configurar: Un alquiler que venció hace 3 días
    fecha_vencimiento = date.today() - timedelta(days=3)
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 123,
        "codigo_pelicula": "COD001",
        "fecha_devolucion_prevista": fecha_vencimiento.isoformat(),
        "fecha_devolucion_real": None
    }

    # Ejecutar devolución hoy
    resultado = alquiler_service.devolver_pelicula(123, date.today())

    # Validar
    assert resultado["dias_retraso"] == 3
    assert resultado["importe_multa"] > 0  # Basado en la lógica de Multa.calcular_importe
    mocks["multa_service"].calcular_y_guardar_multa.assert_called()

def test_devolver_pelicula_ya_devuelta_lanza_error(alquiler_service, mocks):
    # Simular un alquiler que ya tiene fecha de devolución real
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 888,
        "fecha_devolucion_real": "2023-01-01"
    }

    with pytest.raises(ValueError, match="Alquiler ya devuelto"):
        alquiler_service.devolver_pelicula(888)
