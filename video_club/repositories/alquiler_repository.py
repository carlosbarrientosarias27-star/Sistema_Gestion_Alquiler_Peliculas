from database.connection import get_connection
from models.alquiler import Alquiler

class AlquilerRepository:
    def save(self, alquiler: Alquiler):
        """Crea un registro de alquiler."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO alquileres (cliente_id, pelicula_codigo, fecha_alquiler, fecha_devolucion_esperada) VALUES (?, ?, ?, ?)",
                (alquiler.cliente_id, alquiler.pelicula_codigo, alquiler.fecha_alquiler, alquiler.fecha_devolucion_esperada)
            )
            conn.commit()
            return cursor.lastrowid

    def find_active_by_cliente(self, id_cliente: int):
        """Obtiene alquileres que aún no han sido devueltos."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM alquileres WHERE cliente_id = ? AND fecha_devolucion_real IS NULL",
                (id_cliente,)
            )
            return cursor.fetchall()

    def update_devolucion(self, id_alquiler: int, fecha_real: str):
        """Marca un alquiler como devuelto."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alquileres SET fecha_devolucion_real = ? WHERE id = ?",
                (fecha_real, id_alquiler)
            )
            conn.commit()