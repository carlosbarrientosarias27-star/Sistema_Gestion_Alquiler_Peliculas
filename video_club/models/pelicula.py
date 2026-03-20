from dataclasses import dataclass

@dataclass
class Pelicula:
    """Representa una película disponible para alquiler."""
    titulo: str
    director: str
    codigo: str
    copias_disponibles: int

    def __post_init__(self) -> None:
        """Valida los datos iniciales de la película."""
        raise NotImplementedError