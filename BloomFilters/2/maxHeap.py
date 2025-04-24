from minHeap import *
class MaxHeap:
    def __init__(self):
        self.H = [None]  # H[0] no se usa
        
    def size(self):
        return len(self.H) - 1
    
    def __repr__(self):
        return str(self.H[1:])
        
    def satisfies_assertions(self):
        for i in range(2, len(self.H)):
            # En max-heap, cada hijo debe ser menor o igual que su padre
            assert self.H[i] <= self.H[i // 2], f'La propiedad de max-heap falla en la posición {i // 2}, elemento padre: {self.H[i // 2]}, elemento hijo: {self.H[i]}'
    
    def max_element(self):
        return self.H[1]
    
    def bubble_up(self, index):
        # Completa el código: sube el elemento en el heap hasta restaurar la propiedad de max-heap
        assert index >= 1
        if index == 1:
            return
        # Completa el codigo
        elem = self.H[index]
        while(index > 1):
            parent_index = index // 2
            if elem > self.H[parent_index]:
                self.H[index] = self.H[parent_index]
                index = parent_index
            else:
                break
        self.H[index] = elem
            
    def bubble_down(self, index):
        # Completa el código: baja el elemento en el heap hasta restaurar la propiedad de max-heap
        assert index >= 1 and index < len(self.H)
        left = index*2
        right = index*2 + 1
        m = index
        if (left <= self.size() and self.H[left] > self.H[m]):
            m = left
        if (right <= self.size() and self.H[right] > self.H[m]):
            m = right
        if index != m:
            self.H[m], self.H[index] = self.H[index], self.H[m]
            # Bubble down en el hijo menor
            self.bubble_down(m)
        return 
        # COMPLETADO
               
    # Función: insert
    # Inserta un elemento en el max-heap usando bubble_up
    def insert(self, elt):
        self.H.append(elt)
        self.bubble_up(self.size())
        
    # Función: delete_max
    # Elimina el elemento máximo del heap usando bubble_down
    def delete_max(self):
        if self.size() == 0:
            return
        if self.size() == 1:
            self.H.pop()
            return
        self.H[1] = self.H.pop()
        self.bubble_down(1)

h = MaxHeap()
print('Insertando: 5, 2, 4, -1 y 7 en ese orden.')
h.insert(5)
print(f'\t Heap = {h}')
assert(h.max_element() == 5)
h.insert(2)
print(f'\t Heap = {h}')
assert(h.max_element() == 5)
h.insert(4)
print(f'\t Heap = {h}')
assert(h.max_element() == 5)
h.insert(-1)
print(f'\t Heap = {h}')
assert(h.max_element() == 5)
h.insert(7)
print(f'\t Heap = {h}')
assert(h.max_element() == 7)
h.satisfies_assertions()

print('Eliminando el maximo elemento')
h.delete_max()
print(f'\t Heap = {h}')
assert(h.max_element() == 5)
h.delete_max()
print(f'\t Heap = {h}')
assert(h.max_element() == 4)
h.delete_max()
print(f'\t Heap = {h}')
assert(h.max_element() == 2)
h.delete_max()
print(f'\t Heap = {h}')
assert(h.max_element() == -1)
h.delete_max()
print(f'\t Heap = {h}')
print('Pasaste todas las pruebas!')

class MedianMaintainingHeap():
    def __init__(self):
        self.H_max = MaxHeap()
        self.H_min = MinHeap()
        self.mediana = 0
        self.n = 0
    def __repr__(self):
        return (f"H_min = \t{self.H_min}\n"
                f"H_max = \t{self.H_max}")
    def insert(self, e):
        if self.H_min.size() == self.H_max.size():
            if self.H_min.size() == 0 or e >= self.H_max.max_element():
                self.H_min.insert(e)
            else:
                self.H_min.insert(self.H_max.max_element())
                self.H_max.delete_max()
                self.H_max.insert(e)
            self.mediana = self.H_min.min_element()
        else:
            if e<= self.H_min.min_element():
                self.H_max.insert(e)
            else:
                self.H_max.insert(self.H_min.min_element())
                self.H_min.delete_min()
                self.H_min.insert(e)
            self.mediana = (self.H_min.min_element() + self.H_max.max_element()) / 2
        self.n += 1

    def get_median(self):
        return self.mediana 
    
    def satisfies_assertions(self):
        if self.n > 1:
            assert self.H_max.max_element() <= self.H_min.min_element(), "No se cumple H_max.top <= H_min.top"
        assert self.H_max.size() == self.H_min.size() or self.H_max.size() + 1 == self.H_min.size() 

m = MedianMaintainingHeap()
print('Insertando 1, 5, 2, 4, 18, -4, 7, 9')

m.insert(1)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 1, f'se esperaba la mediana = 1, tu código devolvió {m.get_median()}'

m.insert(5)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 3, f'se esperaba la mediana = 3.0, tu código devolvió {m.get_median()}'

m.insert(2)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 2, f'se esperaba la mediana = 2, tu código devolvió {m.get_median()}'

m.insert(4)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 3, f'se esperaba la mediana = 3, tu código devolvió {m.get_median()}'

m.insert(18)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 4, f'se esperaba la mediana = 4, tu código devolvió {m.get_median()}'

m.insert(-4)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 3, f'se esperaba la mediana = 3, tu código devolvió {m.get_median()}'

m.insert(7)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 4, f'se esperaba la mediana = 4, tu código devolvió {m.get_median()}'

m.insert(9)
print(m)
print(m.get_median())
m.satisfies_assertions()
assert m.get_median() == 4.5, f'se esperaba la mediana = 4.5, tu código devolvió {m.get_median()}'

print('Todas las pruebas pasaron!')