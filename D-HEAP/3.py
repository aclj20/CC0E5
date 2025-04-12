from typing import Any, List, Optional, Tuple


class DWayHeap(object):
    def __init__(self, elements: List[Any] = [], priorities: List[Any] = [], branching_factor: int = 2) -> None:
       
        if len(elements) != len(priorities):
            raise ValueError(f'La longitud de la lista de elementos ({len(elements)})'
                             f' debe coincidir con la longitud de la lista de prioridades ({len(priorities)}).')
        if branching_factor < 2:
            raise ValueError(f'El factor de ramificación ({branching_factor}) debe ser mayor que 1.')
        self._pairs: List[Tuple[Any, Any]] = []
        self.D = branching_factor

        if len(elements) > 0:
            self._heapify(elements, priorities)

    def __sizeof__(self) -> int:
        
        return len(self)

    def __len__(self) -> int:
        
        return len(self._pairs)

    def compare(self, prioridad: Any, otraPrioridad: Any)->bool:
        if prioridad>otraPrioridad:
            return True
        else:
            return False
        
    def _push_down(self, index: int) -> None:
    
        assert (0 <= index < len(self._pairs))
        input_pair = self._pairs[index]
        input_priority = input_pair[0]
        current_index = index
        first_leaf = self.first_leaf_index()
        while current_index < first_leaf:
            child_index = self._highest_priority_child_index(current_index)
            assert (child_index is not None)
            if self.compare(self._pairs[child_index][0], input_priority):
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

            if self.compare(input_priority, parent[0]):
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
 