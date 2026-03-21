import sys
from datetime import date
from video_club.services.alquiler_service import AlquilerService
from video_club.services.pelicula_service import PeliculaService
from video_club.services.cliente_service import ClienteService
from ..services.multa_service import MultaService

# Instanciación única de servicios
_pelicula_service = PeliculaService()
_cliente_service = ClienteService()
_multa_service = MultaService()
_alquiler_service = AlquilerService(multa_service=_multa_service)

def ejecutar_menu() -> None:
    """
    Punto de entrada principal de la interfaz de consola. 
    Gestiona el bucle principal y el despacho de opciones.
    """
    opciones: dict[str, Callable[[], None]] = {
        "1": _añadir_pelicula,
        "2": _listar_peliculas,
        "3": _registrar_cliente,
        "4": _listar_clientes,
        "5": _realizar_alquiler,
        "6": _realizar_devolucion,
        "7": _ver_alquileres_activos,
        "8": _ver_multas,
        "9": _ver_historial_cliente,
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
                # Imprimir error en rojo (secuencia ANSI)
                print(f"\033[91m\n❌ Error: {e}\033[0m")
            except Exception as e:
                print(f"\n[!] Error inesperado: {e}")
        else:
            print("\n⚠️ Opción no válida. Intente de nuevo.")

# --- Funciones de Gestión de Películas ---

def _añadir_pelicula() -> None:
    """Solicita datos y delega la creación de una película."""
    codigo = input("Código (ej: COD001): ").strip()
    titulo = input("Título: ").strip()
    director = input("Director: ").strip()
    
    try:
        copias = int(input("Número de copias: "))
        if copias <= 0:
            raise ValueError("El número de copias debe ser mayor a 0.")
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido para las copias.")

    _pelicula_service.registrar_pelicula(codigo, titulo, director, copias)
    print("\n✅ Película añadida correctamente.")

def _listar_peliculas() -> None:
    """Muestra todas las películas registradas."""
    peliculas = _pelicula_service.listar_peliculas()
    if not peliculas:
        print("\nNo hay películas registradas.")
    else:
        print("\n--- Catálogo de Películas ---")
        for p in peliculas:
            print(p)

# --- Funciones de Gestión de Clientes ---

def _registrar_cliente() -> None:
    """Solicita datos para registrar un nuevo cliente."""
    nombre = input("Nombre completo: ").strip()
    email = input("Email: ").strip()
    
    if not nombre or not email:
        raise ValueError("El nombre y el email son obligatorios.")

    _cliente_service.registrar_cliente(nombre, email)
    print("\n✅ Cliente registrado correctamente.")

def _listar_clientes() -> None:
    """Muestra todos los clientes registrados."""
    clientes = _cliente_service.listar_clientes()
    if not clientes:
        print("\nNo hay clientes registrados.")
    else:
        print("\n--- Lista de Clientes ---")
        for c in clientes:
            print(c)

# --- Funciones de Gestión de Alquileres ---

def _realizar_alquiler() -> None:
    """Procesa un nuevo alquiler validando inputs numéricos."""
    try:
        id_cliente = int(input("ID del cliente: "))
        codigo_peli = input("Código de la película: ").strip()
        dias = int(input("Número de días: "))
        
        if dias <= 0:
            raise ValueError("Los días deben ser un número positivo.")
            
        alquiler = _alquiler_service.alquilar_pelicula(id_cliente, codigo_peli, dias)
        print(f"\n✅ Alquiler registrado: {alquiler}")
    except ValueError as e:
        if "invalid literal for int()" in str(e):
            raise ValueError("El ID y los días deben ser números enteros.")
        raise e

def _realizar_devolucion() -> None:
    """Registra la devolución y notifica si se generó una multa."""
    try:
        id_alquiler = int(input("ID del alquiler: "))
    except ValueError:
        raise ValueError("El ID de alquiler debe ser un número entero.")

    # Se usa la fecha actual según el requerimiento
    fecha_hoy = date.today()
    
    # Devolver_pelicula en AlquilerService ya maneja la lógica de multas internamente
    _alquiler_service.devolver_pelicula(id_alquiler, fecha_hoy)
    
    # Verificamos si se creó una multa para informar al usuario
    multas = _multa_service.obtener_multas_por_alquiler(id_alquiler)
    if multas:
        # Mostramos la última multa generada para ese alquiler
        m = multas[-1]
        print(f"⚠️ Devolución con retraso. Multa: {m.importe:.2f}€")
    else:
        print("✅ Devolución registrada correctamente.")

def _ver_alquileres_activos() -> None:
    """Lista los alquileres que aún no han sido devueltos."""
    activos = _alquiler_service.listar_alquileres_activos()
    if not activos:
        print("\nNo hay alquileres activos.")
    else:
        print("\n--- Alquileres en curso ---")
        for a in activos:
            print(a)

# --- Funciones de Reportes y Multas ---

def _ver_multas() -> None:
    """Muestra el histórico de todas las multas en el sistema."""
    multas = _multa_service.listar_todas_las_multas()
    if not multas:
        print("\nNo hay multas registradas.")
    else:
        print("\n--- Historial de Multas ---")
        for m in multas:
            print(m)

def _ver_historial_cliente() -> None:
    """Muestra todos los alquileres (pasados y presentes) de un cliente."""
    try:
        id_cliente = int(input("ID del cliente: "))
    except ValueError:
        raise ValueError("El ID de cliente debe ser un número entero.")

    historial = _alquiler_service.obtener_historial_cliente(id_cliente)
    if not historial:
        print("\nEste cliente no tiene alquileres registrados.")
    else:
        print(f"\n--- Historial del Cliente #{id_cliente} ---")
        for h in historial:
            print(h)