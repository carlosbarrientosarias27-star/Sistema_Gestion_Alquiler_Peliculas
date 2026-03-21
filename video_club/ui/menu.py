import os
from datetime import date
from typing import Callable

# Importaciones limpias (sin duplicados)
from repositories.pelicula_repository import PeliculaRepository
from repositories.cliente_repository import ClienteRepository
from repositories.alquiler_repository import AlquilerRepository

from services.alquiler_service import AlquilerService
from services.pelicula_service import PeliculaService
from services.cliente_service import ClienteService
from services.multa_service import MultaService

class Menu:
    def __init__(self):
        # 1. Instanciamos los Repositorios primero
        self._pelicula_repo = PeliculaRepository()
        self._cliente_repo = ClienteRepository()
        self._alquiler_repo = AlquilerRepository()

        # 2. Instanciamos los Servicios simples
        self._multa_service = MultaService()
        self._pelicula_service = PeliculaService()
        self._cliente_service = ClienteService()

        # 3. Instanciamos AlquilerService pasando TODO lo que pide
        # El error indica que le faltan estos 3 argumentos:
        self._alquiler_service = AlquilerService(
            pelicula_repo=self._pelicula_repo,
            cliente_repo=self._cliente_repo,
            alquiler_repo=self._alquiler_repo,
            multa_service=self._multa_service
        )

    def _leer_int(self, prompt: str) -> int:
        """Helper para asegurar que la entrada sea un entero válido."""
        while True:
            try:
                entrada = input(prompt).strip()
                return int(entrada)
            except ValueError:
                print("\033[91m⚠️ Error: Por favor, introduce un número entero válido.\033[0m")
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
            copias = self._leer_int("Número de copias: ")
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
            id_cli = self._leer_int("ID Cliente: ")
            cod_peli = input("Código Película: ").strip()
            dias = self._leer_int("Días: ")
            alq = self._alquiler_service.alquilar_pelicula(id_cli, cod_peli, dias)
            print(f"\n✅ Alquiler OK: {alq}")
        except ValueError as e:
            print(f"\n❌ Error: {e}")


    def _realizar_devolucion(self) -> None:
        try:
            id_alq = self._leer_int("ID Alquiler: ")
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
            id_cli = self._leer_int("ID Cliente: ")
            hist = self._alquiler_service.obtener_historial_cliente(id_cli)
            for h in hist: print(h)
        except ValueError as e:
            print(f"\n❌ Error: {e}")
