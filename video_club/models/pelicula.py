from dataclasses import dataclass

@dataclass
class Pelicula:
    id: int
    titulo: str
    director: str
    copias_disponibles: int

    def tiene_copias_disponibles(self) -> bool:
        """Verifica si hay stock."""
        return self.copias_disponibles > 0

    def reducir_copia(self) -> None:
        """Resta una unidad al inventario."""
        if not self.tiene_copias_disponibles():
            raise ValueError(f"No hay copias disponibles para la película: {self.titulo}")
        self.copias_disponibles -= 1

    def aumentar_copia(self) -> None:
        """Suma una unidad al inventario."""
        self.copias_disponibles += 1

    def __repr__(self) -> str:
        return f"[{self.codigo}] {self.titulo} - {self.director} ({self.copias_disponibles} copias)"