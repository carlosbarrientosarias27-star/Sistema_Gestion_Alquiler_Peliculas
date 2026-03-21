import sqlite3
from datetime import date, timedelta
from typing import Optional, List


from database.connection import get_connection
from models.alquiler import Alquiler
from .multa_service import MultaService


class AlquilerService:
    def __init__(self, multa_service: MultaService, pelicula_repo, cliente_repo, alquiler_repo):
        """
        Inicializa el servicio de alquileres con sus dependencias inyectadas.
        """
        self._multa_service = multa_service
        self._pelicula_repo = pelicula_repo
        self._cliente_repo = cliente_repo
        self._alquiler_repo = alquiler_repo

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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres...")


           # 1. Buscar película y comprobar stock vía Repository
        peli = self._pelicula_repo.obtener_por_codigo(codigo_pelicula)
        if not peli:
            raise ValueError("Película no encontrada")
        if peli["copias_disponibles"] <= 0:
            raise ValueError("No hay copias disponibles")

        # 2. Buscar cliente vía Repository
        if not self._cliente_repo.existe(id_cliente):
            raise ValueError("Cliente no encontrado")

        # 3. Calcular fechas
        fecha_alquiler = date.today()
        fecha_prevista = fecha_alquiler + timedelta(days=dias)

        try:
            # 4. Delegar persistencia al AlquilerRepository
            id_generado = self._alquiler_repo.crear(
                id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista
            )

            # 5. Actualizar stock vía PeliculaRepository
            self._pelicula_repo.reducir_stock(codigo_pelicula)
            
            return Alquiler(id_generado, id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista, None)
       
        except sqlite3.Error as e:
            raise RuntimeError(f"Error crítico en la base de datos: {e}")


    def devolver_pelicula(self, id_alquiler: int, fecha_real: date) -> None:
        """
        Registra la devolución delegando la persistencia a los repositorios.
        """
        # 1. Obtener datos del alquiler
        alq = self._alquiler_repo.obtener_por_id(id_alquiler)

        if not alq:
            raise ValueError("Alquiler no encontrado")
        if alq["fecha_devolucion_real"] is not None:
            raise ValueError("Este alquiler ya fue devuelto previamente")

        try:
            # 2. Actualizar fechas y stock mediante repositorios
            self._alquiler_repo.registrar_devolucion(id_alquiler, fecha_real)
            self._pelicula_repo.aumentar_stock(alq["id_pelicula"])

            # 3. Lógica de Negocio: Gestión de multas
            fecha_prevista = date.fromisoformat(alq["fecha_devolucion_prevista"])
            dias_retraso = (fecha_real - fecha_prevista).days

            if dias_retraso > 0:
                self._multa_service.crear_multa(id_alquiler, dias_retraso)
            
            # Nota: El 'print' se elimina para mantener el servicio "mudo" (UI agnóstico)
        except sqlite3.Error as e:
            raise RuntimeError(f"Error al procesar la devolución: {e}")


    def listar_alquileres_activos(self) -> List[Alquiler]:
        """
        Lista todos los alquileres que aún no han sido devueltos.
       
        Output:
            list[Alquiler]: Lista de objetos Alquiler activos.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres...")
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
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alquileres...")
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