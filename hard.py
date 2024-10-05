# Prompt/Question entered into ChatGPT:
# "Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array."

def max_difference(arr):
    if len(arr) < 2:
        return 0  # Return 0 if there are fewer than 2 elements
    
    min_element = arr[0]
    max_diff = float('-inf')
    
    for num in arr[1:]:
        max_diff = max(max_diff, num - min_element)
        min_element = min(min_element, num)
    
    return max_diff

# Example usage
arr = [2, 3, 10, 6, 4, 8, 1]
print(max_difference(arr))