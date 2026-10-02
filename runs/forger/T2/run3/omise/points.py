"""ポイント関連の機能"""
from typing import Union

Point = Union[int, float]


def earn_points(amount: Union[int, float]) -> int:
    """税抜き金額（円）の 1% をポイントとして付与（切り捨て）

    Args:
        amount: 税抜き購入金額（円）

    Returns:
        ポイント数（int）

    例:
        earn_points(1000) -> 10
        earn_points(150) -> 1

    >>> earn_points(1000)
    10
    >>> earn_points(150)
    1
    """
    # 整数に変換して計算する
    amount_int = int(amount)
    # 1% を切り捨てで計算
    return amount_int // 100
