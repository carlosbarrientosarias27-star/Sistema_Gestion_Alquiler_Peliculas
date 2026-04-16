from database.connection import get_connection

def init_db() -> None:
    """Crea las tablas necesarias si no existen.

    Output:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peliculas (
        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        director TEXT,
        copias_disponibles INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alquileres (
        id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_pelicula INT,
        fecha_alquiler TEXT,
        fecha_devolucion_prevista TEXT,
        fecha_devolucion_real TEXT,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_pelicula) REFERENCES peliculas(id_pelicula)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS multas (
        id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alquiler INTEGER,
        dias_retraso INTEGER,
        importe REAL,
        FOREIGN KEY (id_alquiler) REFERENCES alquileres(id_alquiler)
    )
    """)

    conn.commit()
    conn.close()