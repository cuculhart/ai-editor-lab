"""商品モデル"""
from dataclasses import dataclass


@dataclass
class Product:
    """商品。price は税抜き価格（円）。"""

    name: str
    price: int
