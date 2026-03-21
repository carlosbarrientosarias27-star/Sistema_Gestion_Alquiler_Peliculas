import os 
import sys
from datetime import date
from typing import Callable, Any

# Importaciones ajustadas a la estructura que usa tu main.py
from services.alquiler_service import AlquilerService
from services.pelicula_service import PeliculaService
from services.cliente_service import ClienteService
from services.multa_service import MultaService

class Menu:
    def __init__(self):
        # Instanciación de servicios como atributos de clase
        self._multa_service = MultaService()
        self._pelicula_service = PeliculaService()
        self._cliente_service = ClienteService()
        self._alquiler_service = AlquilerService(multa_service=self._multa_service)

    def ejecutar(self) -> None:
        """Método principal llamado por main.py"""
        opciones: dict[str, Callable[[], None]] = {
            "1": self._añadir_pelicula,
            "2": self._listar_peliculas,
            "3": self._registrar_cliente,
            "4": self._listar_clientes,
            "5": self._realizar_alquiler,
            "6": self._realizar_devolucion,
            "7": self._ver_alquileres_activos,
            "8": self._ver_multas,
            "9": self._ver_historial_cliente,
        }

        while True:
            print("\n" + "=" * 10 + " 🎬 VIDEOCLUB " + "=" * 10)
            print("1. Añadir película")
            print("2. Listar películas")
            print("3. Registrar cliente")
            print("4. Listar clientes")
            print("5. Alquilar película")
            print("6. Devolver película")
            print("7. Ver alquileres activos")
            print("8. Ver multas")
            print("9. Ver historial de cliente")
            print("0. Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "0":
                print("\n¡Hasta pronto!")
                break
            
            if opcion in opciones:
                try:
                    opciones[opcion]()
                except ValueError as e:
                    print(f"\033[91m\n❌ Error: {e}\033[0m")
                except Exception as e:
                    print(f"\n[!] Error inesperado: {e}")
            else:
                print("\n⚠️ Opción no válida.")

    # --- Métodos Privados (Convertidos de funciones a métodos de clase) ---

    def _añadir_pelicula(self) -> None:
        codigo = input("Código: ").strip()
        titulo = input("Título: ").strip()
        director = input("Director: ").strip()
        try:
            copias = int(input("Número de copias: "))
            self._pelicula_service.registrar_pelicula(codigo, titulo, director, copias)
            print("\n✅ Película añadida correctamente.")
        except ValueError:
            print("\n❌ Error: Las copias deben ser un número.")

    def _listar_peliculas(self) -> None:
        peliculas = self._pelicula_service.listar_peliculas()
        if not peliculas: print("\nNo hay películas.")
        else:
            for p in peliculas: print(p)

    def _registrar_cliente(self) -> None:
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        self._cliente_service.registrar_cliente(nombre, email)
        print("\n✅ Cliente registrado.")

    def _listar_clientes(self) -> None:
        clientes = self._cliente_service.listar_clientes()
        for c in clientes: print(c)

    def _realizar_alquiler(self) -> None:
        try:
            id_cli = int(input("ID Cliente: "))
            cod_peli = input("Código Película: ").strip()
            dias = int(input("Días: "))
            alq = self._alquiler_service.alquilar_pelicula(id_cli, cod_peli, dias)
            print(f"\n✅ Alquiler OK: {alq}")
        except ValueError as e:
            print(f"\n❌ Error: {e}")

    def _realizar_devolucion(self) -> None:
        try:
            id_alq = int(input("ID Alquiler: "))
            self._alquiler_service.devolver_pelicula(id_alq, date.today())
            print("\n✅ Devolución procesada.")
        except ValueError as e:
            print(f"\n❌ Error: {e}")

    def _ver_alquileres_activos(self) -> None:
        activos = self._alquiler_service.listar_alquileres_activos()
        for a in activos: print(a)

    def _ver_multas(self) -> None:
        multas = self._multa_service.listar_todas_las_multas()
        for m in multas: print(m)

    def _ver_historial_cliente(self) -> None:
        try:
            id_cli = int(input("ID Cliente: "))
            hist = self._alquiler_service.obtener_historial_cliente(id_cli)
            for h in hist: print(h)
        except ValueError as e:
            print(f"\n❌ Error: {e}")