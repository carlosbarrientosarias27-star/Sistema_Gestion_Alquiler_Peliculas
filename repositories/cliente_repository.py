from database.connection import obtener_conexion
from models.cliente import Cliente

class ClienteRepository:
    def guardar(self, cliente: Cliente):
        """Registra un nuevo cliente."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, email) VALUES (?, ?)",
                (cliente.nombre, cliente.email)
            )
            conn.commit()
            return cursor.lastrowid

    def obtener_todos(self):
        """Lista todos los clientes registrados."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()

    def buscar_por_id(self, id_cliente: int):
        """Busca un cliente por su ID numérico."""
        with obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            return cursor.fetchone()

    def existe(self, id_cliente: int) -> bool:
        """Verifica si existe un cliente."""
        return self.buscar_por_id(id_cliente) is not None