import pytest
from unittest.mock import MagicMock, patch
from services.cliente_service import ClienteService
from models.cliente import Cliente

# --- 1. Fixtures ---

@pytest.fixture
def cliente_service():
    """Instancia el servicio para ser usado en los tests."""
    return ClienteService()

# --- 2. Tests para registrar_cliente ---

def test_registrar_cliente_exitoso(cliente_service):
    """Verifica que el registro devuelva el ID generado correctamente."""
    with patch('services.cliente_service.o') as mock_conn:
        # Configurar el mock de la conexión y cursor
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 10  # Simular ID generado
        
        id_gen = cliente_service.registrar_cliente("Ana Garcia", "ana@mail.com")
        
        assert id_gen == 10
        mock_cursor.execute.assert_called_once()
        mock_conn.return_value.commit.assert_called_once()

def test_registrar_cliente_vacio_lanza_error(cliente_service):
    """Debe lanzar ValueError si faltan datos obligatorios."""
    with pytest.raises(ValueError, match="Nombre y email son obligatorios."):
        cliente_service.registrar_cliente("", "mail@mail.com")

# --- 3. Tests para buscar_cliente ---

def test_buscar_cliente_existente(cliente_service):
    """Verifica que devuelva un objeto Cliente si se encuentra en la BD."""
    with patch('services.cliente_service.get_connection') as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        # Simular fila devuelta por la base de datos
        mock_cursor.fetchone.return_value = (1, "Juan Perez", "juan@mail.com")
        
        cliente = cliente_service.buscar_cliente(1)
        
        assert isinstance(cliente, Cliente)
        assert cliente.id_cliente == 1
        assert cliente.nombre == "Juan Perez"

def test_buscar_cliente_no_existente(cliente_service):
    """Debe devolver None si el ID no existe."""
    with patch('services.cliente_service.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.fetchone.return_value = None
        
        cliente = cliente_service.buscar_cliente(999)
        
        assert cliente is None

# --- 4. Tests para listar_clientes ---

def test_listar_clientes_vacio(cliente_service):
    """Verifica que devuelva una lista vacía si no hay registros."""
    with patch('services.cliente_service.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.fetchall.return_value = []
        
        lista = cliente_service.listar_clientes()
        
        assert lista == []
        assert len(lista) == 0

def test_listar_clientes_con_datos(cliente_service):
    """Verifica que convierta todas las filas de la BD en objetos Cliente."""
    with patch('services.cliente_service.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.fetchall.return_value = [
            (1, "A", "a@mail.com"),
            (2, "B", "b@mail.com")
        ]
        
        lista = cliente_service.listar_clientes()
        
        assert len(lista) == 2
        assert all(isinstance(c, Cliente) for c in lista)
        assert lista[0].nombre == "A"