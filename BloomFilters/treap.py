import threading
from typing import Optional, TypeVar, Generic, Tuple

T = TypeVar('T')
S = TypeVar('S')

class Treap(Generic[T, S]):
    """
    Implementación de un Treap, una estructura de datos híbrida de
    Árbol binario de búsqueda (BST) y heap (min-heap en prioridad).

    Uso thread-safe con RLock.
    """

    class _TreapNode:
        def __init__(self, key: T, priority: S):
            self.key: T = key
            self.priority: S = priority
            self.left: Optional['Treap._TreapNode'] = None
            self.right: Optional['Treap._TreapNode'] = None
            self.parent: Optional['Treap._TreapNode'] = None

        def is_leaf(self) -> bool:
            return self.left is None and self.right is None

        def is_root(self) -> bool:
            return self.parent is None

        def is_left_child(self) -> bool:
            return (self.parent is not None) and (self.parent.left is self)

        def is_right_child(self) -> bool:
            return (self.parent is not None) and (self.parent.right is self)

        # Búsqueda
        def search(self,
                   target_key: Optional[T] = None,
                   target_priority: Optional[S] = None
                   ) -> Optional['Treap._TreapNode']:
            """
            Busca recursivamente un nodo con clave == target_key (si no es None)
            y prioridad == target_priority (si no es None).
            """
            if ((target_key is None or target_key == self.key) and
                (target_priority is None or target_priority == self.priority)):
                return self

            result = None
            if target_key is None or target_key <= self.key:
                if self.left is not None:
                    result = self.left.search(target_key, target_priority)
            if result is None and (target_key is None or target_key > self.key):
                if self.right is not None:
                    result = self.right.search(target_key, target_priority)
            return result

        # Medidas
        def size(self) -> int:
            return 1 + (self.left.size() if self.left else 0) + (self.right.size() if self.right else 0)

        def height(self) -> int:
            return 1 + max((self.left.height() if self.left else 0),
                           (self.right.height() if self.right else 0))

        def min(self) -> T:
            return self.left.min() if self.left else self.key

        def max(self) -> T:
            return self.right.max() if self.right else self.key

        # Inserción (clásica)
        def add(self, key: T, priority: S, treap: 'Treap') -> 'Treap._TreapNode':
            """
            Inserta un nuevo nodo (key, priority) respetando la propiedad BST en 'key'.
            Se asume que claves iguales se insertan en el subárbol izquierdo.
            Luego se verifica (y, en su caso, se corrige) la propiedad de heap.
            """
            if key <= self.key:
                if self.left is not None:
                    self.left = self.left.add(key, priority, treap)
                    self.left.parent = self
                else:
                    self.left = Treap._TreapNode(key, priority)
                    self.left.parent = self
                if treap.has_higher_priority(self.left.priority, self.priority):
                    return self.rotate_right(treap)
                else:
                    return self
            else:
                if self.right is not None:
                    self.right = self.right.add(key, priority, treap)
                    self.right.parent = self
                else:
                    self.right = Treap._TreapNode(key, priority)
                    self.right.parent = self
                if treap.has_higher_priority(self.right.priority, self.priority):
                    return self.rotate_left(treap)
                else:
                    return self

        # Rotaciones clásicas
        def rotate_left(self, treap: 'Treap') -> 'Treap._TreapNode':
            r"""
            Realiza una rotación a la izquierda.
            Sea x = self y y = x.right. Tras la rotación, y se convierte en la nueva raíz
            de este subárbol, y x pasa a ser su hijo izquierdo.
            """
            y = self.right
            if y is None:
                return self  # no se puede rotar
            self.right = y.left
            if y.left is not None:
                y.left.parent = self
            y.left = self
            y.parent = self.parent
            if self.parent is None:
                treap.root = y
            else:
                if self.is_left_child():
                    self.parent.left = y
                else:
                    self.parent.right = y
            self.parent = y
            return y

        def rotate_right(self, treap: 'Treap') -> 'Treap._TreapNode':
            """
            Realiza una rotación a la derecha.
            Sea x = self y y = x.left. Tras la rotación, y se convierte en la nueva raíz
            de este subárbol, y x pasa a ser su hijo derecho.
            """
            x = self.left
            if x is None:
                return self
            self.left = x.right
            if x.right is not None:
                x.right.parent = self
            x.right = self
            x.parent = self.parent
            if self.parent is None:
                treap.root = x
            else:
                if self.is_left_child():
                    self.parent.left = x
                else:
                    self.parent.right = x
            self.parent = x
            return x

        # Actualización de prioridad con algoritmo iterativo sencillo
        def update_priority(self, new_priority: S, treap: 'Treap') -> 'Treap._TreapNode':
            """
            Actualiza la prioridad del nodo y lo reubica en el árbol.
            Se realiza en dos fases:
              - Bubble-up: se rota mientras la nueva prioridad sea estrictamente menor que la del padre.
              - Push-down: se rota mientras algún hijo tenga prioridad estrictamente menor.
            Se utilizan comparaciones estrictas para evitar oscilaciones.
            """
            self.priority = new_priority
            # Bubble-up: mientras el nodo tenga padre y su prioridad sea menor que la del padre
            while self.parent is not None and self.priority < self.parent.priority:
                if self.is_left_child():
                    self = self.parent.rotate_right(treap)
                else:
                    self = self.parent.rotate_left(treap)
            # Push-down: mientras alguno de sus hijos tenga prioridad menor
            while True:
                changed = False
                if self.left is not None and self.left.priority < self.priority:
                    self = self.rotate_right(treap)
                    changed = True
                elif self.right is not None and self.right.priority < self.priority:
                    self = self.rotate_left(treap)
                    changed = True
                if not changed:
                    break
            return self

        # Eliminación recursiva interna
        def _remove(self, key: T, priority: S, treap: 'Treap') -> Tuple[Optional['Treap._TreapNode'], bool]:
            """
            Elimina recursivamente el nodo que coincida con (key, priority)
            y retorna (nuevo_subárbol, True/False si se eliminó).
            """
            if key < self.key:
                if self.left:
                    new_left, deleted = self.left._remove(key, priority, treap)
                    self.left = new_left
                    if new_left:
                        new_left.parent = self
                    return (self, deleted)
                else:
                    return (self, False)
            elif key > self.key:
                if self.right:
                    new_right, deleted = self.right._remove(key, priority, treap)
                    self.right = new_right
                    if new_right:
                        new_right.parent = self
                    return (self, deleted)
                else:
                    return (self, False)
            else:
                # Clave igual; si la prioridad no coincide, se busca en los hijos.
                if self.priority != priority:
                    if self.left:
                        new_left, deleted = self.left._remove(key, priority, treap)
                        self.left = new_left
                        if new_left:
                            new_left.parent = self
                        if deleted:
                            return (self, True)
                    if self.right:
                        new_right, deleted = self.right._remove(key, priority, treap)
                        self.right = new_right
                        if new_right:
                            new_right.parent = self
                        return (self, deleted)
                    return (self, False)
                # Nodo encontrado.
                if self.left is None:
                    if self.right:
                        self.right.parent = self.parent
                    return (self.right, True)
                elif self.right is None:
                    if self.left:
                        self.left.parent = self.parent
                    return (self.left, True)
                else:
                    # Ambos hijos existen: se rota según la prioridad del hijo más "bueno"
                    if treap.has_higher_priority(self.left.priority, self.right.priority):
                        new_root = self.rotate_right(treap)
                        new_root.right, _ = new_root.right._remove(key, priority, treap)
                        if new_root.right:
                            new_root.right.parent = new_root
                        return (new_root, True)
                    else:
                        new_root = self.rotate_left(treap)
                        new_root.left, _ = new_root.left._remove(key, priority, treap)
                        if new_root.left:
                            new_root.left.parent = new_root
                        return (new_root, True)

        def clean_up(self):
            if self.left:
                self.left.clean_up()
                self.left = None
            if self.right:
                self.right.clean_up()
                self.right = None
            self.parent = None

        def check_treap_invariants(self, treap: 'Treap') -> bool:
            if self.left is not None:
                if (treap.has_higher_priority(self.left.priority, self.priority)
                    or self.left.key > self.key):
                    return False
            if self.right is not None:
                if (treap.has_higher_priority(self.right.priority, self.priority)
                    or self.right.key <= self.key):
                    return False
            left_ok = self.left.check_treap_invariants(treap) if self.left else True
            right_ok = self.right.check_treap_invariants(treap) if self.right else True
            return left_ok and right_ok

    class TreapEntry:
        """
        Par (clave, prioridad) usado en operaciones públicas del Treap.
        """
        def __init__(self, key: T, priority: S):
            self.key = key
            self.priority = priority

        def get_key(self) -> T:
            return self.key

        def get_priority(self) -> S:
            return self.priority

        def __lt__(self, other: 'Treap.TreapEntry') -> bool:
            if other is None:
                return False
            return self.priority < other.priority

    def __init__(self):
        self.root: Optional[Treap._TreapNode] = None
        self._lock = threading.RLock()

    def has_higher_priority(self, first: S, second: S) -> bool:
        # Menor valor => mayor prioridad
        return first < second

    # Métodos públicos
    def size(self) -> int:
        with self._lock:
            return self.root.size() if self.root else 0

    def height(self) -> int:
        with self._lock:
            return self.root.height() if self.root else 0

    def is_empty(self) -> bool:
        with self._lock:
            return self.root is None

    def min(self) -> Optional[T]:
        with self._lock:
            return self.root.min() if self.root else None

    def max(self) -> Optional[T]:
        with self._lock:
            return self.root.max() if self.root else None

    def search(self, key: T) -> Optional[T]:
        with self._lock:
            node = self.root.search(target_key=key) if self.root else None
            return node.key if node else None

    def contains(self, entry: 'Treap.TreapEntry') -> bool:
        with self._lock:
            if not self.root:
                return False
            node = self.root.search(target_key=entry.get_key(),
                                    target_priority=entry.get_priority())
            return node is not None

    def add(self, entry: 'Treap.TreapEntry') -> bool:
        """
        Inserta la entrada siempre retornando True (como en los tests),
        incluso si ya existía.
        """
        with self._lock:
            if self.root is None:
                self.root = Treap._TreapNode(entry.get_key(), entry.get_priority())
            else:
                self.root = self.root.add(entry.get_key(), entry.get_priority(), self)
            return True

    def update_priority(self, old_entry: 'Treap.TreapEntry', new_entry: 'Treap.TreapEntry') -> bool:
        if old_entry.get_key() != new_entry.get_key():
            raise ValueError("Las dos entradas deben tener la misma clave")
        if old_entry.get_priority() == new_entry.get_priority():
            return False
        with self._lock:
            if not self.root:
                return False
            target = self.root.search(target_key=old_entry.get_key(),
                                      target_priority=old_entry.get_priority())
            if not target:
                return False
            new_node = target.update_priority(new_entry.get_priority(), self)
            if new_node.parent is None:
                self.root = new_node
            return True

    def remove(self, entry: 'Treap.TreapEntry') -> bool:
        """
        Elimina el nodo que coincida con (key, priority).
        Retorna True si se eliminó.
        """
        with self._lock:
            if self.root is None:
                return False
            new_root, deleted = self.root._remove(entry.get_key(), entry.get_priority(), self)
            self.root = new_root
            return deleted

    def remove_key(self, key: T) -> bool:
        """
        Elimina UNA copia de la clave 'key'. Se llama repetidamente
        para remover duplicados.
        """
        with self._lock:
            if self.root is None:
                return False
            node = self.root.search(target_key=key)
            if not node:
                return False
            self.root, deleted = self.root._remove(key, node.priority, self)
            return deleted

    def clear(self):
        with self._lock:
            old_root = self.root
            self.root = None
        if old_root:
            old_root.clean_up()

    def check_treap_invariants(self) -> bool:
        with self._lock:
            return self.root.check_treap_invariants(self) if self.root else True

    def check_bst_invariants(self) -> bool:
        with self._lock:
            return self.root.check_treap_invariants(self) if self.root else True

    def peek(self) -> Optional['Treap.TreapEntry']:
        """
        Retorna la raíz (elemento de mayor prioridad) sin eliminarla.
        """
        with self._lock:
            if not self.root:
                return None
            return Treap.TreapEntry(self.root.key, self.root.priority)

    def top(self) -> Optional['Treap.TreapEntry']:
        """
        Extrae y elimina la raíz (elemento de mayor prioridad) y la retorna.
        Se utiliza remove() para eliminar la entrada.
        """
        with self._lock:
            if not self.root:
                return None
            result = Treap.TreapEntry(self.root.key, self.root.priority)
            self.remove(result)
            return result