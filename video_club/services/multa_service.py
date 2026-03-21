import sqlite3
from typing import Optional, List
from database.connection import get_connection
from models.multa import Multa

class MultaService:
    # MEJORA 4: Constante para evitar magic numbers
    PRECIO_POR_DIA = 2.50

    def calcular_y_guardar_multa(self, id_alquiler: int, dias_retraso: int) -> Optional[Multa]:
        if dias_retraso <= 0:
            return None

        # MEJORA 4: Uso de la constante
        importe = dias_retraso * self.PRECIO_POR_DIA

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

    def listar_todas_las_multas(self) -> List[Multa]:
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM multas ORDER BY id_multa DESC")
            # MEJORA 6: Uso de factory method
            return [Multa.from_row(f) for f in cursor.fetchall()]

    # ... (resto de métodos iguales usando factory method para mapear)