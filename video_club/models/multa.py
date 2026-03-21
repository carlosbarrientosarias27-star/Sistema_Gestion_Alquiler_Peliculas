from dataclasses import dataclass

@dataclass
class Multa:
    id_multa: int
    id_alquiler: int
    dias_retraso: int
    importe: float

    TARIFA_POR_DIA: float = 1.50  # euros por día de retraso

    @staticmethod
    def calcular_importe(dias_retraso: int) -> float:
        """
        Calcula el coste basado en días de retraso con 2 decimales.
        
        Input: dias_retraso (int)
        Output: float (Importe total redondeado)
        """
        if dias_retraso <= 0:
            return 0.0
        
        importe = dias_retraso * Multa.TARIFA_POR_DIA
        return round(importe, 2)

    def __repr__(self) -> str:
        """Formato: Multa #1 | Alquiler #2 | 3 días | 4.50€"""
        return f"Multa #{self.id_multa} | Alquiler #{self.id_alquiler} | {self.dias_retraso} días | {self.importe:.2f}€"
    
    @classmethod
    def from_row(cls, row: sqlite3.Row):
         return cls(**dict(row))