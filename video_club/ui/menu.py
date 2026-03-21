from datetime import date
from video_club.services.alquiler_service import AlquilerService
from video_club.services.pelicula_service import PeliculaService
from video_club.services.cliente_service import ClienteService
 
 
class Menu:
    """Interfaz de usuario por consola."""
 
    def __init__(self):
        self._alquiler_service = AlquilerService()
        self._pelicula_service = PeliculaService()
        self._cliente_service = ClienteService()
 
    def mostrar_menu(self) -> None:
        print("""
        1. Alquilar película
        2. Devolver película
        3. Buscar película
        4. Buscar cliente
        5. Listar alquileres activos
        0. Salir
        """)
 
    def ejecutar(self) -> None:
        """Loop principal del menú."""
        while True:
            self.mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()
 
            if opcion == "1":
                self._opcion_alquilar()
            elif opcion == "2":
                self._opcion_devolver()
            elif opcion == "3":
                self._opcion_buscar_pelicula()
            elif opcion == "4":
                self._opcion_buscar_cliente()
            elif opcion == "5":
                self._opcion_listar_activos()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
 
    # ------------------------------------------------------------------ #
    #  Opciones individuales                                               #
    # ------------------------------------------------------------------ #
 
    def _opcion_alquilar(self) -> None:
        try:
            id_cliente = int(input("ID de cliente: "))
            codigo = input("Código de película: ").strip()
            dias = int(input("Días de alquiler: "))
            alquiler = self._alquiler_service.alquilar_pelicula(id_cliente, codigo, dias)
            print(f"\n✔ Alquiler registrado (ID {alquiler.id_alquiler}). "
                  f"Devolver antes del {alquiler.fecha_devolucion_prevista}.\n")
        except ValueError as e:
            print(f"\n✘ Error: {e}\n")
 
    def _opcion_devolver(self) -> None:
        try:
            id_alquiler = int(input("ID de alquiler: "))

            # ← CORRECCIÓN: se pide la fecha al usuario en lugar de asumir hoy
            fecha_str = input("Fecha de devolución (AAAA-MM-DD) [Enter = hoy]: ").strip()
            if fecha_str == "":
                fecha_real = date.today()
            else:
                fecha_real = date.fromisoformat(fecha_str)  # ValueError si formato incorrecto

            self._alquiler_service.devolver_pelicula(id_alquiler, fecha_real)
            print(f"\n✔ Devolución registrada el {fecha_real}.\n")
        except ValueError as e:
            print(f"\n✘ Error: {e}\n")
 
    def _opcion_buscar_pelicula(self) -> None:
        codigo = input("Código de película: ").strip()
        pelicula = self._pelicula_service.buscar_por_codigo(codigo)
        if pelicula:
            print(f"\n  Título:    {pelicula.titulo}")
            print(f"  Director:  {pelicula.director}")
            print(f"  Copias:    {pelicula.copias_disponibles}\n")
        else:
            print("\n✘ Película no encontrada.\n")
 
    def _opcion_buscar_cliente(self) -> None:
        try:
            id_cliente = int(input("ID de cliente: "))
            cliente = self._cliente_service.buscar_cliente(id_cliente)
            if cliente:
                print(f"\n  Nombre: {cliente.nombre}")
                print(f"  Email:  {cliente.email}\n")
            else:
                print("\n✘ Cliente no encontrado.\n")
        except ValueError:
            print("\n✘ ID inválido.\n")
 
    def _opcion_listar_activos(self) -> None:
        activos = self._alquiler_service.listar_alquileres_activos()
        if not activos:
            print("\n  No hay alquileres activos.\n")
            return
        print(f"\n  {'ID':>4}  {'Cliente':>8}  {'Película':<12}  {'Prevista'}")
        print("  " + "-" * 44)
        for a in activos:
            print(f"  {a.id_alquiler:>4}  {a.id_cliente:>8}  "
                  f"{a.codigo_pelicula:<12}  {a.fecha_devolucion_prevista}")
        print()
 