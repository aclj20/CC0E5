class BSTNode:
    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.size = 1  # El tamaño del subárbol inicial es 1 (el nodo mismo)

    # Función de búsqueda
    def search(self, key):
        if self.key == key:
            return True, self
        elif key < self.key:
            if self.left:
                return self.left.search(key)
            else:
                return False, self  # Aquí se insertaría si no se encuentra
        else:  # key >= self.key, acepta duplicados en el subárbol derecho
            if self.right:
                return self.right.search(key)
            else:
                return False, self  # Aquí se insertaría si no se encuentra

    # Función de inserción (permite duplicados)
    def insert(self, key):
        found, node = self.search(key)

        if found:
            return None  # Si ya existe la clave, no insertamos nada

        new_node = BSTNode(key, parent=node)

        if key < node.key:
            node.left = new_node
        else:
            node.right = new_node

        # Actualizamos el tamaño de los nodos ancestros
        current = new_node.parent
        while current:
            current.size += 1
            current = current.parent

        return new_node

    # Función de altura
    def height(self):
        left_h = self.left.height() if self.left else 0
        right_h = self.right.height() if self.right else 0
        return 1 + max(left_h, right_h)

    # Función para obtener el tamaño del subárbol
    def get_size(self):
        return self.size

    # Función para encontrar el k-ésimo elemento más pequeño
    def find_kth_smallest(self, k):
        left_size = self.left.size if self.left else 0

        if k == left_size + 1:
            return self  # El k-ésimo elemento es el nodo actual
        elif k <= left_size:
            return self.left.find_kth_smallest(k)  # Buscar en el subárbol izquierdo
        else:
            return self.right.find_kth_smallest(k - left_size - 1)  # Buscar en el subárbol derecho

    # Función para eliminar un nodo
    def delete(self, key):
        found, node_to_delete = self.search(key)
        if not found:
            return None  # No se encuentra el nodo a eliminar

        # Caso 1: Nodo sin hijos (hoja)
        if not node_to_delete.left and not node_to_delete.right:
            if node_to_delete.parent:
                if node_to_delete.parent.left == node_to_delete:
                    node_to_delete.parent.left = None
                else:
                    node_to_delete.parent.right = None
            self.update_size_upward(node_to_delete.parent)

        # Caso 2: Nodo con un hijo (izquierdo o derecho)
        elif node_to_delete.left and not node_to_delete.right:
            if node_to_delete.parent:
                if node_to_delete.parent.left == node_to_delete:
                    node_to_delete.parent.left = node_to_delete.left
                else:
                    node_to_delete.parent.right = node_to_delete.left
            node_to_delete.left.parent = node_to_delete.parent
            self.update_size_upward(node_to_delete.parent)

        elif not node_to_delete.left and node_to_delete.right:
            if node_to_delete.parent:
                if node_to_delete.parent.left == node_to_delete:
                    node_to_delete.parent.left = node_to_delete.right
                else:
                    node_to_delete.parent.right = node_to_delete.right
            node_to_delete.right.parent = node_to_delete.parent
            self.update_size_upward(node_to_delete.parent)

        # Caso 3: Nodo con dos hijos
        else:
            successor = node_to_delete.right.get_leftmost_descendant()
            node_to_delete.key = successor.key
            node_to_delete.right.delete(successor.key)

        return node_to_delete

    # Función para actualizar los tamaños hacia arriba
    def update_size_upward(self, node):
        while node:
            node.size -= 1
            node = node.parent

    # Función para encontrar el sucesor (más pequeño en el subárbol derecho)
    def get_leftmost_descendant(self):
        if self.left:
            return self.left.get_leftmost_descendant()
        return self


# Ejemplo de uso

# Crear el árbol
root = BSTNode(25)
root.insert(12)
root.insert(18)
root.insert(40)
root.insert(30)
root.insert(50)

# Buscar el 3er elemento más pequeño
k = 3
kth_node = root.find_kth_smallest(k)
print(f"El {k}-ésimo elemento más pequeño es {kth_node.key}")

# Mostrar el árbol después de la eliminación
print(f"Tamaño del subárbol de 25 después de eliminación: {root.size}")
