import csv
import os

# Ruta del CSV: se busca en la misma carpeta que este archivo,
# así el programa funciona sin importar desde qué carpeta se ejecute.
ARCHIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]

# Colores para la terminal (códigos ANSI, no requieren instalar nada).
# Se escriben antes del texto y RESET vuelve al color normal.
ROJO = "\033[91m"      # errores y avisos
VERDE = "\033[92m"     # acciones exitosas
AMARILLO = "\033[93m"  # búsquedas o filtros sin resultados
CIAN = "\033[96m"      # resultados (tablas y estadísticas)
RESET = "\033[0m"

# En Windows, esta línea activa los colores en la consola (cmd / PowerShell)
os.system("")


def cargar_paises(ruta=ARCHIVO_CSV):
    """Lee el CSV y devuelve una lista de diccionarios.
    Las filas con errores de formato o repetidas se informan y se omiten."""
    paises = []
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames is None or not all(campo in lector.fieldnames for campo in CAMPOS):
                print(f"{ROJO}Error: el CSV debe tener las columnas {', '.join(CAMPOS)}.{RESET}")
                return paises

            # La línea 1 es el encabezado, por eso los datos empiezan en la 2
            for numero_linea, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])
                    if not nombre or not continente or poblacion <= 0 or superficie <= 0:
                        raise ValueError
                except (ValueError, TypeError, AttributeError):
                    # TypeError/AttributeError: la fila tiene columnas de menos
                    print(f"{ROJO}Aviso: línea {numero_linea} del CSV con datos inválidos, se omite.{RESET}")
                    continue

                if existe_pais(paises, nombre):
                    print(f"{ROJO}Aviso: línea {numero_linea} repite el país '{nombre}', se omite.{RESET}")
                    continue

                paises.append({
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente,
                })

    except FileNotFoundError:
        print(f"{ROJO}Aviso: no se encontró el archivo {ruta}. Se empieza con una lista vacía.{RESET}")
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        print(f"{ROJO}Error al leer el CSV: {error}{RESET}")

    return paises


def guardar_paises(paises, ruta=ARCHIVO_CSV):
    """Sobrescribe el CSV con la lista completa de países.
    Devuelve True si se guardó correctamente y False si hubo un error."""
    try:
        with open(ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        return True
    except OSError as error:
        print(f"{ROJO}Error: no se pudieron guardar los datos: {error}{RESET}")
        return False


def mostrar_paises(paises):
    """Muestra una lista de países en forma de tabla."""
    if not paises:
        print(f"{AMARILLO}No se encontraron países.{RESET}")
        return

    print(f"{CIAN}\n{'PAÍS':<20} {'POBLACIÓN':>15} {'SUPERFICIE km²':>16}   CONTINENTE")
    print("-" * 70)
    for pais in paises:
        print(f"{pais['nombre']:<20} {pais['poblacion']:>15,} "
              f"{pais['superficie']:>16,}   {pais['continente']}")
    print(f"\nTotal: {len(paises)} país(es).{RESET}")


def leer_entero(mensaje, minimo=1):
    """Pide un número entero mayor o igual a 'minimo' y lo repite hasta que sea válido."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"{ROJO}Error: el valor debe ser mayor o igual a {minimo}.{RESET}")
            else:
                return valor
        except ValueError:
            print(f"{ROJO}Error: ingresá un número entero (sin puntos ni comas).{RESET}")


def existe_pais(paises, nombre):
    """Devuelve True si ya hay un país con ese nombre (sin importar mayúsculas)."""
    nombre = nombre.strip().casefold()
    return any(pais["nombre"].casefold() == nombre for pais in paises)


def agregar_pais(paises):
    """Opción 2: pide todos los datos de un país nuevo, lo agrega y guarda el CSV.
    No se permiten campos vacíos ni países repetidos."""
    nombre = input("Nombre del país: ").strip()
    if not nombre:
        print(f"{ROJO}Error: el nombre no puede estar vacío.{RESET}")
        return
    if existe_pais(paises, nombre):
        print(f"{ROJO}Error: el país '{nombre}' ya existe en el dataset.{RESET}")
        return

    poblacion = leer_entero("Población: ")
    superficie = leer_entero("Superficie en km²: ")
    continente = input("Continente: ").strip()
    if not continente:
        print(f"{ROJO}Error: el continente no puede estar vacío. No se agregó el país.{RESET}")
        return

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })

    if guardar_paises(paises):
        print(f"{VERDE}Éxito: '{nombre}' fue agregado y guardado en el CSV.{RESET}")


def actualizar_pais(paises):
    """Opción 3: busca un país y actualiza su población y superficie."""
    texto = input("País que desea actualizar: ").strip()
    resultados = buscar_paises(paises, texto)
    if not resultados:
        print(f"{ROJO}Error: no se encontró el país '{texto}'.{RESET}")
        return

    # Si se escribió el nombre exacto se usa ese; si no, se elige entre las coincidencias
    exactos = [p for p in resultados if p["nombre"].casefold() == texto.casefold()]
    if exactos:
        pais = exactos[0]
    elif len(resultados) == 1:
        pais = resultados[0]
    else:
        print("\nSe encontraron varias coincidencias:")
        for i, p in enumerate(resultados, start=1):
            print(f"{i}. {p['nombre']}")
        indice = leer_entero("Seleccioná el número del país: ")
        while indice > len(resultados):
            print(f"{ROJO}Error: elegí un número entre 1 y {len(resultados)}.{RESET}")
            indice = leer_entero("Seleccioná el número del país: ")
        pais = resultados[indice - 1]

    print(f"{CIAN}País seleccionado: {pais['nombre']} "
          f"(población: {pais['poblacion']:,} | superficie: {pais['superficie']:,} km²){RESET}")
    # Como el diccionario está dentro de la lista, el cambio se ve en la lista
    pais["poblacion"] = leer_entero("Nueva población: ")
    pais["superficie"] = leer_entero("Nueva superficie en km²: ")

    if guardar_paises(paises):
        print(f"{VERDE}Éxito: '{pais['nombre']}' fue actualizado y guardado en el CSV.{RESET}")


def buscar_paises(paises, texto):
    """Devuelve los países cuyo nombre contiene el texto (coincidencia parcial).
    Si se escribe el nombre completo también lo encuentra (coincidencia exacta)."""
    texto = texto.strip().casefold()
    if not texto:
        return []
    return [pais for pais in paises if texto in pais["nombre"].casefold()]


def buscar_menu(paises):
    """Opción 4: pide un texto y muestra las coincidencias."""
    texto = input("Ingresá el nombre completo o una parte: ").strip()
    if not texto:
        print(f"{ROJO}Error: la búsqueda no puede estar vacía.{RESET}")
        return
    resultado = buscar_paises(paises, texto)
    if resultado:
        mostrar_paises(resultado)
    else:
        print(f"{AMARILLO}No se encontraron países que coincidan con '{texto}'.{RESET}")


def filtrar_continente(paises):
    """Opción 5: muestra los países del continente indicado."""
    continentes = sorted({pais["continente"] for pais in paises})
    print(f"{CIAN}Continentes disponibles: {', '.join(continentes)}{RESET}")
    continente = input("Continente: ").strip().casefold()

    resultado = [p for p in paises if p["continente"].casefold() == continente]
    if resultado:
        mostrar_paises(resultado)
    else:
        print(f"{AMARILLO}No hay países en ese continente. Escribilo como aparece en la lista.{RESET}")


def filtrar_rango(paises, campo, etiqueta):
    """Opciones 6 y 7: muestra los países cuyo 'campo' ("poblacion" o "superficie")
    está entre un mínimo y un máximo (ambos incluidos)."""
    minimo = leer_entero(f"Valor mínimo de {etiqueta}: ", 0)
    maximo = leer_entero(f"Valor máximo de {etiqueta}: ", 0)
    if minimo > maximo:
        print(f"{ROJO}Error: el mínimo no puede ser mayor que el máximo.{RESET}")
        return

    resultado = [p for p in paises if minimo <= p[campo] <= maximo]
    if resultado:
        mostrar_paises(resultado)
    else:
        print(f"{AMARILLO}No hay países con {etiqueta} entre {minimo:,} y {maximo:,}.{RESET}")


def ordenar_paises(paises):
    """Opción 8: muestra los países ordenados por nombre, población o superficie,
    en forma ascendente o descendente. sorted() no modifica la lista original."""
    print("1. Nombre\n2. Población\n3. Superficie")
    opcion = input("Criterio: ").strip()
    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in campos:
        print(f"{ROJO}Error: criterio inválido.{RESET}")
        return

    print("1. Ascendente\n2. Descendente")
    sentido = input("Sentido: ").strip()
    if sentido not in ("1", "2"):
        print(f"{ROJO}Error: sentido inválido.{RESET}")
        return

    campo = campos[opcion]
    if campo == "nombre":
        clave = lambda p: p["nombre"].casefold()
    else:
        clave = lambda p: p[campo]
    mostrar_paises(sorted(paises, key=clave, reverse=(sentido == "2")))


def mostrar_estadisticas(paises):
    """Opción 9: mayor y menor población, promedios y cantidad por continente."""
    if not paises:
        print(f"{AMARILLO}No hay datos para calcular estadísticas.{RESET}")
        return

    mayor = max(paises, key=lambda p: p["poblacion"])
    menor = min(paises, key=lambda p: p["poblacion"])
    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)

    # Diccionario acumulador {continente: cantidad}
    cantidades = {}
    for pais in paises:
        continente = pais["continente"]
        cantidades[continente] = cantidades.get(continente, 0) + 1

    print(f"{CIAN}\nPaís con mayor población: {mayor['nombre']} ({mayor['poblacion']:,} hab.){RESET}")
    print(f"{CIAN}País con menor población: {menor['nombre']} ({menor['poblacion']:,} hab.){RESET}")
    print(f"{CIAN}Promedio de población: {promedio_poblacion:,.2f} hab.{RESET}")
    print(f"{CIAN}Promedio de superficie: {promedio_superficie:,.2f} km²{RESET}")

    print(f"{CIAN}\nCantidad de países por continente:{RESET}")
    for continente, cantidad in sorted(cantidades.items()):
        print(f"{CIAN}- {continente}: {cantidad}{RESET}")
