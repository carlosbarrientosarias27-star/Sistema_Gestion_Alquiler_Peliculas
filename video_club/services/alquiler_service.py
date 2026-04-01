import sqlite3
from datetime import date, timedelta
from typing import Optional, List


from video_club.database.connection import get_connection
from video_club.models.alquiler import Alquiler
from video_club.models.multa import Multa
from video_club.services.multa_service import MultaService


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

        peli = self._pelicula_repo.obtener_por_codigo(codigo_pelicula)
        if not peli:
            raise ValueError("Película no encontrada")
        if peli["copias_disponibles"] <= 0:
            raise ValueError("No hay copias disponibles")

        if not self._cliente_repo.existe(id_cliente):
            raise ValueError("Cliente no encontrado")

        fecha_alquiler = date.today()
        fecha_prevista = fecha_alquiler + timedelta(days=dias)

        try:
            id_generado = self._alquiler_repo.crear(
                id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista
            )

            self._pelicula_repo.reducir_stock(codigo_pelicula)
            
            return Alquiler(id_generado, id_cliente, codigo_pelicula, fecha_alquiler, fecha_prevista, None)
       
        except sqlite3.Error as e:
            raise RuntimeError(f"Error crítico en la base de datos: {e}")


    def devolver_pelicula(self, id_alquiler: int, fecha_real: Optional[date] = None) -> dict:
        """
        Procesa la devolución de una película, calcula multa si hay retraso.
        
        Input:
            id_alquiler: ID del alquiler a devolver.
            fecha_real: Fecha de devolución (por defecto hoy).
        Output:
            dict con datos de la devolución y multa si aplica.
        """
        if fecha_real is None:
            fecha_real = date.today()

        alquiler = self._alquiler_repo.obtener_por_id(id_alquiler)
        if not alquiler:
            raise ValueError("Alquiler no encontrado")
        
        if alquiler["fecha_devolucion_real"]:
            raise ValueError("Alquiler ya devuelto")

        fecha_vencimiento = date.fromisoformat(alquiler["fecha_devolucion_prevista"])
        
        dias_retraso = (fecha_real - fecha_vencimiento).days
        
        resultado = {
            "id_alquiler": id_alquiler,
            "dias_retraso": max(0, dias_retraso),
            "importe_multa": 0.0
        }

        if dias_retraso > 0:
            resultado["importe_multa"] = Multa.calcular_importe(dias_retraso)
            self._multa_service.calcular_y_guardar_multa(id_alquiler, dias_retraso)

        self._alquiler_repo.actualizar_devolucion(id_alquiler, fecha_real.isoformat())
        self._pelicula_repo.aumentar_stock(alquiler["codigo_pelicula"])
        
        return resultado

    def listar_alquileres_activos(self) -> List[Alquiler]:
        """
        Lista todos los alquileres que aún no han sido devueltos.
       
        Output:
            list[Alquiler]: Lista de objetos Alquiler activos.
        """
        with get_connection() as conn:
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
        filas = self._alquiler_repo.obtener_por_cliente(id_cliente)
        return [self._mapear_alquiler(f) for f in filas]


    def _mapear_alquiler(self, row) -> Alquiler:
        """Helper interno para convertir una fila de BD a objeto Alquiler."""
        return Alquiler(
            id_alquiler=row["id_alquiler"],
            id_cliente=row["id_cliente"],
            codigo_pelicula=row["codigo_pelicula"],
            fecha_alquiler=date.fromisoformat(row["fecha_alquiler"]),
            fecha_devolucion_prevista=date.fromisoformat(row["fecha_devolucion_prevista"]),
            fecha_devolucion_real=date.fromisoformat(row["fecha_devolucion_real"]) if row["fecha_devolucion_real"] else None
        )