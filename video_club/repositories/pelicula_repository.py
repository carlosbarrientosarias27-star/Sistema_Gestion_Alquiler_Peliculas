from database.connection import get_connection
from models.pelicula import Pelicula

class PeliculaRepository:
    def save(self, pelicula: Pelicula):
        """Guarda una nueva película en la base de datos."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO peliculas (codigo, titulo, director, copias_disponibles) VALUES (?, ?, ?, ?)",
                (pelicula.codigo, pelicula.titulo, pelicula.director, pelicula.copias_disponibles)
            )
            conn.commit()

    def find_by_codigo(self, codigo: str):
        """Busca una película por su código único."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peliculas WHERE codigo = ?", (codigo,))
            row = cursor.fetchone()
            if row:
                return Pelicula(row[1], row[2], row[3], row[4])
            return None

    def get_all(self):
        """Devuelve una lista de todas las películas."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peliculas")
            return [Pelicula(row[1], row[2], row[3], row[4]) for row in cursor.fetchall()]