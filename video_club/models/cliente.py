from dataclasses import dataclass

@dataclass
class Cliente:
    """Representa un cliente del videoclub."""
    id_cliente: int
    nombre: str
    email: str

    def __post_init__(self) -> None:
        """Valida los datos del cliente."""
        raise NotImplementedError
