from typing import Any, List, Optional, Tuple


class DWayHeap(object):
    def __init__(self, elements: List[Any] = [], priorities: List[float] = [], branching_factor: int = 2) -> None:
       
        if len(elements) != len(priorities):
            raise ValueError(f'La longitud de la lista de elementos ({len(elements)})'
                             f' debe coincidir con la longitud de la lista de prioridades ({len(priorities)}).')
        if branching_factor < 2:
            raise ValueError(f'El factor de ramificación ({branching_factor}) debe ser mayor que 1.')
        self._pairs: List[Tuple[float, Any]] = []
        self.D = branching_factor

        if len(elements) > 0:
            self._heapify(elements, priorities)

    def __sizeof__(self) -> int:
        
        return len(self)

    def __len__(self) -> int:
        
        return len(self._pairs)

    def _validate(self) -> bool:
        """Verifica que se cumplan las tres invariantes del heap:
        1. Cada nodo tiene como máximo `D` hijos. (Garantizado por la construcción)
        2. El árbol del heap es completo y alineado a la izquierda. (También garantizado por la construcción)
        3. Cada nodo contiene la mayor prioridad en el subárbol con raíz en ese nodo.

        Returns: True si se cumplen todas las invariantes del heap.
        """
        current_index = 0
        first_leaf = self.first_leaf_index()
        while current_index < first_leaf:
            current_priority: float = self._pairs[current_index][0]
            first_child = self._first_child_index(current_index)
            last_child_guard = min(first_child + self.D, len(self))
            for child_index in range(first_child, last_child_guard):
                if current_priority < self._pairs[child_index][0]:
                    return False
            current_index += 1
        return True

    def _push_down(self, index: int) -> None:
    
        assert (0 <= index < len(self._pairs))
        input_pair = self._pairs[index]
        input_priority = input_pair[0]
        current_index = index
        first_leaf = self.first_leaf_index()
        while current_index < first_leaf:
            child_index = self._highest_priority_child_index(current_index)
            assert (child_index is not None)
            if self._pairs[child_index][0] > input_priority:
                self._pairs[current_index] = self._pairs[child_index]
                current_index = child_index
            else:
                break

        self._pairs[current_index] = input_pair

    def _bubble_up(self, index: int) -> None:
        
        assert (0 <= index < len(self._pairs))
        input_pair = self._pairs[index]
        input_priority = input_pair[0]
        while index > 0:
            parent_index = self._parent_index(index)
            parent = self._pairs[parent_index]

            if input_priority > parent[0]:
                self._pairs[index] = parent
                index = parent_index
            else:
                break

        self._pairs[index] = input_pair

    def _first_child_index(self, index) -> int:
        
        return index * self.D + 1

    def _parent_index(self, index) -> int:
        
        return (index - 1) // self.D

    def _highest_priority_child_index(self, index) -> Optional[int]:
       
        first_index = self._first_child_index(index)
        size = len(self)
        last_index = min(first_index + self.D, size)

        if first_index >= size:
            return None

        highest_priority = -float('inf')
        index = first_index
        for i in range(first_index, last_index):
            if self._pairs[i][0] > highest_priority:
                highest_priority = self._pairs[i][0]
                index = i

        return index

    def first_leaf_index(self):
        return (len(self) - 2) // self.D + 1

    def _heapify(self, elements: List[Any], priorities: List[float]) -> None:
        assert (len(elements) == len(priorities))
        self._pairs = list(zip(priorities, elements))
        last_inner_node_index = self.first_leaf_index() - 1
        for index in range(last_inner_node_index, -1, -1):
            self._push_down(index)

    def is_empty(self) -> bool:
        return len(self) == 0

    def top(self) -> Any:

        if self.is_empty():
            raise RuntimeError('Se llamó al método top en un heap vacío.')
        if len(self) == 1:
            element = self._pairs.pop()[1]
        else:
            element = self._pairs[0][1]
            self._pairs[0] = self._pairs.pop()
            self._push_down(0)

        return element

    def peek(self) -> Any:
        if self.is_empty():
            raise RuntimeError('Se llamó al método peek en un heap vacío.')
        return self._pairs[0][1]

    def insert(self, element: Any, priority: float) -> None:
        self._pairs.append((priority, element))
        self._bubble_up(len(self._pairs) - 1)
    
    def decrease_key(self, index, newPriority):
        self._pairs[index][0] = newPriority
        self._push_down(index)
    
    def increase_key(self, index, newPriority):
        self._pairs[index][0] = newPriority
        self._bubble_up(index)
    
    def change_key(self, index, newPriority):
        if (newPriority > self._pairs[index][0]):
            self.increase_key(index, newPriority)
        else:
            self.decrease_key(index, newPriority)