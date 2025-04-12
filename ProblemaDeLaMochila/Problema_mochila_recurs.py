def maxValorRetirado(W, j, pesos, valores):
    assert j >= 0 
    assert len(pesos) == len(valores)
    
    if W == 0:
        return 0
    if W < 0:  # Se han agregado más ítems a la mochila de lo que permite su capacidad
        return -float('inf')
    if j >= len(pesos):
        return 0
    # A continuación, se maneja la recurrencia.
    return max(
        valores[j] + maxValorRetirado(W - pesos[j], j+1, pesos, valores),  # remover el ítem j
        maxValorRetirado(W, j+1, pesos, valores)  # omitir el ítem j
    )

#T(w,j)= T(w-c,j+1) + T(w, j+1)