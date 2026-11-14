# Gestión de Datos de Países en Python

Trabajo Práctico Integrador – Programación 1
Tecnicatura Universitaria en Programación a Distancia – UTN

## Descripción

Aplicación de consola en Python 3 que gestiona información de países. Los datos se leen desde `dataset.csv` y se cargan en una **lista de diccionarios** (un diccionario por país con las claves `nombre`, `poblacion`, `superficie` y `continente`). Permite agregar, actualizar, buscar, filtrar, ordenar países y calcular estadísticas. Los cambios se guardan en el CSV en el momento.

## Estructura del proyecto

Archivo --> Contenido 
| `main.py` --> Programa principal: carga los datos, muestra el menú y llama a cada opción. No define funciones.
| `funciones.py` --> Las funciones del sistema: leer/guardar el CSV, mostrar, agregar, actualizar, buscar, filtrar, ordenar y estadísticas.
| `dataset.csv` --> Dataset base de países.
| `documentacion.pdf` --> Documentación académica y técnica.

## Instrucciones de uso

Requiere Python 3 (no usa librerías externas). Desde la carpeta del proyecto:

```
python main.py
```

Menú principal:

```
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
```

## Validaciones

- Columnas faltantes en el CSV, filas con datos inválidos o países repetidos: se informa la línea y se omite.
- Si no existe el CSV, se empieza con una lista vacía.
- No se permiten campos vacíos; población y superficie deben ser enteros mayores a 0.
- No se puede agregar un país que ya existe (sin distinguir mayúsculas: "perú" = "Perú").
- En los rangos, el mínimo no puede ser mayor que el máximo.
- Búsquedas y filtros sin resultados muestran un mensaje en lugar de fallar.
- Si se elige una opción inválida, se muestra un mensaje de error y se vuelve al menú.

## Ejemplos de entradas y salidas

**Buscar (coincidencia parcial)**
```
Seleccioná una opción: 4
Ingresá el nombre completo o una parte: per

PAÍS                       POBLACIÓN   SUPERFICIE km²   CONTINENTE
----------------------------------------------------------------------
Perú                      34,352,719        1,285,216   América

Total: 1 país(es).
```

**Filtrar por rango de población**
```
Seleccioná una opción: 6
Valor mínimo de población: 100
Valor máximo de población: 10
Error: el mínimo no puede ser mayor que el máximo.
```

**Agregar un país**
```
Seleccioná una opción: 2
Nombre del país: Kenia
Población: abc
Error: ingresá un número entero (sin puntos ni comas).
Población: 55100000
Superficie en km²: 580367
Continente: África
Éxito: 'Kenia' fue agregado y guardado en el CSV.
```

**Estadísticas**
```
Seleccioná una opción: 9

País con mayor población: India (1,428,627,663 hab.)
País con menor población: Uruguay (3,423,108 hab.)
Promedio de población: 182,959,176.36 hab.
Promedio de superficie: 2,226,296.08 km²

Cantidad de países por continente:
- América: 8
- Asia: 5
- Europa: 6
- Oceanía: 2
- África: 4
```

## Integrantes y participación

- Emiliano Valenzuela: Creó el repositorio del proyecto, Realizó análisis inicial del proyecto, Creó primer borrador del proyecto,
- Fausto Mariño: Realizó análisis inicial del proyecto, Subió los archivos al repositorio, Corrigió los archivos y el programa,

## Enlaces

- Video demostrativo: [COMPLETAR – link público]
