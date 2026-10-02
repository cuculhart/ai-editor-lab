import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartAdditional(unittest.TestCase):
    def test_remove_product(self):
        """remove メソッドが商品を正しく削除することを確認する"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        
        cart.add(apple, 2)
        cart.add(banana, 1)
        
        # りんごを1つ削除
        cart.remove(apple)
        
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(banana), 1)
        self.assertEqual(cart.count(), 2)
        self.assertEqual(cart.subtotal(), 180)

    def test_quantities(self):
        """quantities メソッドが商品ごとの数量マップを正しく返すことを確認する"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        
        cart.add(apple, 3)
        cart.add(banana, 2)
        
        expected = {
            "りんご": 3,
            "バナナ": 2,
        }
        self.assertEqual(cart.quantities(), expected)

    def test_mixed_products_and_operations(self):
        """複数種類の商品が混在するケースで、追加・削除・数量・小計が正しく連携することを確認する"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        orange = Product("みかん", 60)
        
        cart.add(apple, 2)
        cart.add(banana, 3)
        cart.add(orange, 1)
        
        # 混在時の初期状態確認
        self.assertEqual(cart.count(), 6)
        self.assertEqual(cart.subtotal(), (100 * 2) + (80 * 3) + (60 * 1)) # 200 + 240 + 60 = 500
        self.assertEqual(cart.quantities(), {"りんご": 2, "バナナ": 3, "みかん": 1})
        
        # バナナを1つ削除
        cart.remove(banana)
        
        self.assertEqual(cart.count(banana), 2)
        self.assertEqual(cart.quantities(), {"りんご": 2, "バナナ": 2, "みかん": 1})
        self.assertEqual(cart.subtotal(), 420)


if __name__ == "__main__":
    unittest.main()
