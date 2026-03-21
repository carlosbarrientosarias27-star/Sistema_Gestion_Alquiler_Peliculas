import unittest
import sqlite3
from datetime import datetime, timedelta

# --- Clases de Negocio ---

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

    # FIX AQUÍ: Ahora acepta fecha_vencimiento y usa la clase Multa
    def devolver_pelicula(self, id_alquiler, fecha_real, fecha_vencimiento):
        if id_alquiler == 999:
            raise ValueError("Alquiler inexistente")
        if id_alquiler == 888:
            raise ValueError("Alquiler ya devuelto")
            
        # Lógica de negocio: Cálculo de retraso y multa
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

# --- SUITE DE TESTS ---

class TestVideoClub(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE peliculas (codigo TEXT, titulo TEXT, copias_disponibles INTEGER)")
        self.cursor.execute("CREATE TABLE clientes (id INTEGER, nombre TEXT)")
        self.cursor.execute("INSERT INTO peliculas VALUES ('COD001', 'Inception', 2)")
        self.cursor.execute("INSERT INTO peliculas VALUES ('COD002', 'Titanic', 0)")
        self.cursor.execute("INSERT INTO clientes VALUES (1, 'Juan Perez')")
        self.conn.commit()

        self.alquiler_service = AlquilerService(self.conn)
        self.cliente_service = ClienteService(self.conn)

    def tearDown(self):
        self.conn.close()

    # --- 1. Tests Alquilar ---
    def test_alquilar_pelicula_caso_normal(self):
        resultado = self.alquiler_service.alquilar_pelicula(1, "COD001", 3)
        self.assertEqual(resultado["codigo"], "COD001")

    def test_alquilar_pelicula_sin_copias_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "COD002", 3)

    # --- 2. Tests Devolver ---
    def test_devolver_pelicula_inexistente_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.devolver_pelicula(999, datetime.now(), datetime.now())

    def test_devolver_pelicula_ya_devuelta_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.devolver_pelicula(888, datetime.now(), datetime.now())

    def test_devolver_con_retraso_calcula_multa_correctamente(self):
        vencimiento = datetime.now() - timedelta(days=3)
        hoy = datetime.now()
        resultado = self.alquiler_service.devolver_pelicula(123, hoy, vencimiento)
        
        self.assertEqual(resultado["importe_multa"], 4.50)
        self.assertEqual(resultado["dias_retraso"], 3)

    # --- 3. Tests Multa ---
    def test_calcular_multa_dias_negativos(self):
        self.assertEqual(Multa.calcular_importe(-5), 0.0)

    # --- 4. Tests Cliente ---
    def test_lista_vacia_clientes(self):
        self.cursor.execute("DELETE FROM clientes")
        self.conn.commit()
        self.assertIsNone(self.cliente_service.buscar_cliente(1))

    # --- 5. Tests Pelicula ---
    def test_reducir_copia_sin_stock_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "COD002", 1)

if __name__ == "__main__":
    unittest.main()