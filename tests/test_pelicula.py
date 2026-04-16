import pytest
from models.pelicula import Pelicula

# --- Fixtures ---

@pytest.fixture
def pelicula_valida():
    """Retorna una instancia de Pelicula con stock inicial."""
    return Pelicula(
        id_peliculas="COD001",
        titulo="Inception",
        director="Christopher Nolan",
        copias_disponibles=2
    )

@pytest.fixture
def pelicula_sin_stock():
    """Retorna una instancia de Pelicula con 0 copias."""
    return Pelicula("COD002", "Titanic", "James Cameron", 0)

# --- Tests de Funcionalidad ---

def test_creacion_pelicula(pelicula_valida):
    """Verifica que los atributos se asignen correctamente al crear la instancia."""
    assert pelicula_valida.id_peliculas == "COD001"
    assert pelicula_valida.titulo == "Inception"
    assert pelicula_valida.copias_disponibles == 2

def test_tiene_copias_disponibles_true(pelicula_valida):
    """Debe retornar True si hay copias."""
    assert pelicula_valida.tiene_copias_disponibles() is True

def test_tiene_copias_disponibles_false(pelicula_sin_stock):
    """Debe retornar False si el stock es 0."""
    assert pelicula_sin_stock.tiene_copias_disponibles() is False

def test_reducir_copia_disminuye_stock(pelicula_valida):
    """Verifica que el stock baje en una unidad."""
    pelicula_valida.reducir_copia()
    assert pelicula_valida.copias_disponibles == 1

def test_reducir_copia_sin_stock_lanza_error(pelicula_sin_stock):
    """Debe lanzar ValueError si se intenta reducir stock a cero copias."""
    with pytest.raises(ValueError, match="No hay copias disponibles"):
        pelicula_sin_stock.reducir_copia()

def test_aumentar_copia_incrementa_stock(pelicula_valida):
    """Verifica que el stock suba en una unidad."""
    pelicula_valida.aumentar_copia()
    assert pelicula_valida.copias_disponibles == 3

def test_representacion_string(pelicula_valida):
    """Verifica que el método __repr__ tenga el formato esperado."""
    esperado = "[COD001] Inception - Christopher Nolan (2 copias)"
    assert repr(pelicula_valida) == esperado