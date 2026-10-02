import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartAdditional(unittest.TestCase):
    def test_remove_item(self):
        """商品をカートから正しく削除できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 120)
        cart.add(apple, 2)
        cart.add(banana, 1)
        
        self.assertEqual(cart.count(), 3)
        cart.remove(apple)
        self.assertEqual(cart.count(), 2)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(banana), 1)

    def test_quantities_with_mixed_products(self):
        """複数種類の商品が混在するケースで、商品ごとの数量（quantities）が正しく取得できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 120)
        orange = Product("みかん", 80)
        
        cart.add(apple, 3)
        cart.add(banana, 1)
        cart.add(orange, 2)
        
        expected_quantities = {
            "りんご": 3,
            "バナナ": 1,
            "みかん": 2,
        }
        self.assertEqual(cart.quantities(), expected_quantities)
        self.assertEqual(cart.count(), 6)
        self.assertEqual(cart.subtotal(), (100 * 3) + (120 * 1) + (80 * 2))

    def test_remove_non_existent_item_raises_error(self):
        """存在しない商品を削除しようとした場合にエラー（ValueError）が発生すること"""
        cart = Cart()
        apple = Product("りんご", 100)
        with self.assertRaises(ValueError):
            cart.remove(apple)


if __name__ == "__main__":
    unittest.main()
