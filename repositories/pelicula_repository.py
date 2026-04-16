from database.connection import obtener_conexion
from models.pelicula import Pelicula

class PeliculaRepository:
    def guardar(self, pelicula: Pelicula):
        """Guarda una nueva película en la base de datos."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            # Asegúrate de usar id_pelicula
            cursor.execute(
                "INSERT INTO peliculas (id_pelicula, titulo, director, copias_disponibles) VALUES (?, ?, ?, ?)",
                (pelicula.codigo, pelicula.titulo, pelicula.director, pelicula.copias_disponibles)
            )
            conn.commit()

    def obtener_por_codigo(self, codigo: str):
        """Busca una película por su código único."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            # CORRECCIÓN: 'id_pelicula' en lugar de 'id'
            cursor.execute("SELECT * FROM peliculas WHERE id_pelicula = ?", (codigo,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_pelicula": row["id_pelicula"], # CORRECCIÓN: nombre de columna
                    "titulo": row["titulo"],
                    "director": row["director"],
                    "copias_disponibles": row["copias_disponibles"]
                }
            return None

    def reducir_stock(self, codigo: str):
        """Reduce en 1 las copias disponibles."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            # CORRECCIÓN: 'id_pelicula' en lugar de 'id'
            cursor.execute(
                "UPDATE peliculas SET copias_disponibles = copias_disponibles - 1 WHERE id_pelicula = ?",
                (codigo,)
            )
            conn.commit()

    def aumentar_stock(self, codigo: str):
        """Aumenta en 1 las copias disponibles."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            # CORRECCIÓN: 'id_pelicula' y variable 'codigo'
            cursor.execute(
                "UPDATE peliculas SET copias_disponibles = copias_disponibles + 1 WHERE id_pelicula = ?",
                (codigo,)
            )
            conn.commit()

    def obtener_todos(self):
        """Devuelve una lista de todas las películas."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM peliculas")
            rows = cursor.fetchall()
            # Aquí ya usabas id_pelicula correctamente
            return [Pelicula(row["id_pelicula"], row["titulo"], row["director"], row["copias_disponibles"]) for row in rows]