#Ejercicio: El problema se reduce a encontrar el número de nodos del ciclo más largo en un grafo

#Utilizamos networkx para la construcción del grafo, librería usada en clase
import networkx as nx

#Solución: Buscamos ciclos válidos usando DFS con backtracking, encontramos los ciclos válidos y devolvemos el número de nodos k del ciclo de mayor longitud
#Función que tiene como entrada un grafo y retorna el número de nodos k del ciclo más largo
def encontrar_ciclo_mas_largo(G):
    max_largo = 0  #Número de nodos del ciclo más largo

    #Función que realiza búsqueda en profundidad (DFS) para encontrar ciclos váñidos
    def dfs_buscar_ciclo(nodo_actual, inicio, visitados, largo_actual):
        nonlocal max_largo

        # Marcamos el nodo actual como visitado
        visitados.add(nodo_actual)

        # Exploramos los vecinos del nodo actual
        for vecino in G.neighbors(nodo_actual):
            if vecino == inicio and largo_actual >= 3:
                # Si volvemos al nodo inicial y el ciclo tiene al menos 3 nodos, es un ciclo válido
                max_largo = max(max_largo, largo_actual)
            elif vecino not in visitados:
                # Si el vecino no ha sido visitado, continuamos explorando
                dfs_buscar_ciclo(vecino, inicio, visitados, largo_actual + 1)

        # Backtracking, desmarcamos el nodo actual
        visitados.remove(nodo_actual)

    # Probamos iniciar la búsqueda desde cada nodo del grafo
    for nodo in G.nodes:
       dfs_buscar_ciclo(nodo, nodo, set(), 1)

    # Retornamos el tamaño del ciclo más largo encontrado
    return max_largo


T = int(input()) #Número de casos de prueba

for caso in range(1, T + 1):
    N = int(input()) #Número de nodos en el grafo
    #Diccionario de adyacencoa qie define el estado inicial del grafo
    adjacency_dict = {1: (2, 3), 2: (1, 3), 3: (1, 2)}
    
    # Para nodos desde 4 hasta N, leemos las conexiones y las añadimos
    for i in range(4, N + 1):
        A, B = map(int, input().split()) 
        adjacency_dict[i] = [A, B] # Nodo i está conectado con A y B
    
    # Construimos el grafo con networkx a partir del diccionario de adyacencia
    H = nx.Graph(adjacency_dict)
    
    # Ejecutamos el algoritmo para encontrar el ciclo más largo
    resultado = encontrar_ciclo_mas_largo(H)
    print(f"Caso #{caso}: {resultado}")
