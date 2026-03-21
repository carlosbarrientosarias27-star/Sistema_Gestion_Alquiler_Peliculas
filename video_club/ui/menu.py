import os 
from datetime import date
from typing import Callable

from services.alquiler_service import AlquilerService
from services.pelicula_service import PeliculaService
from services.cliente_service import ClienteService
from services.multa_service import MultaService

class Menu:
    def __init__(self):
        self._multa_service = MultaService()
        self._pelicula_service = PeliculaService()
        self._cliente_service = ClienteService()
        self._alquiler_service = AlquilerService(multa_service=self._multa_service)

    # MEJORA 3: Validación centralizada de entrada de datos
    def _leer_int(self, mensaje: str) -> int:
        while True:
            try:
                return int(input(f"{mensaje}: "))
            except ValueError:
                print("❌ Por favor, introduce un número entero válido.")

    def ejecutar(self) -> None:
        # ... (lógica del diccionario de opciones igual) ...
        pass

    def _realizar_alquiler(self) -> None:
        try:
            # MEJORA 3: Uso del lector validado
            id_cli = self._leer_int("ID Cliente")
            cod_peli = input("Código Película: ").strip()
            dias = self._leer_int("Días")
            
            alq = self._alquiler_service.alquilar_pelicula(id_cli, cod_peli, dias)
            print(f"\n✅ Alquiler OK: {alq}")
        except ValueError as e:
            print(f"\n❌ Error: {e}")

    def _realizar_devolucion(self) -> None:
        try:
            id_alq = self._leer_int("ID Alquiler")
            # MEJORA 5: El menú ya no envía date.today()
            self._alquiler_service.registrar_devolucion_hoy(id_alq)
            print("\n✅ Devolución procesada.")
        except ValueError as e:
            print(f"\n❌ Error: {e}")

    def _ver_historial_cliente(self) -> None:
        id_cli = self._leer_int("ID Cliente")
        hist = self._alquiler_service.obtener_historial_cliente(id_cli)
        for h in hist: print(h)