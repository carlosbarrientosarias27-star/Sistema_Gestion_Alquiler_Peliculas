import sqlite3

DB_NAME = "video_club.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Configurado una sola vez
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tablas() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla Películas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peliculas (
        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT, 
        titulo TEXT NOT NULL,
        director TEXT NOT NULL,
        copias_disponibles INTEGER DEFAULT 0
    )
    """)

    # Tabla Clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla Alquileres (CORREGIDA)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alquileres (
        id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        id_pelicula INTEGER NOT NULL,
        fecha_alquiler TEXT NOT NULL,
        fecha_devolucion_prevista TEXT NOT NULL,
        fecha_devolucion_real TEXT DEFAULT NULL,
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY(id_pelicula) REFERENCES peliculas(id_pelicula) 
    )
    """)

    # Tabla Multas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS multas (
        id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
        id_alquiler INTEGER,
        dias_retraso INTEGER,
        importe REAL,
        FOREIGN KEY(id_alquiler) REFERENCES alquileres(id_alquiler)
    )
    """)

    conn.commit()
    conn.close()

def inicializar_db() -> None:
    """
    Inicializa el esquema de la base de datos.
    
    Output:
        None
    """
    crear_tablas()
    print(f"Base de datos '{DB_NAME}' inicializada correctamente con claves foráneas activas.")