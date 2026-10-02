"""カート機能。"""

from omise.models import Product


class Cart:
    """ショッピングカート。商品を管理し小計を計算する。"""

    def __init__(self) -> None:
        self._items: dict[Product, int] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        """商品をカートに追加する。"""
        if quantity > 0:
            self._items[product] = self._items.get(product, 0) + quantity

    def remove(self, product: Product, quantity: int = 1) -> None:
        """商品をカートから指定数減らす。

        カート内の数量以上の数を指定した場合はカートから完全に削除する。
        """
        if product not in self._items or quantity <= 0:
            return

        current_qty = self._items[product]
        if quantity >= current_qty:
            del self._items[product]
        else:
            self._items[product] = current_qty - quantity

    def count(self) -> int:
        """カート内の商品の総数を返す。"""
        return sum(self._items.values())

    def quantities(self) -> dict[Product, int]:
        """商品ごとの数量を辞書で返す。"""
        return dict(self._items)

    def subtotal(self) -> int:
        """小計（割引前）を計算する。"""
        return sum(product.price * qty for product, qty in self._items.items())
