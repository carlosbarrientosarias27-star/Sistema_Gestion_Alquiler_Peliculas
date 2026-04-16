import pytest
from models.cliente import Cliente

# --- Fixtures ---

@pytest.fixture
def cliente_ejemplo():
    """Retorna una instancia de Cliente para las pruebas."""
    return Cliente(
        id_cliente=1,
        nombre="Juan Pérez",
        email="juan.perez@example.com"
    )

# --- Tests de Funcionalidad ---

def test_creacion_cliente(cliente_ejemplo):
    """Verifica que los atributos se asignen correctamente al instanciar la clase."""
    assert cliente_ejemplo.id_cliente == 1
    assert cliente_ejemplo.nombre == "Juan Pérez"
    assert cliente_ejemplo.email == "juan.perez@example.com"

def test_representacion_string(cliente_ejemplo):
    """Verifica que el método __repr__ devuelva el formato esperado."""
    # El formato definido es: Cliente #ID - Nombre (Email)
    esperado = "Cliente #1 - Juan Pérez (juan.perez@example.com)"
    assert repr(cliente_ejemplo) == esperado

def test_cliente_distintos_valores():
    """Verifica la creación de un cliente con valores diferentes."""
    cliente = Cliente(99, "Ana López", "ana@mail.com")
    assert cliente.id_cliente == 99
    assert cliente.nombre == "Ana López"
    assert "Ana López" in repr(cliente)