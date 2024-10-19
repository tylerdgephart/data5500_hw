def search_bst(root, value):
    # Base case: if root is None, value not found, return False
    if root is None:
        return False
    
    # If the value matches the root's value, return True
    if root.value == value:
        return True
    
    # If the value is less than the root's value, search the left subtree
    if value < root.value:
        return search_bst(root.left, value)
    
    # If the value is greater, search the right subtree
    return search_bst(root.right, value)