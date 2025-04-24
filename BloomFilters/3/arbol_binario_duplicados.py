class BSTNode:
    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None


    def search(self, key):
        if self.key == key:
            return True, self
        elif key < self.key:
            if self.left:
                return self.left.search(key)
            else:
                return False, self  
        else:  
            if self.right:
                return self.right.search(key)
            else:
                return False, self  

    
    def insert(self, key):
        found, node = self.search(key)

        if found:
            return None  

        new_node = BSTNode(key, parent=node)

        if key < node.key:
            node.left = new_node
        else:
            node.right = new_node

        return new_node

 
    def height(self):
        left_h = self.left.height() if self.left else 0
        right_h = self.right.height() if self.right else 0
        return 1 + max(left_h, right_h)

   
    def get_leftmost_descendant(self):
        if self.left is not None:
            return self.left.get_leftmost_descendant()
        else:
            return self
    
 
    def delete(self, key):
        found, node_to_delete = self.search(key)
        assert(found), f"El nodo con la clave {key} no se encuentra en el árbol"

        parent = node_to_delete.parent

        if not node_to_delete.left and not node_to_delete.right:
            if parent:
                if parent.left == node_to_delete:
                    parent.left = None
                elif parent.right == node_to_delete:
                    parent.right = None
        

        elif (node_to_delete.left and not node_to_delete.right) or (not node_to_delete.left and node_to_delete.right):
            child = node_to_delete.left if node_to_delete.left else node_to_delete.right
            if parent:
                if parent.left == node_to_delete:
                    parent.left = child
                elif parent.right == node_to_delete:
                    parent.right = child
            child.parent = parent


        else:
           
            successor = node_to_delete.right.get_leftmost_descendant()
            successor_key = successor.key
            
            node_to_delete.key = successor_key
          
            successor.delete(successor_key)
