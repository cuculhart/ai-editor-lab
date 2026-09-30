def even_numbers(numbers):
    """整数のリストを受け取り、偶数だけを昇順に並べて返す"""
    even_list = []
    for num in numbers:
        if num % 2 == 0:
            even_list.append(num)
    return even_list
