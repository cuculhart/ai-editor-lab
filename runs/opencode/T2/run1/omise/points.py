"""ポイント"""

POINT_RATE = 0.01


def earn_points(amount: int) -> int:
    """税抜き購入金額に対する獲得ポイント（小数点以下切り捨て）。"""
    return int(amount * POINT_RATE)
