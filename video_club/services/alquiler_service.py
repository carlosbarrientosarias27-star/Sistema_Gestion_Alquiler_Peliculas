import sqlite3
from datetime import date, timedelta
from typing import List, Optional

# CAMBIO: Importar desde la ruta raíz que entiende tu main.py
from models.alquiler import Alquiler
from database.connection import get_connection  # Asegúrate de usar get_connection
from services.pelicula_service import PeliculaService
from services.multa_service import MultaService

class AlquilerService:
    def __init__(self, multa_service: Optional[MultaService] = None):
        """
        Inicializa el servicio de alquileres.
        
        Input:
            multa_service: Opcional, instancia de MultaService.
        """
        self._multa_service = multa_service or MultaService()

    def alquilar_pelicula(self, id_cliente: int, codigo_pelicula: str, dias: int) -> Alquiler:
        """
        Registra un nuevo alquiler, validando existencia y stock.
        
        Input:
            id_cliente: ID del cliente que alquila.
            codigo_pelicula: Código único de la película.
            dias: Duración del préstamo.
        Output:
            Alquiler: El objeto de alquiler creado.
        """
        if dias <= 0:
            raise ValueError("Los días deben ser positivos")

        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Buscar película y comprobar copias
            cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", (codigo_pelicula,))
            fila_peli = cursor.fetchone()
            if not fila_peli:
                raise ValueError("Película no encontrada")
            if fila_peli["copias_disponibles"] <= 0:
                raise ValueError("No hay copias disponibles")

            # 2. Buscar cliente
            cursor.execute("SELECT id_cliente FROM clientes WHERE id_cliente = ?", (id_cliente,))
            if not cursor.fetchone():
                raise ValueError("Cliente no encontrado")

            # 3. Calcular fechas
            fecha_alquiler = date.today()
            fecha_prevista = fecha_alquiler + timedelta(days=dias)

            try:
                # 4. Insertar alquiler
                cursor.execute(
                    """INSERT INTO alquileres (id_cliente, id_pelicula, fecha_alquiler, fecha_devolucion_prevista)
                       VALUES (?, ?, ?, ?)""",
                    (id_cliente, codigo_pelicula, fecha_alquiler.isoformat(), fecha_prevista.isoformat())
                )
                id_generado = cursor.lastrowid

                # 5. Reducir stock
                cursor.execute(
                    "UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE codigo = ?",
                    (codigo_pelicula,)
                )
                
                conn.commit()
                return Alquiler(id_generado, id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista, None)
            
            except Exception as e:
                conn.rollback()
                raise e

    def devolver_pelicula(self, id_alquiler: int, fecha_real: date) -> None:
        """
        Registra la devolución y gestiona multas por retraso.
        
        Input:
            id_alquiler: ID del registro de alquiler.
            fecha_real: Fecha en la que se devuelve la película.
        """
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Buscar alquiler
            cursor.execute("SELECT * FROM alquileres WHERE id_alquiler = ?", (id_alquiler,))
            alq = cursor.fetchone()

            if not alq:
                raise ValueError("Alquiler no encontrado")
            if alq["fecha_devolucion_real"] is not None:
                raise ValueError("Ya fue devuelto")

            try:
                # 2. Actualizar fecha real
                cursor.execute(
                    "UPDATE alquileres SET fecha_devolucion_real = ? WHERE id_alquiler = ?",
                    (fecha_real.isoformat(), id_alquiler)
                )

                # 3. Aumentar stock de la película
                cursor.execute(
                    "UPDATE peliculas SET copias_disponibles = copias_disponibles + 1 WHERE codigo = ?",
                    (alq["id_pelicula"],)
                )

                # 4. Calcular retraso y multa
                fecha_prevista = date.fromisoformat(alq["fecha_devolucion_prevista"])
                dias_retraso = (fecha_real - fecha_prevista).days

                mensaje = f"Devolución exitosa del alquiler #{id_alquiler}."
                if dias_retraso > 0:
                    self._multa_service.crear_multa(id_alquiler, dias_retraso)
                    mensaje += f" ¡Atención! Generada multa por {dias_retraso} días de retraso."
                
                conn.commit()
                print(mensaje)

            except Exception as e:
                conn.rollback()
                raise e

    def listar_alquileres_activos(self) -> List[Alquiler]:
        """
        Lista todos los alquileres que aún no han sido devueltos.
        
        Output:
            list[Alquiler]: Lista de objetos Alquiler activos.
        """
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE fecha_devolucion_real IS NULL")
            filas = cursor.fetchall()
            
            return [self._mapear_alquiler(f) for f in filas]

    def obtener_historial_cliente(self, id_cliente: int) -> List[Alquiler]:
        """
        Obtiene todos los alquileres realizados por un cliente específico.
        
        Input:
            id_cliente: ID del cliente.
        Output:
            list[Alquiler]: Historial completo de alquileres.
        """
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres WHERE id_cliente = ?", (id_cliente,))
            filas = cursor.fetchall()
            
            return [self._mapear_alquiler(f) for f in filas]

    def _mapear_alquiler(self, row: sqlite3.Row) -> Alquiler:
        """Helper interno para convertir una fila de BD a objeto Alquiler."""
        return Alquiler(
            id_alquiler=row["id_alquiler"],
            id_cliente=row["id_cliente"],
            codigo_pelicula=row["id_pelicula"],
            fecha_alquiler=date.fromisoformat(row["fecha_alquiler"]),
            fecha_devolucion_prevista=date.fromisoformat(row["fecha_devolucion_prevista"]),
            fecha_devolucion_real=date.fromisoformat(row["fecha_devolucion_real"]) if row["fecha_devolucion_real"] else None
        )