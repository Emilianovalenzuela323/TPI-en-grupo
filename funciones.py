import csv
import os

ARCHIVO_CSV = os.path.join(os.path.dirname(__file__), "dataset.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


def cargar_paises(ruta=ARCHIVO_CSV):
    """Lee el CSV y devuelve una lista de diccionarios."""
    paises = []
    try:
        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames is None or not all(campo in lector.fieldnames for campo in CAMPOS):
                raise ValueError("El CSV no contiene todas las columnas requeridas.")

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])

                    if not nombre or not continente or poblacion < 0 or superficie <= 0:
                        raise ValueError

                    paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente
                    })
                except (ValueError, TypeError, AttributeError):
                    print(f"Aviso: se omitió la fila {numero_fila} por tener datos inválidos.")

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {ruta}.")
    except (OSError, csv.Error, ValueError) as error:
        print(f"Error al leer el CSV: {error}")

    return paises


def guardar_paises(paises, ruta=ARCHIVO_CSV):
    """Guarda la lista completa de países en el CSV."""
    try:
        with open(ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        return True
    except OSError as error:
        print(f"No se pudieron guardar los datos: {error}")
        return False


def mostrar_paises(paises):
    if not paises:
        print("No se encontraron países.")
        return

    print(f"\n{'PAÍS':<22} {'POBLACIÓN':>15} {'SUPERFICIE km²':>17} {'CONTINENTE':<15}")
    print("-" * 75)
    for pais in paises:
        print(f"{pais['nombre']:<22} {pais['poblacion']:>15,} {pais['superficie']:>17,} {pais['continente']:<15}")


def leer_entero(mensaje, minimo=0):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"El valor debe ser mayor o igual que {minimo}.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Ingresá un número entero.")


def existe_pais_exacto(paises, nombre):
    """Verifica si un país ya existe por coincidencia exacta."""
    nombre_limpio = nombre.strip().casefold()
    return any(p["nombre"].casefold() == nombre_limpio for p in paises)


def agregar_pais(paises):
    nombre = input("Nombre del país: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    if existe_pais_exacto(paises, nombre):
        print("Ese país ya existe en el dataset.")
        return

    poblacion = leer_entero("Población: ")
    superficie = leer_entero("Superficie en km² (mayor que 0): ", 1)
    continente = input("Continente: ").strip()

    if not continente:
        print("El continente no puede estar vacío.")
        return

    paises.append({
        "nombre": nombre.title(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.title()
    })

    if guardar_paises(paises):
        print("País agregado y guardado correctamente.")


def actualizar_pais(paises):
    nombre = input("País que desea actualizar: ").strip()
    resultados = buscar_paises(paises, nombre)

    if not resultados:
        print("No se encontró el país.")
        return
    pais = []
    if len(resultados) > 1:
        print("\nSe encontraron varias coincidencias:")
        for i, p in enumerate(resultados, start=1):
            print(f"{i}. {p['nombre']}")
        indice = leer_entero("Seleccioná el número del país: ", 1)
        if indice > len(resultados):
            print("Selección inválida.")
            return
        pais = resultados[indice - 1]
    else:
        pais = resultados[0]

    print(f"País seleccionado: {pais['nombre']}")
    pais["poblacion"] = leer_entero("Nueva población: ")
    pais["superficie"] = leer_entero("Nueva superficie en km² (mayor que 0): ", 1)

    if guardar_paises(paises):
        print("Datos actualizados correctamente.")


def buscar_paises(paises, texto):
    texto = texto.strip().casefold()
    if not texto:
        return []
    return [pais for pais in paises if texto in pais["nombre"].casefold()]


def buscar_menu(paises):
    texto = input("Ingresá el nombre completo o una parte: ")
    mostrar_paises(buscar_paises(paises, texto))


def filtrar_continente(paises):
    continente = input("Continente: ").strip().casefold()
    resultado = [p for p in paises if p["continente"].casefold() == continente]
    mostrar_paises(resultado)


def filtrar_rango(paises, campo, etiqueta):
    minimo = leer_entero(f"Valor mínimo de {etiqueta}: ")
    maximo = leer_entero(f"Valor máximo de {etiqueta}: ")
    if minimo > maximo:
        print("El mínimo no puede ser mayor que el máximo.")
        return
    resultado = [p for p in paises if minimo <= p[campo] <= maximo]
    mostrar_paises(resultado)


def ordenar_paises(paises):
    print("1. Nombre\n2. Población\n3. Superficie")
    opcion = input("Criterio: ").strip()
    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}

    if opcion not in campos:
        print("Opción inválida.")
        return

    descendente = False
    if opcion != "1":
        sentido = input("1. Ascendente\n2. Descendente\nSentido: ").strip()
        if sentido not in ("1", "2"):
            print("Sentido inválido.")
            return
        descendente = sentido == "2"

    resultado = sorted(
        paises,
        key=lambda p: p[campos[opcion]].casefold() if opcion == "1" else p[campos[opcion]],
        reverse=descendente
    )
    mostrar_paises(resultado)


def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos para calcular estadísticas.")
        return

    mayor = max(paises, key=lambda p: p["poblacion"])
    menor = min(paises, key=lambda p: p["poblacion"])
    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)

    cantidades = {}
    for pais in paises:
        continente = pais["continente"]
        cantidades[continente] = cantidades.get(continente, 0) + 1

    print(f"\nMayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,})")
    print(f"Promedio de población: {promedio_poblacion:,.2f}")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km²")

    print("\nCantidad de países por continente:")
    for continente, cantidad in sorted(cantidades.items()):
        print(f"- {continente}: {cantidad}")
