"""割引ルール"""



def bulk_discount_rate(quantity: int) -> float:
    """同一商品を 3 個以上買うと 10%引き。"""
    if quantity >= 3:
        return 0.10
    return 0.0


def apply_bulk_discount(product_price: int, quantity: int) -> int:
    """まとめ買い割引後の金額（円、小数点以下切り捨て）。"""
    rate = bulk_discount_rate(quantity)
    return int(product_price * quantity * (1 - rate))
