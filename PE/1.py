#Ejercicio: El problema se reduce a una variante problema de mochila (0/1). 
# donde cada persona tiene un consumo individual de tres tipos de bebida A, B y C.

#Solución: 
# Podemos incluir o excluir a cada persona en nuestra selección.

# Para que k personas puedan ser seleccionadas, la suma de los consumos máximos de A, B y C
# entre ellas debe cumplir que max_A + max_B + max_C <= 10,000.


def max_cantidad(index, personas, max_bebidas):
    if index == len(personas):
        # Caso base: Ya hemos evaluado a todas las personas
        return 0

    #Devuelve una 3-tupla con los consumos A, B y C de la persona actual
    persona = personas[index]

    #Calculamos los nuevos consumos máximos max_A, max_B y max_C
    nuevos_maximos = [
        #Devuelve el máximo valor entre el consumo máximo previo y el consumo de esa persona
        max(max_bebidas[0], persona[0]),
        max(max_bebidas[1], persona[1]),
        max(max_bebidas[2], persona[2])
    ]

    # Caso 1: Incluimos a la persona en la solución óptima
    incluir = 0
    
    # Verificamos si la persona presenta un consumo válido,
    # si la suma de los máximos no excede el límite
    if sum(nuevos_maximos) <= 10000:
        # Sumamos 1 por incluir a esta persona, y continuamos con el resto
        incluir = 1 + max_cantidad(index + 1, personas, nuevos_maximos)

    # Caso 2: Excluimos a la persona en la solución óptima
    excluir = max_cantidad(index + 1, personas, max_bebidas)

    # Retornamos el máximo entre incluir o no incluir a la persona actual
    return max(incluir, excluir)


T = int(input()) #Número de casos de prueba

for caso in range(1, T + 1):
    N = int(input()) # Número de personas
    personas = []

    # Leemos los consumos A, B y C de cada persona
    for _ in range(N):
        A, B, C = map(int, input().split())
        personas.append((A, B, C))

     # Iniciamos la búsqueda con consumos máximos en 0
    resultado = max_cantidad(0, personas, [0, 0, 0])

     # Mostramos el resultado del caso actual
    print(f"Caso #{caso}: {resultado}")


