from database.connection import get_connection
from models.cliente import Cliente

class ClienteRepository:
    def save(self, cliente: Cliente):
        """Registra un nuevo cliente."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                (cliente.nombre, cliente.email)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all(self):
        """Lista todos los clientes registrados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()

    def find_by_id(self, id_cliente: int):
        """Busca un cliente por su ID numérico."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            return cursor.fetchone()

    def existe(self, id_cliente: int) -> bool:
        """Verifica si existe un cliente."""
        return self.find_by_id(id_cliente) is not None