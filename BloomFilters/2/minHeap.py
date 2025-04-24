# Completemos primero la implementación de una estructura de min-heap.
# Por favor, completa las partes faltantes a continuación.

class MinHeap:
    def __init__(self):
        self.H = [None]  # Usamos H[0] como posición sin usar
 
    def size(self):
        return len(self.H) - 1
    
    def __repr__(self):
        return str(self.H[1:])
        
    def satisfies_assertions(self):
        for i in range(2, len(self.H)):
            assert self.H[i] >= self.H[i // 2], f'La propiedad de min-heap falla en la posición {i // 2}, elemento padre: {self.H[i // 2]}, elemento hijo: {self.H[i]}'
    
    def min_element(self):
        return self.H[1]

    # Función bubble_up en el índice dado
    # ADVERTENCIA: esta función se ha copiado y pegado para el siguiente problema también
    def bubble_up(self, index):
        assert index >= 1
        if index == 1:
            return
        # Completa el codigo
        elem = self.H[index]
        while(index > 1):
            parent_index = index // 2
            if elem < self.H[parent_index]:
                self.H[index] = self.H[parent_index]
                index = parent_index
            else:
                break
        self.H[index] = elem
        # COMPLETADO
    
    # Función bubble_down en el índice dado
    # ADVERTENCIA: esta función se ha copiado y pegado para el siguiente problema también
    def bubble_down(self, index):
        assert index >= 1 and index < len(self.H)
        # Completa el codigo
        left = index*2
        right = index*2 + 1
        m = index
        if (left <= self.size() and self.H[left] < self.H[m]):
            m = left
        if (right <= self.size() and self.H[right] < self.H[m]):
            m = right
        if index != m:
            self.H[m], self.H[index] = self.H[index], self.H[m]
            # Bubble down en el hijo menor
            self.bubble_down(m)
        return 
        # COMPLETADO
        
    # Función: insert (inserta un elemento en el heap)
    # Usa las funciones bubble_up y bubble_down
    def insert(self, elt):
        self.H.append(elt)
        self.bubble_up(len(self.H) - 1)
        
    # Función: delete_min (elimina el elemento mínimo del heap)
    def delete_min(self):
        if self.size() == 0:
            raise Exception("El heap está vacío")

        self.H[1] = self.H[-1]
        # Elimina el último elemento
        self.H.pop()
        if self.size() > 0:  # Si aún queda algún elemento, aplica bubble_down
            self.bubble_down(1)

h = MinHeap()
print('Insertando: 5, 2, 4, -1 y 7 en ese orden.')
h.insert(5)
print(f'\t Heap = {h}')
assert(h.min_element() == 5)
h.insert(2)
print(f'\t Heap = {h}')
assert(h.min_element() == 2)
h.insert(4)
print(f'\t Heap = {h}')
assert(h.min_element() == 2)
h.insert(-1)
print(f'\t Heap = {h}')
assert(h.min_element() == -1)
h.insert(7)
print(f'\t Heap = {h}')
assert(h.min_element() == -1)
h.satisfies_assertions()

print('Eliminando el menor elemento')
h.delete_min()
print(f'\t Heap = {h}')
assert(h.min_element() == 2), 'El elemento mínimo del heap ya no es 2'
h.delete_min()
print(f'\t Heap = {h}')
assert(h.min_element() == 4)
h.delete_min()
print(f'\t Heap = {h}')
assert(h.min_element() == 5)
h.delete_min()
print(f'\t Heap = {h}')
assert(h.min_element() == 7)
h.delete_min()
print(f'\t Heap = {h}')
print('All tests passed: 10 points!')

class TopKHeap:
    
    # Constructor: inicializa una estructura de datos vacía
    def __init__(self, k):
        self.k = k
        self.A = []
        self.H = MinHeap()
        
    def size(self):
        return len(self.A) + self.H.size()
    
    def get_jth_element(self, j):
        assert 0 <= j < self.k
        assert j < self.size()
        return self.A[j]
    
    def satisfies_assertions(self):
        # Verificar que A esté ordenado
        for i in range(len(self.A) - 1):
            assert self.A[i] <= self.A[i + 1], f'El arreglo A no está ordenado en la posición {i}: {self.A[i]}, {self.A[i+1]}'
        # Verificar que H sea un heap (propiedad de min-heap)
        self.H.satisfies_assertions()
        # Verificar que cada elemento de A sea menor o igual que el elemento mínimo de H
        for i in range(len(self.A)):
            assert self.A[i] <= self.H.min_element(), f'El elemento A[{i}] = {self.A[i]} es mayor que el elemento mínimo del heap {self.H.min_element()}'
        
    # Función: insert_into_A
    # Esta función auxiliar inserta un elemento 'elt' en self.A.
    # Si el tamaño es menor que k, simplemente se agrega 'elt' al final del arreglo A
    # y se reubica para que A permanezca ordenado.
    def insert_into_A(self, elt):
        print("k =", self.k)
        assert(self.size() < self.k)
        self.A.append(elt)
        j = len(self.A) - 1
        while j >= 1 and self.A[j] < self.A[j - 1]:
            # Intercambiar A[j] y A[j-1]
            (self.A[j], self.A[j - 1]) = (self.A[j - 1], self.A[j])
            j = j - 1
        return
    
    # Función: insert -- inserta un elemento en la estructura de datos
    # El código para el caso cuando self.size() < self.k ya está proporcionado
    def insert(self, elt):
        size = self.size()
        # Si tenemos menos de k elementos, se maneja de forma especial
        if size <= self.k:
            self.insert_into_A(elt)
            return
        # Escribe tu algoritmo a partir de aquí:
        else:
            if elt < self.A[-1]:
                self.H.insert(self.A[-1])
                self.A = self.A[0:-1]
                self.A.append(elt)
                j = len(self.A) - 1
                while j >= 1 and self.A[j] < self.A[j - 1]:
                    (self.A[j], self.A[j - 1]) = (self.A[j - 1], self.A[j])
                    j = j - 1
                self.H.bubble_up(self.H.size())
            else:
                self.H.insert(elt)
        return
    
    # Función: delete_top_k
    # Elimina un elemento del arreglo A, es decir, elimina el elemento en la posición j (donde j = 0 es el menor)
    # j debe estar en el rango de 0 a self.k - 1
    def delete_top_k(self, j):
        k = self.k
        assert self.size() > k  # se asume que hay más de k elementos
        assert j >= 0
        assert j < self.k
        # Completa el código
        for i in range(j, len(self.A)-1):
            self.A[i] = self.A[i+1]
        self.A = self.A[0:-1]
        self.A.append(self.H.min_element())
        self.H.delete_min()
        # COMPLETADO

h = TopKHeap(5)
# Forzar el arreglo A
h.A = [-10, -9, -8, -4, 0]
# Forzar el heap con estos elementos
[h.H.insert(elt) for elt in [1, 4, 5, 6, 15, 22, 31, 7]]

print('Estructura de datos inicial: ')
print('\t A = ', h.A)
print('\t H = ', h.H)

# Insertar el elemento -2
print('Test 1: Insertando el elemento -2')
h.insert(-2)
print('\t A = ', h.A)
print('\t H = ', h.H)
assert h.A == [-10, -9, -8, -4, -2]
assert h.H.min_element() == 0, 'El elemento mínimo del heap ya no es 0'
h.satisfies_assertions()

print('Test2: Insertando el elemento -11')
h.insert(-11)
print('\t A = ', h.A)
print('\t H = ', h.H)
assert h.A == [-11, -10, -9, -8, -4]
assert h.H.min_element() == -2
h.satisfies_assertions()

print('Test 3 delete_top_k(3)')
h.delete_top_k(3)
print('\t A = ', h.A)
print('\t H = ', h.H)
h.satisfies_assertions()
assert h.A == [-11, -10, -9, -4, -2]
assert h.H.min_element() == 0
h.satisfies_assertions()

print('Test 4 delete_top_k(4)')
h.delete_top_k(4)
print('\t A = ', h.A)
print('\t H = ', h.H)
assert h.A == [-11, -10, -9, -4, 0]
h.satisfies_assertions()

print('Test 5 delete_top_k(0)')
h.delete_top_k(0)
print('\t A = ', h.A)
print('\t H = ', h.H)
assert h.A == [-10, -9, -4, 0, 1]
h.satisfies_assertions()

print('Test 6 delete_top_k(1)')
h.delete_top_k(1)
print('\t A = ', h.A)
print('\t H = ', h.H)
assert h.A == [-10, -4, 0, 1, 4]
h.satisfies_assertions()
print('Pasamos todas las pruebas')