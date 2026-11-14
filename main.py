import funciones as fn


def mostrar_menu():
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
0. Guardar y salir
""")


def main():
    paises = fn.cargar_paises()
    if not paises:
        print("No se cargaron registros. Revisá el archivo dataset.csv.")
    while True:
        mostrar_menu()
        opcion = input("Seleccioná una opción: ").strip()
        if opcion == "1":
            fn.mostrar_paises(paises)
        elif opcion == "2":
            fn.agregar_pais(paises)
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
        elif opcion == "0":
            fn.guardar_paises(paises)
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Elegí una opción del menú.")


if __name__ == "__main__":
    main()