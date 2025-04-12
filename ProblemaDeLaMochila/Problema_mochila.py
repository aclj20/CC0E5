def memoizedMaxValorRetirado(W, pesos, valores):
    n = len(pesos)
    assert (len(valores) == n)
    assert (W>=0)

    if W == 0:
        return 0, []
    
    T = [[0 for j in range(n)] for w in range(W+1)]
    S = [[0 for j in range(n)] for w in range(W+1)]

    def getTblEntry(w, j): 
        if w == 0: 
            return 0
        if w < 0: 
            return -float('inf')
        if j >= n:
            return 0
        return T[w][j]
    
    for w in range(1, W+1):  #O(w)
        for j in range(n-1, -1, -1): #O(n)
            (T[w][j], S[w][j]) = max(
                (valores[j] + getTblEntry(w - pesos[j], j+1), 1), 
                (getTblEntry(w, j+1), 0)
            ) 

    itemsToSteal = []
    weightOfKnapsack = W  

    for j in range(n): 
        if (S[weightOfKnapsack][j] == 1):
            itemsToSteal.append(j)
            weightOfKnapsack = weightOfKnapsack - pesos[j]
            print(f'Remover ítem {j}: Peso = {pesos[j]}, Valor = {valores[j]}')
    
    print(f'Peso total retirado: {W - weightOfKnapsack}, valor = {T[W][0]}')
    return (T[W][0], itemsToSteal)



W = 50
pesos = [1, 5, 20, 35, 90]  
valores = [15, 14.5, 19.2, 19.8, 195.2]

a, itemToSteal = memoizedMaxValorRetirado(W, pesos, valores)

#Lista con las tuplas
lista =[]
for item in itemToSteal:
    j = item
    tupla = (item, pesos[item], valores[item])
    lista.append(tupla)

print(lista)