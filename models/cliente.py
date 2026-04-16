from dataclasses import dataclass

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    email: str

    def __repr__(self) -> str:
        return f"Cliente #{self.id_cliente} - {self.nombre} ({self.email})"