from typing import Optional
from models.cliente import Cliente
from database.connection import get_connection

class ClienteService:
    def registrar_cliente(self, nombre: str, email: str) -> int:
        if not nombre or not email:
            raise ValueError("Nombre y email son obligatorios.")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (?, ?)", (nombre, email))
        id_generado = cursor.lastrowid
        conn.commit()
        conn.close()
        if id_generado is None:
            raise RuntimeError("No se pudo registrar el cliente")
        return id_generado

    def buscar_cliente(self, id_cliente: int) -> Optional[Cliente]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, email FROM clientes WHERE id_cliente = ?", (id_cliente,))
        f = cursor.fetchone()
        conn.close()
        return Cliente(f[0], f[1], f[2]) if f else None

    def listar_clientes(self) -> list[Cliente]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, email FROM clientes")
        filas = cursor.fetchall()
        conn.close()
        return [Cliente(f[0], f[1], f[2]) for f in filas]