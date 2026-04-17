# 🎬 VideoClub — Sistema de Gestión de Alquiler de Películas

Sistema de gestión de videoclub desarrollado en Python con interfaz de consola.
Permite administrar películas, clientes y alquileres con cálculo automático de multas por retraso, usando SQLite como base de datos persistente.

---

## ✅ Requisitos previos

- **Python** 3.10 o superior
- **SQLite3** (incluido en la biblioteca estándar de Python)
- Sin dependencias externas adicionales

```bash
python --version   # debe mostrar Python 3.10+
```

---

## ⚙️ Instalación y configuración

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/videoclub.git
cd videoclub

# 2. (Opcional) Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instala dependencias (solo stdlib, sin requirements.txt necesario)
# No se requiere ningún paso adicional

# 4. La base de datos video_club.db se crea automáticamente al iniciar
```

---

## ▶️ Cómo ejecutar el sistema

```bash
python main.py
```

Al iniciar, se crea automáticamente el archivo `video_club.db` con todas las tablas necesarias.

---

## 🧪 Cómo ejecutar los tests

```bash
# Ejecutar todos los tests
python -m unittest tests/test_videoclub.py -v

# Salida esperada
# test_alquiler_bloqueado_sin_copias ... ok
# test_devolucion_con_multa ... ok
# test_devolucion_puntual_sin_multa ... ok
# ...
```

---

## 📁 Estructura de archivos

```
video_club/
├── __init__.py
├── models/
│   ├── pelicula.py             # Entidad Pelicula (código, título, copias)
│   ├── cliente.py              # Entidad Cliente (ID, nombre, email)
│   ├── alquiler.py             # Entidad Alquiler (fechas, estado)
│   └── multa.py                # Entidad Multa — tarifa: 1.50 €/día
├── database/
│   ├── connection.py           # Conexión SQLite y creación de tablas
│   └── init_db.py              # Inicialización y población inicial de la BD
├── repositories/
│   ├── pelicula_repository.py  # Acceso a datos de películas (SQL)
│   ├── cliente_repository.py   # Acceso a datos de clientes (SQL)
│   └── alquiler_repository.py  # Acceso a datos de alquileres (SQL)
├── services/
│   ├── pelicula_service.py     # Lógica de negocio de películas
│   ├── cliente_service.py      # Lógica de negocio de clientes
│   ├── alquiler_service.py     # Lógica de alquiler y devolución
│   └── multa_service.py        # Cálculo y registro de multas
├── ui/
│   └── menu.py                 # Menú interactivo de consola
├── tests/
│    └── test_alquiler_service.py   
|    └── test_cliente_service.py
|    └── test_cliente.py
|    └── test_multa.py
|    └── test_pelicula.py
|    └── test_videoclub.py      # Suite de tests con pytest
└── main.py                     # Punto de entrada de la aplicación
```

---

## 🚀 Guía de uso rápido

### Flujo completo de ejemplo

```
========================================
     🎬 VIDEOCLUB — MENÚ PRINCIPAL
========================================
 1. Gestión de películas
 2. Gestión de clientes
 3. Alquilar película
 4. Devolver película
 5. Ver historial de cliente
 0. Salir
========================================
Selecciona una opción: 1

--- GESTIÓN DE PELÍCULAS ---
 1. Añadir película
 2. Listar todas
 3. Buscar por código
Opción: 1

Código:  PEL001
Título:  Interstellar
Género:  Ciencia Ficción
Copias disponibles: 3
✅ Película añadida correctamente.

--- Registrar cliente ---
ID cliente:   CLI001
Nombre:       Ana García
Email:        ana@email.com
✅ Cliente registrado.

--- ALQUILAR PELÍCULA ---
ID cliente:   CLI001
Código película: PEL001
Fecha devolución prevista (YYYY-MM-DD): 2025-08-10
✅ Alquiler registrado. ID de alquiler: ALQ001

--- DEVOLVER PELÍCULA ---
ID alquiler: ALQ001
Fecha de devolución real (YYYY-MM-DD): 2025-08-13
⚠️  Devolución con 3 días de retraso.
💶 Multa generada: 4.50 € (3 días × 1.50 €/día)
✅ Devolución registrada correctamente.
```

---

## 🧠 Decisiones de diseño

| Decisión | Justificación |
|----------|---------------|
| **SQLite** como base de datos | Sin instalación de servidor; portabilidad total del archivo `.db` |
| **Arquitectura por capas** (models / repositories / services / ui) | Separación de responsabilidades: repositories solo hablan con SQL, services solo con lógica de negocio |
| **Multa de 1.50 €/día** | Calculada solo sobre días de retraso; devolución anticipada → 0 € |
| **Bloqueo de alquiler** sin copias | Control en `alquiler_service` antes de modificar el inventario |
| **IDs manuales** (PEL001, CLI001…) | Simplicidad en la interfaz de consola sin depender de autoincremento |
| **unittest** estándar | Sin dependencias externas; integrado en Python 3 |

---

## 👤 Autor

**Tu Nombre** · Carlos   
🐍 Python 3.10+ · 🗄️ SQLite3 · 🖥️ Interfaz de consola
