from .connection import get_connection  # Change this line

def init_db() -> None:
    """Crea las tablas necesarias si no existen.

    Output:
        None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pelicula (
        codigo TEXT PRIMARY KEY,
        titulo TEXT,
        director TEXT,
        copias_disponibles INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alquiler (
        id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        codigo_pelicula TEXT,          -- ← corregido: era id_pelicula INTEGER
        fecha_alquiler TEXT,
        fecha_devolucion_prevista TEXT,
        fecha_devolucion_real TEXT,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
        FOREIGN KEY (codigo_pelicula) REFERENCES pelicula(codigo)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS multa (
        id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alquiler INTEGER,
        dias_retraso INTEGER,
        importe REAL,
        FOREIGN KEY (id_alquiler) REFERENCES alquiler(id_alquiler)
    )
    """)

    conn.commit()
    conn.close()