from database.connection import get_connection
from models.pelicula import Pelicula

class PeliculaRepository:
    def guardar(self, pelicula: Pelicula):
        """Guarda una nueva película en la base de datos."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO peliculas (id_pelicula, titulo, director, copias_disponibles) VALUES (?, ?, ?, ?)",
                (pelicula.codigo, pelicula.titulo, pelicula.director, pelicula.copias_disponibles)
            )
            conn.commit()

    def obtener_por_codigo(self, codigo: str):
        """Busca una película por su código único."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peliculas WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_pelicula": row["id"],
                    "titulo": row["titulo"],
                    "director": row["director"],
                    "copias_disponibles": row["copias_disponibles"]
                }
            return None

    def reducir_stock(self, codigo: str):
        """Reduce en 1 las copias disponibles."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE id = ?",
                (codigo,)
            )
            conn.commit()

    def aumentar_stock(self, codigo: str):
        """Aumenta en 1 las copias disponibles."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE peliculas SET copias_disponibles = copias_disponibles + 1 WHERE id = ?",
                (id,)
            )
            conn.commit()

    def obtener_todos(self):
        """Devuelve una lista de todas las películas."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peliculas")
            rows = cursor.fetchall()
            return [Pelicula(row["id_pelicula"], row["titulo"], row["director"], row["copias_disponibles"]) for row in rows]