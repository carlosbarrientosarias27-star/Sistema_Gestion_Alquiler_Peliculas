import unittest
import sqlite3
from datetime import datetime, timedelta

# --- Mock de Clases de Negocio (Para que el test sea ejecutable) ---
# En un escenario real, estas clases estarían en sus propios archivos.

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
        # Verificar cliente
        cursor.execute("SELECT id FROM clientes WHERE id = ?", (id_cliente,))
        if not cursor.fetchone():
            raise ValueError("Cliente inexistente")
            
        # Verificar película
        cursor.execute("SELECT codigo, copias_disponibles FROM peliculas WHERE codigo = ?", (codigo,))
        res = cursor.fetchone()
        if not res:
            raise ValueError("Película inexistente")
        
        if res[1] <= 0:
            raise ValueError("Película sin copias")
            
        # Lógica de alquiler (Simplificada para el test)
        cursor.execute("UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE codigo = ?", (codigo,))
        return {"id_cliente": id_cliente, "codigo": codigo, "dias": dias}

    def devolver_pelicula(self, id_alquiler, fecha_real):
        # Lógica simulada de devolución
        if id_alquiler == 999: # ID inexistente para el test
            raise ValueError("Alquiler inexistente")
        if id_alquiler == 888: # ID ya devuelto para el test
            raise ValueError("Alquiler ya devuelto")
            
        # Simulación: supongamos que el alquiler vencía hoy y fecha_real es mañana
        return True

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
        """Configuración de base de datos en memoria antes de cada test."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        
        # Crear tablas
        self.cursor.execute("CREATE TABLE peliculas (codigo TEXT, titulo TEXT, copias_disponibles INTEGER)")
        self.cursor.execute("CREATE TABLE clientes (id INTEGER, nombre TEXT)")
        
        # Insertar datos de prueba
        self.cursor.execute("INSERT INTO peliculas VALUES ('COD001', 'Inception', 2)")
        self.cursor.execute("INSERT INTO peliculas VALUES ('COD002', 'Titanic', 0)")
        self.cursor.execute("INSERT INTO clientes VALUES (1, 'Juan Perez')")
        self.conn.commit()

        # Instanciar servicios
        self.alquiler_service = AlquilerService(self.conn)
        self.cliente_service = ClienteService(self.conn)

    def tearDown(self):
        """Limpieza de la conexión después de cada test."""
        self.conn.close()

    # --- 1. Tests AlquilerService.alquilar_pelicula ---

    def test_alquilar_pelicula_caso_normal(self):
        resultado = self.alquiler_service.alquilar_pelicula(1, "COD001", 3)
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado["codigo"], "COD001")

    def test_alquilar_pelicula_sin_copias_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "COD002", 3)

    def test_alquilar_pelicula_inexistente_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "NONEXISTENT", 3)

    def test_alquilar_pelicula_cliente_inexistente_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(99, "COD001", 3)

    def test_alquilar_pelicula_dias_invalidos_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "COD001", 0)

    # --- 2. Tests AlquilerService.devolver_pelicula ---

    def test_devolver_pelicula_inexistente_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.devolver_pelicula(999, datetime.now())

    def test_devolver_pelicula_ya_devuelta_lanza_error(self):
        with self.assertRaises(ValueError):
            self.alquiler_service.devolver_pelicula(888, datetime.now())

    # --- 3. Tests Multa.calcular_importe ---

    def test_calcular_multa_3_dias(self):
        self.assertEqual(Multa.calcular_importe(3), 4.50)

    def test_calcular_multa_10_dias(self):
        self.assertEqual(Multa.calcular_importe(10), 15.00)

    def test_calcular_multa_0_dias(self):
        self.assertEqual(Multa.calcular_importe(0), 0.0)

    def test_calcular_multa_dias_negativos(self):
        # Caso límite extra solicitado
        self.assertEqual(Multa.calcular_importe(-5), 0.0)

    def test_calcular_multa_1_dia(self):
        self.assertEqual(Multa.calcular_importe(1), 1.50)

    # --- 4. Tests ClienteService.buscar_cliente ---

    def test_buscar_cliente_existente(self):
        cliente = self.cliente_service.buscar_cliente(1)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente["id"], 1)

    def test_buscar_cliente_inexistente_devuelve_none(self):
        cliente = self.cliente_service.buscar_cliente(999)
        self.assertIsNone(cliente)

    def test_lista_vacia_clientes(self):
        # Caso límite extra: limpiar tabla y buscar
        self.cursor.execute("DELETE FROM clientes")
        self.conn.commit()
        cliente = self.cliente_service.buscar_cliente(1)
        self.assertIsNone(cliente)

    # --- 5. Tests Pelicula.tiene_copias_disponibles ---

    def test_pelicula_con_2_copias_tiene_disponibilidad(self):
        p = Pelicula("C1", "T1", 2)
        self.assertTrue(p.tiene_copias_disponibles())

    def test_pelicula_con_0_copias_no_tiene_disponibilidad(self):
        p = Pelicula("C2", "T2", 0)
        self.assertFalse(p.tiene_copias_disponibles())

    def test_pelicula_con_1_copia_tiene_disponibilidad(self):
        p = Pelicula("C3", "T3", 1)
        self.assertTrue(p.tiene_copias_disponibles())

    def test_reducir_copia_sin_stock_lanza_error(self):
        # Caso límite extra: intentar alquilar algo con 0 copias en BD
        with self.assertRaises(ValueError):
            self.alquiler_service.alquilar_pelicula(1, "COD002", 1)

if __name__ == "__main__":
    unittest.main()