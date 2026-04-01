from models.pelicula import Pelicula
import pytest

# --- tiene_copias_disponibles ---

def test_tiene_copias_disponibles_true():
    peli = Pelicula("COD001", "Inception", "Nolan", 2)
    assert peli.tiene_copias_disponibles() is True

def test_tiene_copias_disponibles_false():
    peli = Pelicula("COD002", "Titanic", "Cameron", 0)
    assert peli.tiene_copias_disponibles() is False


# --- reducir_copia ---

def test_reducir_copia_ok():
    peli = Pelicula("COD001", "Inception", "Nolan", 2)
    peli.reducir_copia()
    assert peli.copias_disponibles == 1

def test_reducir_copia_sin_stock_lanza_error():
    peli = Pelicula("COD002", "Titanic", "Cameron", 0)

    with pytest.raises(ValueError):
        peli.reducir_copia()


# --- aumentar_copia ---

def test_aumentar_copia():
    peli = Pelicula("COD001", "Inception", "Nolan", 1)
    peli.aumentar_copia()
    assert peli.copias_disponibles == 2


# --- __repr__ ---

def test_repr_formato_correcto():
    peli = Pelicula("COD001", "Inception", "Nolan", 2)
    esperado = "[COD001] Inception - Nolan (2 copias)"
    assert repr(peli) == esperado