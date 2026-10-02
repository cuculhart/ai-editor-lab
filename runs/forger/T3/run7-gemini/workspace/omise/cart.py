from typing import Optional

from omise.models import Product


class Cart:
    """買い物かご。商品ごとの数量を辞書で保持する。"""

    def __init__(self) -> None:
        self._items: dict[Product, int] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        """商品をかごに追加する。quantity は 1 以上の整数。"""
        if quantity <= 0:
            raise ValueError(f"数量は1以上でなければなりません: {quantity}")
        self._items[product] = self._items.get(product, 0) + quantity

    def remove(self, product: Product, quantity: int = 1) -> None:
        """指定した商品をかごから減らす。かごにない商品を指定すると ValueError。"""
        if quantity <= 0:
            raise ValueError(f"数量は1以上でなければなりません: {quantity}")
        current = self._items.get(product, 0)
        if current < quantity:
            raise ValueError(
                f"かご内の数量({current})より多く減らすことはできません: {quantity}"
            )
        if current == quantity:
            del self._items[product]
        else:
            self._items[product] = current - quantity

    def count(self, product: Optional[Product] = None) -> int:
        """商品ごとの個数、またはかご全体の合計個数を返す。"""
        if product is None:
            return sum(self._items.values())
        return self._items.get(product, 0)

    def quantities(self) -> dict[Product, int]:
        """商品ごとの数量を辞書で返す。"""
        return dict(self._items)

    def subtotal(self) -> int:
        """かご内の商品の合計金額（税抜き）を計算する。"""
        return sum(product.price * qty for product, qty in self._items.items())
