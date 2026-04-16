from typing import Optional
from models.pelicula import Pelicula
from database.connection import obtener_conexion

class PeliculaService:
    def registrar_pelicula(self, id_pelicula: int, titulo: str, director: str, copias: int) -> None:
        if copias < 0:
            raise ValueError("Las copias no pueden ser negativas.")
        if self.buscar_por_codigo(id_pelicula):
            raise ValueError(f"Ya existe una película con el código {id_pelicula}.")
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO peliculas (id_pelicula, titulo, director, copias_disponibles) VALUES (?,?,?,?)",
            (id_pelicula, titulo, director, copias)
        )
        conn.commit()
        conn.close()

    def buscar_por_codigo(self, id: int) -> Optional[Pelicula]:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pelicula, titulo, director, copias_disponibles FROM peliculas WHERE id_pelicula = ?", (id,))
        f = cursor.fetchone()
        conn.close()
        return Pelicula(f[0], f[1], f[2], f[3]) if f else None

    def listar_peliculas(self) -> list[Pelicula]:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_pelicula, titulo, director, copias_disponibles FROM peliculas")
        filas = cursor.fetchall()
        conn.close()
        return [Pelicula(f[0], f[1], f[2], f[3]) for f in filas]