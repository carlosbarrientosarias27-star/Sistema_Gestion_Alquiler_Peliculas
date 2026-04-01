from video_club.models.cliente import Cliente

def test_creacion_cliente():
    cliente = Cliente(1, "Juan", "juan@email.com")

    assert cliente.id_cliente == 1
    assert cliente.nombre == "Juan"
    assert cliente.email == "juan@email.com"


def test_repr_cliente():
    cliente = Cliente(1, "Juan", "juan@email.com")

    resultado = repr(cliente)

    assert resultado == "Cliente #1 - Juan (juan@email.com)"