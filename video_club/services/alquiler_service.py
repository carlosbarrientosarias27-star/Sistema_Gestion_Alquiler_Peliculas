import sqlite3
from datetime import date, timedelta
from typing import List, Optional

from models.alquiler import Alquiler
from database.connection import get_connection 
from services.multa_service import MultaService

class AlquilerService:
    def __init__(self, multa_service: Optional[MultaService] = None):
        self._multa_service = multa_service or MultaService()

    def alquilar_pelicula(self, id_cliente: int, codigo_pelicula: str, dias: int) -> Alquiler:
        if dias <= 0:
            raise ValueError("Los días deben ser positivos")

        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", (codigo_pelicula,))
            fila_peli = cursor.fetchone()
            if not fila_peli:
                raise ValueError("Película no encontrada")
            if fila_peli["copias_disponibles"] <= 0:
                raise ValueError("No hay copias disponibles")

            cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))
            if not cursor.fetchone():
                raise ValueError("Cliente no encontrado")

            fecha_alquiler = date.today()
            fecha_prevista = fecha_alquiler + timedelta(days=dias)

            try:
                cursor.execute(
                    """INSERT INTO alquileres (id_cliente, id_pelicula, fecha_alquiler, fecha_devolucion_prevista)
                       VALUES (?, ?, ?, ?)""",
                    (id_cliente, codigo_pelicula, fecha_alquiler.isoformat(), fecha_prevista.isoformat())
                )
                id_generado = cursor.lastrowid
                cursor.execute(
                    "UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE codigo = ?",
                    (codigo_pelicula,)
                )
                conn.commit()
                return Alquiler(id_generado, id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista, None)
            
            except sqlite3.Error as e: # MEJORA 2: Excepción específica
                conn.rollback()
                raise RuntimeError(f"Error en la base de datos al alquilar: {e}")

    # MEJORA 5: Nueva función para SRP (Lógica de "Hoy" en el servicio)
    def registrar_devolucion_hoy(self, id_alquiler: int) -> None:
        return self.devolver_pelicula(id_alquiler, date.today())

    def devolver_pelicula(self, id_alquiler: int, fecha_real: date) -> None:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM alquileres WHERE id_alquiler = ?", (id_alquiler,))
            alq = cursor.fetchone()

            if not alq:
                raise ValueError("Alquiler no encontrado")
            if alq["fecha_devolucion_real"] is not None:
                raise ValueError("Ya fue devuelto")

            try:
                cursor.execute(
                    "UPDATE alquileres SET fecha_devolucion_real = ? WHERE id_alquiler = ?",
                    (fecha_real.isoformat(), id_alquiler)
                )
                cursor.execute(
                    "UPDATE peliculas SET copias_disponibles = copias_disponibles + 1 WHERE codigo = ?",
                    (alq["id_pelicula"],)
                )

                fecha_prevista = date.fromisoformat(alq["fecha_devolucion_prevista"])
                dias_retraso = (fecha_real - fecha_prevista).days

                if dias_retraso > 0:
                    # MEJORA 1: Nombre de método correcto
                    self._multa_service.calcular_y_guardar_multa(id_alquiler, dias_retraso)
                
                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                raise RuntimeError(f"Error en la base de datos al devolver: {e}")

    def listar_alquileres_activos(self) -> List[Alquiler]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE fecha_devolucion_real IS NULL")
            # MEJORA 6: Uso de factory method en el modelo
            return [Alquiler.from_row(f) for f in cursor.fetchall()]

    def obtener_historial_cliente(self, id_cliente: int) -> List[Alquiler]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE id_cliente = ?", (id_cliente,))
            return [Alquiler.from_row(f) for f in cursor.fetchall()]