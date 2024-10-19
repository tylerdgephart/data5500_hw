def delete_node(root, value):
    if root is None:
        return root

    # If the value to be deleted is less than the root's value, search in the left subtree
    if value < root.value:
        root.left = delete_node(root.left, value)
    
    # If the value to be deleted is greater than the root's value, search in the right subtree
    elif value > root.value:
        root.right = delete_node(root.right, value)
    
    # If the value matches the root's value, this is the node to be deleted
    else:
        # Case 1: Node with only one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        
        # Case 2: Node with two children
        # Find the in-order successor (smallest value in the right subtree)
        successor = find_min(root.right)
        root.value = successor.value  # Replace root's value with the successor's value
        # Delete the successor node from the right subtree
        root.right = delete_node(root.right, successor.value)
    
    return root

def find_min(node):
    # Helper function to find the minimum value node in a BST
    current = node
    while current.left is not None:
        current = current.left
    return current