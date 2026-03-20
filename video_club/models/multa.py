from dataclasses import dataclass

@dataclass
class Multa:
    """Representa una multa por retraso en la devolución."""
    id_multa: int
    id_alquiler: int
    dias_retraso: int
    importe: float

    def calcular_importe(self) -> float:
        """
        Calcula el importe de la multa.
        Input: dias_retraso (int)
        Output: float
        Caso límite: dias_retraso <= 0 → 0.0
        """
        raise NotImplementedError