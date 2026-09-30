import unittest
from omise.models import Product
from omise.cart import Cart


class TestCartAdditional(unittest.TestCase):
    def test_remove(self):
        """商品を削除できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 2)
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 1)

    def test_quantities(self):
        """商品ごとの数量が正しく集計されること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        cart.add(apple, 2)
        cart.add(banana, 3)
        self.assertEqual(cart.quantities(), {"りんご": 2, "バナナ": 3})

    def test_multiple_products_subtotal(self):
        """複数種類の商品が混在する場合に小計が正しく計算されること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        cart.add(apple, 2)
        cart.add(banana, 1)
        self.assertEqual(cart.subtotal(), 280)
