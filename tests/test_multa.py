from video_club.models.multa import Multa

# --- Caso ya hecho ---
def test_calcular_importe_dias_negativos():
    assert Multa.calcular_importe(-5) == 0.0


# --- NUEVOS (paso a paso) ---

def test_calcular_importe_cero_dias():
    assert Multa.calcular_importe(0) == 0.0


def test_calcular_importe_dias_positivos():
    resultado = Multa.calcular_importe(3)
    assert resultado == 4.50


def test_calcular_importe_un_dia():
    assert Multa.calcular_importe(1) == 1.50