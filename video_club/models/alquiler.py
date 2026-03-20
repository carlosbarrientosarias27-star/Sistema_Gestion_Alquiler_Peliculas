from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Alquiler:
    """Representa un alquiler de una película."""
    id_alquiler: int
    id_cliente: int
    id_pelicula: int
    fecha_alquiler: date
    fecha_devolucion_prevista: date
    fecha_devolucion_real: Optional[date]

    def marcar_devolucion(self, fecha_real: date) -> None:
        """
        Marca la devolución del alquiler.
        Input: fecha_real (date)
        Output: None
        Caso límite: alquiler ya devuelto → ValueError
        """
        raise NotImplementedError