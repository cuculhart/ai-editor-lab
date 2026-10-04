def even_numbers(numbers):
    """
    Returns a list of even numbers from the input list, sorted in ascending order.
    """
    evens = [n for n in numbers if n % 2 == 0]
    evens.sort()
    return evens

if __name__ == "__main__":
    # Basic test
    print(even_numbers([3, 1, 4, 2]))  # [2, 4]
    print(even_numbers([]))  # []
