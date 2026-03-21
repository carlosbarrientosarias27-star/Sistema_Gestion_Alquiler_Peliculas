import sqlite3
from typing import Optional, List
from database.connection import get_connection
from models.multa import Multa

class MultaService:
    """Servicio para la gestión y persistencia de multas en la base de datos."""

    def calcular_y_guardar_multa(self, id_alquiler: int, dias_retraso: int) -> Optional[Multa]:
        """
        Calcula e inserta una multa si existe retraso.
        
        Input: id_alquiler (int), dias_retraso (int)
        Output: Objeto Multa creado o None si no hay retraso.
        """
        if dias_retraso <= 0:
            return None

        importe = Multa.calcular_importe(dias_retraso)

        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO multas (id_alquiler, dias_retraso, importe) VALUES (?, ?, ?)",
                    (id_alquiler, dias_retraso, importe)
                )
                id_generado = cursor.lastrowid
                conn.commit()
                return Multa(id_generado, id_alquiler, dias_retraso, importe)
            except sqlite3.Error as e:
                conn.rollback()
                print(f"Error al guardar la multa: {e}")
                return None

    def obtener_multas_por_alquiler(self, id_alquiler: int) -> List[Multa]:
        """Busca multas asociadas a un alquiler específico."""
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM multas WHERE id_alquiler = ?", (id_alquiler,))
            filas = cursor.fetchall()
            return [self._mapear_multa(f) for f in filas]

    def listar_todas_las_multas(self) -> List[Multa]:
        """Devuelve todas las multas registradas, de la más reciente a la más antigua."""
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM multas ORDER BY id_multa DESC")
            filas = cursor.fetchall()
            return [self._mapear_multa(f) for f in filas]

    def total_multas_cliente(self, id_cliente: int) -> float:
        """
        Calcula la suma total de importes de multas para un cliente específico.
        
        Input: id_cliente (int)
        Output: float (Suma total)
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            # Realizamos JOIN entre multas y alquileres para filtrar por cliente
            cursor.execute("""
                SELECT SUM(m.importe) 
                FROM multas m
                JOIN alquileres a ON m.id_alquiler = a.id_alquiler
                WHERE a.id_cliente = ?
            """, (id_cliente,))
            
            resultado = cursor.fetchone()
            total = resultado[0] if resultado and resultado[0] else 0.0
            return round(total, 2)

    def _mapear_multa(self, row: sqlite3.Row) -> Multa:
        """Helper para convertir filas de BD en objetos Multa."""
        return Multa(
            id_multa=row["id_multa"],
            id_alquiler=row["id_alquiler"],
            dias_retraso=row["dias_retraso"],
            importe=row["importe"]
        )