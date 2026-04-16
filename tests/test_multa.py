import pytest
from models.multa import Multa

# --- Tests para el método estático calcular_importe ---

def test_calcular_importe_con_retraso():
    """Verifica que el importe se calcule correctamente multiplicando días por tarifa (1.50)."""
    dias = 3
    esperado = 4.50  # 3 * 1.50
    assert Multa.calcular_importe(dias) == esperado

def test_calcular_importe_sin_retraso():
    """Verifica que si los días son 0, el importe sea 0.0."""
    assert Multa.calcular_importe(0) == 0.0

def test_calcular_importe_dias_negativos():
    """Verifica que si los días son negativos, el importe sea 0.0."""
    assert Multa.calcular_importe(-5) == 0.0

def test_calcular_importe_redondeo():
    """Verifica que el importe se redondee a 2 decimales."""
    # Aunque 1.50 no suele dar muchos decimales, es bueno probar la lógica de round()
    assert Multa.calcular_importe(1) == 1.50

# --- Tests para la instancia y representación ---

@pytest.fixture
def multa_ejemplo():
    """Fixture que retorna una instancia de Multa para pruebas de atributos."""
    return Multa(
        id_multa=1,
        id_alquiler=100,
        dias_retraso=3,
        importe=4.50
    )

def test_creacion_multa(multa_ejemplo):
    """Verifica la correcta asignación de atributos en el constructor."""
    assert multa_ejemplo.id_multa == 1
    assert multa_ejemplo.id_alquiler == 100
    assert multa_ejemplo.dias_retraso == 3
    assert multa_ejemplo.importe == 4.50

def test_representacion_string(multa_ejemplo):
    """Verifica que el método __repr__ devuelva el formato string esperado."""
    # Formato esperado: Multa #1 | Alquiler #100 | 3 días | 4.50€
    esperado = "Multa #1 | Alquiler #100 | 3 días | 4.50€"
    assert repr(multa_ejemplo) == esperado

def test_tarifa_por_dia_por_defecto():
    """Verifica que la constante TARIFA_POR_DIA sea la correcta."""
    assert Multa.TARIFA_POR_DIA == 1.50