from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Alquiler:
    id_alquiler: int
    id_cliente: int
    codigo_pelicula: str
    fecha_alquiler: date
    fecha_devolucion_prevista: date
    fecha_devolucion_real: Optional[date] = None

    def esta_activo(self) -> bool:
        """Determina si la película aún no ha sido devuelta."""
        return self.fecha_devolucion_real is None

    def dias_retraso(self) -> int:
        """
        Calcula los días transcurridos entre la devolución real y la prevista.
        Si no se ha devuelto, se asume 0 o se puede comparar con date.today() 
        según la lógica de negocio (aquí usamos la real según el requerimiento).
        """
        if not self.fecha_devolucion_real or self.fecha_devolucion_real <= self.fecha_devolucion_prevista:
            return 0
        
        delta = self.fecha_devolucion_real - self.fecha_devolucion_prevista
        return max(0, delta.days)

    def __repr__(self) -> str:
        return f"Alquiler #{self.id_alquiler} | Cliente {self.id_cliente} | Pelicula {self.codigo_pelicula}"