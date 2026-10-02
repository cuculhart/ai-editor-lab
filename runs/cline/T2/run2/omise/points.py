"""ポイント機能"""

import math


def earn_points(amount: int) -> int:
    """税抜き購入金額（円）の1%をポイントとして付与し、小数点以下は切り捨てる。"""
    return math.floor(amount * 0.01)
