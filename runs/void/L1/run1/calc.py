def even_numbers(numbers):
    """
    Filters even numbers from a list of integers and returns them sorted in ascending order.
    
    Args:
        numbers: A list of integers
        
    Returns:
        A list of even integers, sorted in ascending order
        
    Examples:
        >>> even_numbers([3, 1, 4, 2])
        [2, 4]
        >>> even_numbers([])
        []
    """
    return sorted([n for n in numbers if n % 2 == 0])

# Test examples
if __name__ == "__main__":
    print(even_numbers([3, 1, 4, 2]))  # Output: [2, 4]
    print(even_numbers([]))              # Output: []
    print(even_numbers([1, 2, 3, 4, 5, 6]))  # Output: [2, 4, 6]
