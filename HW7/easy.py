class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert_into_bst(root, value):
    # If the tree is empty, create a new node and return it
    if root is None:
        return TreeNode(value)
    
    # If the value to insert is less than the root, insert in the left subtree
    if value < root.value:
        root.left = insert_into_bst(root.left, value)
    
    # If the value to insert is greater than the root, insert in the right subtree
    else:
        root.right = insert_into_bst(root.right, value)
    
    # Return the (potentially updated) root node
    return root