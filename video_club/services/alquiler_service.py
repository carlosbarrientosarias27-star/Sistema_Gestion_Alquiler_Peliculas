from datetime import date, timedelta
from typing import List
from video_club.models.alquiler import Alquiler
from video_club.database.connection import get_connection
from video_club.services.pelicula_service import PeliculaService
from video_club.services.multa_service import MultaService


class AlquilerService:
    """Servicio de gestión de alquileres."""

    def __init__(self, multa_service: MultaService = None):   # ← inyección
        self._pelicula_service = PeliculaService()
        self._multa_service = multa_service or MultaService() # ← sin import circular

    def alquilar_pelicula(self, id_cliente: int, codigo: str, dias: int) -> Alquiler:
        """Crea un alquiler.

        Input:
            id_cliente: int
            codigo: str
            dias: int
        Output:
            Alquiler

        Casos límite:
            - Sin copias disponibles → ValueError
            - Película no encontrada → ValueError
        """
        pelicula = self._pelicula_service.buscar_por_codigo(codigo)
        if pelicula is None:
            raise ValueError(f"Película con código '{codigo}' no encontrada.")
        if pelicula.copias_disponibles <= 0:
            raise ValueError(f"No hay copias disponibles de '{pelicula.titulo}'.")

        hoy = date.today()
        fecha_devolucion = hoy + timedelta(days=dias)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE pelicula SET copias_disponibles = copias_disponibles - 1 WHERE codigo = ?",
            (codigo,)
        )
        cursor.execute(
            "INSERT INTO alquiler (id_cliente, codigo_pelicula, fecha_alquiler, "
            "fecha_devolucion_prevista, fecha_devolucion_real) VALUES (?,?,?,?,?)",
            (id_cliente, codigo, hoy.isoformat(), fecha_devolucion.isoformat(), None)
        )
        id_alquiler = cursor.lastrowid
        conn.commit()
        conn.close()

        return Alquiler(
            id_alquiler=id_alquiler,
            id_cliente=id_cliente,
            codigo_pelicula=codigo,
            fecha_alquiler=hoy,
            fecha_devolucion_prevista=fecha_devolucion,
            fecha_devolucion_real=None,
        )

    def devolver_pelicula(self, id_alquiler: int, fecha_real: date) -> None:
        """Registra devolución y genera multa si hay retraso.

        Input:
            id_alquiler: int
            fecha_real: date
        Output:
            None

        Casos límite:
            - Alquiler inexistente → ValueError
            - Alquiler ya devuelto → ValueError
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT codigo_pelicula, fecha_devolucion_prevista, fecha_devolucion_real "
            "FROM alquiler WHERE id_alquiler = ?",
            (id_alquiler,)
        )
        fila = cursor.fetchone()

        if fila is None:
            conn.close()
            raise ValueError(f"Alquiler {id_alquiler} no encontrado.")
        if fila[2] is not None:
            conn.close()
            raise ValueError(f"Alquiler {id_alquiler} ya fue devuelto.")

        codigo_pelicula = fila[0]
        fecha_prevista = date.fromisoformat(fila[1])

        cursor.execute(
            "UPDATE alquiler SET fecha_devolucion_real = ? WHERE id_alquiler = ?",
            (fecha_real.isoformat(), id_alquiler)
        )
        cursor.execute(
            "UPDATE pelicula SET copias_disponibles = copias_disponibles + 1 WHERE codigo = ?",
            (codigo_pelicula,)
        )
        conn.commit()
        conn.close()

        dias_retraso = (fecha_real - fecha_prevista).days
        if dias_retraso > 0:
            self._multa_service.calcular_multa(id_alquiler, dias_retraso)

    def listar_alquileres_activos(self) -> List[Alquiler]:
        """Lista alquileres activos (sin fecha de devolución real).

        Output:
            list[Alquiler]
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_alquiler, id_cliente, codigo_pelicula, "
            "fecha_alquiler, fecha_devolucion_prevista "
            "FROM alquiler WHERE fecha_devolucion_real IS NULL"
        )
        filas = cursor.fetchall()
        conn.close()

        return [
            Alquiler(
                id_alquiler=f[0],
                id_cliente=f[1],
                codigo_pelicula=f[2],
                fecha_alquiler=date.fromisoformat(f[3]),
                fecha_devolucion_prevista=date.fromisoformat(f[4]),
                fecha_devolucion_real=None,
            )
            for f in filas
        ]