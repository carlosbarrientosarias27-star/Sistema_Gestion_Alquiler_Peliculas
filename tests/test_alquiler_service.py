import pytest
import sqlite3
from datetime import datetime, timedelta
from video_club.services.alquiler_service import AlquilerService


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE peliculas (codigo TEXT, titulo TEXT, copias_disponibles INTEGER)")
    cursor.execute("CREATE TABLE clientes (id INTEGER, nombre TEXT)")
    cursor.execute("INSERT INTO peliculas VALUES ('COD001', 'Inception', 2)")
    cursor.execute("INSERT INTO peliculas VALUES ('COD002', 'Titanic', 0)")
    cursor.execute("INSERT INTO clientes VALUES (1, 'Juan Perez')")
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def alquiler_service(db_conn):
    return AlquilerService(db_conn)


# --- 1. Tests Alquilar ---
def test_alquilar_pelicula_caso_normal(alquiler_service):
    resultado = alquiler_service.alquilar_pelicula(1, "COD001", 3)
    assert resultado["codigo"] == "COD001"

def test_alquilar_pelicula_sin_copias_lanza_error(alquiler_service):
    with pytest.raises(ValueError):
        alquiler_service.alquilar_pelicula(1, "COD002", 3)


# --- 2. Tests Devolver ---
def test_devolver_pelicula_inexistente_lanza_error(alquiler_service):
    with pytest.raises(ValueError):
        alquiler_service.devolver_pelicula(999, datetime.now(), datetime.now())

def test_devolver_pelicula_ya_devuelta_lanza_error(alquiler_service):
    with pytest.raises(ValueError):
        alquiler_service.devolver_pelicula(888, datetime.now(), datetime.now())

def test_devolver_con_retraso_calcula_multa_correctamente(alquiler_service):
    vencimiento = datetime.now() - timedelta(days=3)
    hoy = datetime.now()
    resultado = alquiler_service.devolver_pelicula(123, hoy, vencimiento)
    assert resultado["importe_multa"] == 4.50
    assert resultado["dias_retraso"] == 3
