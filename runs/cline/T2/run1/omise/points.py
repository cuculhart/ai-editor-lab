\"\"\"ポイント機能\"\"\"


def earn_points(amount: int) -> int:
    \"\"\"税抜購入金額（円）の1%をポイントとして付与し、小数点以下は切り捨てます。
    
    例:
        earn_points(1000) -> 10
        earn_points(150) -> 1
    \"\"\"
    return int(amount * 0.01)