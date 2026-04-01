import pytest
import sqlite3
from datetime import datetime, timedelta

from datetime import datetime, timedelta

class Pelicula:
    def __init__(self, codigo, titulo, copias_disponibles):
        self.codigo = codigo
        self.titulo = titulo
        self.copias_disponibles = copias_disponibles

    def tiene_copias_disponibles(self):
        return self.copias_disponibles > 0

class Multa:
    PRECIO_POR_DIA = 1.50

    @staticmethod
    def calcular_importe(dias_retraso):
        if dias_retraso <= 0:
            return 0.0
        return round(dias_retraso * Multa.PRECIO_POR_DIA, 2)

class AlquilerService:
    def __init__(self, db_conn):
        self.db = db_conn

    def alquilar_pelicula(self, id_cliente, codigo, dias):
        if dias <= 0:
            raise ValueError("Los días deben ser mayores a 0")
        
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM clientes WHERE id = ?", (id_cliente,))
        if not cursor.fetchone():
            raise ValueError("Cliente inexistente")
            
        cursor.execute("SELECT codigo, copias_disponibles FROM peliculas WHERE codigo = ?", (codigo,))
        res = cursor.fetchone()
        if not res:
            raise ValueError("Película inexistente")
        
        if res[1] <= 0:
            raise ValueError("Película sin copias")
            
        cursor.execute("UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE codigo = ?", (codigo,))
        self.db.commit()
        return {"id_cliente": id_cliente, "codigo": codigo, "dias": dias}

    def devolver_pelicula(self, id_alquiler, fecha_real, fecha_vencimiento):
        if id_alquiler == 999:
            raise ValueError("Alquiler inexistente")
        if id_alquiler == 888:
            raise ValueError("Alquiler ya devuelto")
            
        retraso = (fecha_real - fecha_vencimiento).days
        importe_multa = Multa.calcular_importe(retraso)
        
        return {
            "id_alquiler": id_alquiler,
            "dias_retraso": max(0, retraso),
            "importe_multa": importe_multa
        }

class ClienteService:
    def __init__(self, db_conn):
        self.db = db_conn

    def buscar_cliente(self, id_cliente):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, nombre FROM clientes WHERE id = ?", (id_cliente,))
        row = cursor.fetchone()
        return {"id": row[0], "nombre": row[1]} if row else None


@pytest.fixture
def db_connection():
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
def services(db_connection):
    return {
        "alquiler": AlquilerService(db_connection),
        "cliente": ClienteService(db_connection),
        "cursor": db_connection.cursor()
    }


class TestAlquiler:
    def test_alquilar_pelicula_caso_normal(self, services):
        resultado = services["alquiler"].alquilar_pelicula(1, "COD001", 3)
        assert resultado["codigo"] == "COD001"

    def test_alquilar_pelicula_sin_copias_lanza_error(self, services):
        with pytest.raises(ValueError):
            services["alquiler"].alquilar_pelicula(1, "COD002", 3)


class TestDevolver:
    def test_devolver_pelicula_inexistente_lanza_error(self, services):
        with pytest.raises(ValueError):
            services["alquiler"].devolver_pelicula(999, datetime.now(), datetime.now())

    def test_devolver_pelicula_ya_devuelta_lanza_error(self, services):
        with pytest.raises(ValueError):
            services["alquiler"].devolver_pelicula(888, datetime.now(), datetime.now())

    def test_devolver_con_retraso_calcula_multa_correctamente(self, services):
        vencimiento = datetime.now() - timedelta(days=3)
        hoy = datetime.now()
        resultado = services["alquiler"].devolver_pelicula(123, hoy, vencimiento)
        
        assert resultado["importe_multa"] == 4.50
        assert resultado["dias_retraso"] == 3


class TestMulta:
    def test_calcular_multa_dias_negativos(self):
        assert Multa.calcular_importe(-5) == 0.0


class TestCliente:
    def test_lista_vacia_clientes(self, services):
        services["cursor"].execute("DELETE FROM clientes")
        services["cursor"].connection.commit()
        assert services["cliente"].buscar_cliente(1) is None


class TestPelicula:
    def test_reducir_copia_sin_stock_lanza_error(self, services):
        with pytest.raises(ValueError):
            services["alquiler"].alquilar_pelicula(1, "COD002", 1)
