"""会計"""

TAX_RATE = 0.10


def total_with_tax(amount: int) -> int:
    """税込金額（小数点以下切り捨て）。"""
    return int(amount * (1 + TAX_RATE))
