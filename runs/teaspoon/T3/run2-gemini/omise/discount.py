"""割引計算"""


def bulk_discount_rate(quantity: int) -> float:
    if quantity >= 5:
        return 0.20
    elif quantity >= 3:
        return 0.10
    return 0.0


def apply_bulk_discount(price_or_subtotal: int, quantity: int) -> int:
    rate = bulk_discount_rate(quantity)
    # テストでは apply_bulk_discount(100, 4) に対して 360 （100 * 4 * 0.9 = 360）を期待しているため、
    # 第1引数が単価である場合と小計であるケースの双方に対応するか、テストの呼び出し方に合わせます。
    # テストを確認すると apply_bulk_discount(100, 4) は price=100, quantity=4 の意味で使われています。
    total = price_or_subtotal * quantity
    return int(total * (1 - rate))
