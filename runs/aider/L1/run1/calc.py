def even_numbers(numbers):
    """
    整数のリストを受け取り、偶数だけを昇順に並べて返す
    
    Args:
        numbers: 整数のリスト
        
    Returns:
        偶数だけを昇順に並べたリスト
    """
    even_list = [num for num in numbers if num % 2 == 0]
    return even_list
