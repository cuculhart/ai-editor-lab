def even_numbers(numbers):
    """偶数だけを昇順に並べて返す関数"""
    even = [n for n in numbers if n % 2 == 0]
    return even
