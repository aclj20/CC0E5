import random
class Node:
    # Implementa un nodo del árbol de búsqueda binaria.
    # Constructor para un nodo con una clave y un padre dado.
    # El padre puede ser None para un nodo raíz.
    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None  # Establece que el hijo izquierdo es None
        self.right = None # Establece que el hijo derecho es None
        # Asegurate de que el puntero izquierdo/derecho del padre
        # apunte al nodo recién creado.
        if parent is not None:
            if key < parent.key:
                assert(parent.left is None), 'El padre ya tiene un hijo izquierdo -- no se puede crear el nodo'
                parent.left = self
            else:
                assert key > parent.key, 'La clave es igual a la clave del padre. No se permiten claves duplicadas en un BST ya que rompe algunos algoritmos.'
                assert(parent.right is None), 'El padre ya tiene un hijo derecho -- no se puede crear el nodo'
                parent.right = self

    # Función de utilidad que recorre hacia la izquierda hasta encontrar el descendiente más a la izquierda
    def get_leftmost_descendant(self):
        if self.left is not None:
            return self.left.get_leftmost_descendant()
        else:
            return self
    
    # Completa el algoritmo de búsqueda a continuación
    # Puedes llamar a search recursivamente en el hijo izquierdo o derecho según corresponda.
    # Si la búsqueda tiene éxito: devuelve una tupla (True, nodo) donde nodo es el nodo del árbol con la clave buscada.
    # Ten en cuenta que si la búsqueda falla en encontrar la clave, debe devolver una tupla (False, nodo),
    # donde nodo sería el padre si se fuera a insertar la clave posteriormente.
    def search(self, key):

        if self.key == key:
            return (True, self)
        elif key < self.key:
            if self.left is not None:
                return self.left.search(key)
            else:
                return (False, self)  # No hay hijo izquierdo: se insertaría aquí
        else:  # key > self.key
            if self.right is not None:
                return self.right.search(key)
            else:
                return (False, self)  # No hay hijo derecho: se insertaría aquí

        # Código a completar
      
    # Completa el algoritmo de inserción a continuación
    # Primero, busca la posición donde se insertará la clave, encontrando
    # el nodo padre correspondiente para la nueva clave.
    # Crea un nuevo nodo con esa clave e insertarlo.
    # Retorna None si la clave ya existe en el árbol.
    # Retorna el nuevo nodo correspondiente a la clave insertada en caso contrario.
    def insert(self, key):
        found, node = self.search(key)

        if found:
            return None  # La clave ya existe

        new_node = Node(key)  # Crear un nuevo nodo con la clave
        new_node.parent = node
        if key < node.key:
            node.left = new_node
        else:
            node.right = new_node

        return new_node
        
    # Completa el algoritmo para calcular la altura del árbol
    # La altura de un nodo cuyos hijos son ambos None se define como 1.
    # La altura de cualquier otro nodo es 1 + el máximo de la altura de sus hijos.
    # Retorna un número que represente la altura.
    def height(self):
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)
            
        
    # Escribe un algoritmo para eliminar una clave en el árbol.
    # Primero, encuentra el nodo en el árbol con la clave.
    # Se recomienda dibujar diagramas para visualizar los siguientes casos antes de programar.
    # Caso 1: ambos hijos del nodo son None
    #   -- En este caso, la eliminación es sencilla: simplemente determinar si el nodo con la clave
    #      es el hijo izquierdo o derecho del padre y establecer ese puntero en None en el nodo padre.
    # Caso 2: uno de los hijos es None y el otro no lo es.
    #   -- Reemplaza el nodo por su único hijo. Es decir,
    #      modifica el padre del hijo para que sea el padre del nodo que se elimina.
    #      además, ajusta el puntero izquierdo/derecho del padre según corresponda.
    # Caso 3: ambos hijos del nodo existen.
    #    -- Primero, encuentra su sucesor (ir un paso a la derecha y luego todo lo posible a la izquierda).
    #    -- La función get_leftmost_descendant puede ser útil aquí.
    #    -- Reemplaza la clave del nodo por la de su sucesor.
    #    -- Elimina el nodo sucesor.
    # Retorno: no se especifica un valor de retorno
    def delete(self, key):
        (found, node_to_delete) = self.search(key)
        assert(found == True), f"La clave a eliminar: {key} no existe en el árbol"
        # Código a completar

        parent = node_to_delete.parent

        if not node_to_delete.left and not node_to_delete.right:
            if parent:
                if parent.left == node_to_delete:
                    parent.left = None
                else:
                    parent.right = None
        
        elif node_to_delete.left and not node_to_delete.right:
            if parent:
                if parent.left == node_to_delete:
                    parent.left = node_to_delete.left
                else:
                    parent.right = node_to_delete.left
            node_to_delete.left.parent = parent

        elif not node_to_delete.left and node_to_delete.right:
            if parent:
                if parent.left == node_to_delete:
                    parent.left = node_to_delete.right
                else:
                    parent.right = node_to_delete.right
            node_to_delete.right.parent = parent
        
        else:
            successor = node_to_delete.right.get_leftmost_descendant()
            temp_key = successor.key
            self.delete(successor.key)  # Recursivamente elimina el sucesor
            node_to_delete.key = temp_key


t1 = Node(25, None)
t2 = Node(12, t1)
t3 = Node(18, t2)
t4 = Node(40, t1)

print('-- Probando la construcción básica de nodos (código proporcionado originalmente) --')
assert(t1.left == t2), 'prueba 1 falló'
assert(t2.parent == t1), 'prueba 2 falló'
assert(t2.right == t3), 'prueba 3 falló'
assert(t3.parent == t2), 'prueba 4 falló'
assert(t1.right == t4), 'prueba 5 falló'
assert(t4.left is None), 'prueba 6 falló'
assert(t4.right is None), 'prueba 7 falló'
# El árbol debería ser:
#             25
#            /  \
#         12     40
#           \
#           18

print('-- Probando búsqueda --')
(b, found_node) = t1.search(18)
assert(b and found_node.key == 18), 'prueba 8 falló'
(b, found_node) = t1.search(25)
assert(b and found_node.key == 25), 'prueba 9 falló -- debes encontrar el nodo con clave 25, que es la raíz'
(b, found_node) = t1.search(26)
assert((not b)), 'prueba 10 falló'
assert(found_node.key == 40), 'prueba 11 falló -- debes retornar el nodo hoja que sería el padre si se insertara la clave faltante'

print('-- Probando inserción --')
ins_node = t1.insert(26)
assert(ins_node.key == 26), 'prueba 12 falló'
assert(ins_node.parent == t4), 'prueba 13 falló'
assert(t4.left == ins_node), 'prueba 14 falló'

ins_node2 = t1.insert(33)
assert(ins_node2.key == 33), 'prueba 15 falló'
assert(ins_node2.parent == ins_node), 'prueba 16 falló'
assert(ins_node.right == ins_node2), 'prueba 17 falló'

print('-- Probando altura --')

assert(t1.height() == 4), 'prueba 18 falló'
assert(t4.height() == 3), 'prueba 19 falló'
assert(t2.height() == 2), 'prueba 20 falló'

print('¡Pasaron todas las pruebas!')

# Probando la eliminación
t1 = Node(16, None)
# Inserta los nodos de la lista
lst = [18, 25, 10, 14, 8, 22, 17, 12]
for elt in lst:
    t1.insert(elt)

# El árbol debería tener la siguiente forma:
#               16
#            /     \
#          10      18
#        /  \     /  \
#       8   14   17  25
#          /         /
#         12        22


# Probemos los tres casos de eliminación.
# Caso 1: eliminar el nodo 8
# El nodo 8 no tiene hijos (hoja).
t1.delete(8)  # después de eliminar, ambos hijos deben ser None.
(b8, n8) = t1.search(8)
assert(not b8), 'Prueba A: la eliminación no eliminó el nodo.'
(b, n) = t1.search(10)
assert(b), 'Prueba B falló: la búsqueda no funciona'
assert(n.left is None), 'Prueba C falló: el nodo 8 no fue eliminado correctamente.'

# Probemos eliminar el nodo 14, cuyo hijo derecho es None.
# n aún apunta al nodo 10 después de eliminar 8.
# Asegurémonos de que su hijo derecho sea 14.
assert(n.right is not None), 'Prueba D falló: el nodo 10 debería tener un hijo derecho, el nodo 14'
assert(n.right.key == 14), 'Prueba E falló: el nodo 10 debería tener el nodo 14 como hijo derecho'

# Eliminemos el nodo 14
t1.delete(14)
(b14, n14) = t1.search(14)
assert(not b14), 'Prueba F: La eliminación del nodo 14 falló, aún existe en el árbol.'
(b, n) = t1.search(10)
assert(n.right is not None), 'Prueba G falló: la eliminación del nodo 14 no se manejó correctamente'
assert(n.right.key == 12), f'Prueba H falló: la eliminación del nodo 14 no se manejó correctamente: {n.right.key}'

# Eliminemos el nodo 18 del árbol.
# Debe ser reemplazado por el nodo 22.

t1.delete(18)
(b18, n18) = t1.search(18)
assert(not b18), 'Prueba I: La eliminación del nodo 18 falló'
assert(t1.right.key == 22), 'Prueba J: Falló el reemplazo del nodo con su sucesor.'
assert(t1.right.right.left is None), 'Prueba K: Falló la eliminación correcta del nodo sucesor (hoja).' 

print('¡Todas las pruebas pasaron!')

def run_single_experiment(n):
    # 1. Crear una lista de números del 0 al n-1
    numbers = list(range(n))

    # 2. Mezclar aleatoriamente la lista
    random.shuffle(numbers)

    # 3. Crear el árbol e insertar los elementos de la lista mezclada
    root = Node(numbers[0])  # Inicializamos el árbol con el primer número
    for num in numbers[1:]:  # Insertamos el resto de números
        root.insert(num)

    # 4. Calcular y devolver la altura del árbol
    return root.height()

def run_multiple_trials(n, numTrials):
    lst_of_depths = [run_single_experiment(n) for j in range(numTrials)]
    return (sum(lst_of_depths) / len(lst_of_depths), lst_of_depths)