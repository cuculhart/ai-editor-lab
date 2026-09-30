def even_numbers(numbers):
    """
    整数のリストを受け取り、偶数だけを昇順に並べて返す

    例:
    - even_numbers([3, 1, 4, 2]) は [2, 4] を返す
    - even_numbers([]) は [] を返す

    :param numbers: 整数のリスト
    :return: 偶数の昇順リスト
    """
    even_list = sorted([num for num in numbers if num % 2 == 0])
    return even_list


if __name__ == "__main__":
    # テスト例
    test_cases = [
        ([3, 1, 4, 2], [2, 4]),
        ([], []),
        ([1, 3, 5], []),
        ([2, 4, 6, 8], [2, 4, 6, 8]),
        ([], []),
    ]
    
    for input_list, expected in test_cases:
        result = even_numbers(input_list)
        print(f"even_numbers({input_list}) = {result}")
        assert result == expected, f"Expected {expected}, got {result}"
    
    print("\nすべてのテストが通りました!")