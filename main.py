import funciones as fn

# Carga inicial de los países desde el archivo CSV
paises = fn.cargar_paises()
print(f"{fn.VERDE}Se cargaron {len(paises)} países desde el archivo.{fn.RESET}")

# Menú principal: se repite hasta que el usuario elige 0.
# Agregar y actualizar guardan el CSV en el momento,
# por eso al salir no hace falta volver a guardar.
try:
    while True:
        print("""
========== GESTIÓN DE DATOS DE PAÍSES ==========
1. Mostrar todos los países
2. Agregar un país
3. Actualizar población y superficie
4. Buscar país por nombre
5. Filtrar por continente
6. Filtrar por rango de población
7. Filtrar por rango de superficie
8. Ordenar países
9. Mostrar estadísticas
0. Salir
""")
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "0":
            print(f"{fn.VERDE}Programa finalizado.{fn.RESET}")
            break
        elif opcion == "2":
            fn.agregar_pais(paises)
        elif opcion not in ("1", "3", "4", "5", "6", "7", "8", "9"):
            print(f"{fn.ROJO}Opción inválida. Elegí una opción del menú (0 a 9).{fn.RESET}")
        elif not paises:
            # Las demás opciones necesitan al menos un país cargado
            print(f"{fn.ROJO}Error: no hay países cargados. Agregá uno primero (opción 2).{fn.RESET}")
        elif opcion == "1":
            fn.mostrar_paises(paises)
        elif opcion == "3":
            fn.actualizar_pais(paises)
        elif opcion == "4":
            fn.buscar_menu(paises)
        elif opcion == "5":
            fn.filtrar_continente(paises)
        elif opcion == "6":
            fn.filtrar_rango(paises, "poblacion", "población")
        elif opcion == "7":
            fn.filtrar_rango(paises, "superficie", "superficie")
        elif opcion == "8":
            fn.ordenar_paises(paises)
        elif opcion == "9":
            fn.mostrar_estadisticas(paises)
except (KeyboardInterrupt, EOFError):
    # Ctrl+C o fin de entrada: se sale sin mostrar el error de Python
    print(f"{fn.ROJO}\nPrograma interrumpido por el usuario.{fn.RESET}")

