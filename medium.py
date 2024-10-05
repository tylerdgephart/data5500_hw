# Prompt/Question entered into ChatGPT:
# "Given an array of integers, write a function that finds the second largest number in the array."

def second_largest(arr):
    if len(arr) < 2:
        return None  # Return None if there are fewer than 2 elements
    
    # Initialize two variables to hold the largest and second largest numbers
    largest = second_largest = float('-inf')
    
    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
            
    return second_largest

# Example usage
arr = [10, 20, 4, 45, 99, 99]
print(second_largest(arr))