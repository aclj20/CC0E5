class Fibonacci_Heap():
    def __init__(self):
        self.n = 0
        self.min = None
        self.root_list = None
    def make_heap():
        pass
    def insert(self, key):
        node = Node(key)
        node.left = node
        node.right = node

        self.merge_with_root_list(node)

        if self.min is None or node.key < self.min.key:
            self.min = node 

        self.n += 1
        return node

    def minimum(self):
        return self.min
    def extract_min():
        pass
    def union():
        pass
    def decrease_key():
        pass
    def delete():
        pass

    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            # insert at end of root list
            node.right = self.root_list
            node.left = self.root_list.left
            self.root_list.left.right = node
            self.root_list.left = node
            
class Node():
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False

        self.parent = None
        self.child = None
        self.left = None
        self.right = None