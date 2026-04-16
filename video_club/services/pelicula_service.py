from typing import Optional
from video_club.models.pelicula import Pelicula
from video_club.database.connection import get_connection

class PeliculaService:
    def registrar_pelicula(self, id: int, titulo: str, director: str, copias: int) -> None:
        if copias < 0:
            raise ValueError("Las copias no pueden ser negativas.")
        if self.buscar_por_codigo(id):
            raise ValueError(f"Ya existe una película con el código {id}.")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO peliculas (id, titulo, director, copias_disponibles) VALUES (?,?,?,?)",
            (id, titulo, director, copias)
        )
        conn.commit()
        conn.close()

    def buscar_por_codigo(self, id: int) -> Optional[Pelicula]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, director, copias_disponibles FROM peliculas WHERE codigo = ?", (id,))
        f = cursor.fetchone()
        conn.close()
        return Pelicula(f[0], f[1], f[2], f[3]) if f else None

    def listar_peliculas(self) -> list[Pelicula]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, director, copias_disponibles FROM peliculas")
        filas = cursor.fetchall()
        conn.close()
        return [Pelicula(f[0], f[1], f[2], f[3]) for f in filas]