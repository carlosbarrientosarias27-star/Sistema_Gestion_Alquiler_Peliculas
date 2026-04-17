import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta
from services.alquiler_service import AlquilerService
from models.alquiler import Alquiler

# --- 1. Fixtures para dependencias ---

@pytest.fixture
def mocks():
    """Crea mocks para todas las dependencias del servicio."""
    return {
        "multa_svc": MagicMock(),
        "peli_repo": MagicMock(),
        "clie_repo": MagicMock(),
        "alqu_repo": MagicMock()
    }

@pytest.fixture
def alquiler_service(mocks):
    """Instancia el servicio inyectando los mocks creados."""
    return AlquilerService(
        multa_service=mocks["multa_svc"],
        pelicula_repo=mocks["peli_repo"],
        cliente_repo=mocks["clie_repo"],
        alquiler_repo=mocks["alqu_repo"]
    )

# --- 2. Tests para alquilar_pelicula ---

def test_alquilar_pelicula_exitoso(alquiler_service, mocks):
    """Verifica que un alquiler se registre correctamente si hay stock y el cliente existe."""
    # Configuración de los mocks
    mocks["peli_repo"].obtener_por_codigo.return_value = {"id_pelicula": "COD1", "copias_disponibles": 5}
    mocks["clie_repo"].existe.return_value = True
    mocks["alqu_repo"].crear.return_value = 1  # ID del nuevo alquiler

    # Ejecución
    resultado = alquiler_service.alquilar_peliculas(id_cliente=10, id_pelicula="COD1", dias=3)

    # Verificaciones
    assert isinstance(resultado, Alquiler)
    assert resultado.id_alquiler == 1
    mocks["peli_repo"].reducir_stock.assert_called_once_with("COD1")

def test_alquilar_pelicula_sin_stock_lanza_error(alquiler_service, mocks):
    """Debe lanzar ValueError si la película tiene 0 copias."""
    mocks["peli_repo"].obtener_por_codigo.return_value = {"codigo": "COD2", "copias_disponibles": 0}
    
    with pytest.raises(ValueError, match="No hay copias disponibles"):
        alquiler_service.alquilar_peliculas(1, "COD2", 3)

# --- 3. Tests para devolver_pelicula ---

def test_devolver_con_retraso_genera_multa(alquiler_service, mocks):
    """Verifica el cálculo de multa cuando la fecha real es posterior a la prevista."""
    # Configurar alquiler vencido hace 2 días
    fecha_prevista = date.today() - timedelta(days=2)
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 5,
        "id_pelicula": "COD1",
        "fecha_devolucion_prevista": fecha_prevista.isoformat(),
        "fecha_devolucion_real": None
    }

    # Ejecución (devolución hoy)
    resultado = alquiler_service.devolver_peliculas(id_alquiler=5, fecha_real=date.today())

    # Verificaciones
    assert resultado["dias_retraso"] == 2
    assert resultado["importe_multa"] == 3.0  # 2 días * 1.50 tarifa
    mocks["multa_svc"].calcular_y_guardar_multa.assert_called_with(5, 2)
    mocks["peli_repo"].aumentar_stock.assert_called_with("COD1")

def test_devolver_pelicula_ya_devuelta_lanza_error(alquiler_service, mocks):
    """Debe fallar si el alquiler ya tiene una fecha_devolucion_real."""
    mocks["alqu_repo"].obtener_por_id.return_value = {
        "id_alquiler": 5,
        "fecha_devolucion_real": "2023-10-01"
    }

    with pytest.raises(ValueError, match="Alquiler ya devuelto"):
        alquiler_service.devolver_peliculas(5)

# --- 4. Tests de Listado e Historial ---

def test_obtener_historial_cliente(alquiler_service, mocks):
    """Verifica que el mapeo de filas de BD a objetos Alquiler funcione."""
    # Simular fila de base de datos
    mocks["alqu_repo"].obtener_por_cliente.return_value = [{
        "id_alquiler": 1,
        "id_cliente": 10,
        "id_pelicula": "COD1",
        "fecha_alquiler": "2023-10-01",
        "fecha_devolucion_prevista": "2023-10-04",
        "fecha_devolucion_real": None
    }]

    historial = alquiler_service.obtener_historial_clientes(10)

    assert len(historial) == 1
    assert isinstance(historial[0], Alquiler)
    assert historial[0].codigo_pelicula == "COD1"
