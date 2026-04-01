from database.connection import get_connection
from video_club.models.alquiler import Alquiler

class AlquilerRepository:
    def crear(self, id_cliente: int, codigo_pelicula: str, fecha_alquiler, fecha_prevista):
        """Crea un registro de alquiler."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO alquileres (id_cliente, codigo_pelicula, fecha_alquiler, fecha_devolucion_prevista) VALUES (?, ?, ?, ?)",
                (id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista)
            )
            conn.commit()
            return cursor.lastrowid

    def obtener_por_id(self, id_alquiler: int):
        """Obtiene un alquiler por su ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE id_alquiler = ?", (id_alquiler,))
            return cursor.fetchone()

    def find_active_by_cliente(self, id_cliente: int):
        """Obtiene alquileres que aún no han sido devueltos."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM alquileres WHERE id_cliente = ? AND fecha_devolucion_real IS NULL",
                (id_cliente,)
            )
            return cursor.fetchall()

    def actualizar_devolucion(self, id_alquiler: int, fecha_real):
        """Marca un alquiler como devuelto."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE alquileres SET fecha_devolucion_real = ? WHERE id_alquiler = ?",
                (fecha_real, id_alquiler)
            )
            conn.commit()

    def obtener_todos(self):
        """Obtiene todos los alquileres."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres")
            return cursor.fetchall()

    def obtener_por_cliente(self, id_cliente: int):
        """Obtiene todos los alquileres de un cliente."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE id_cliente = ?", (id_cliente,))
            return cursor.fetchall()