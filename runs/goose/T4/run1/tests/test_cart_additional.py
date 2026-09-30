import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartAdditional(unittest.TestCase):
    def test_remove_product(self):
        """商品をカートから削除（remove）できること、および複数個ある場合は1つだけ削除されることをテスト"""
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 2)
        self.assertEqual(cart.count(apple), 2)
        
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(), 1)
        
        # もう一度削除して空になること
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 0)
        self.assertEqual(cart.count(), 0)

    def test_quantities_summary(self):
        """quantitiesメソッドが商品ごとの数量の辞書を正しく返すことをテスト"""
        cart = Cart()
        apple = Product("りんご", 100)
        orange = Product("みかん", 80)
        
        cart.add(apple, 3)
        cart.add(orange, 2)
        
        expected = {"りんご": 3, "みかん": 2}
        self.assertEqual(cart.quantities(), expected)

    def test_mixed_products_operations(self):
        """複数種類の商品が混在するケースで、追加・削除・数量集計・小計計算が正しく動作することをテスト"""
        cart = Cart()
        apple = Product("りんご", 100)
        orange = Product("みかん", 80)
        banana = Product("バナナ", 120)
        
        cart.add(apple, 2)
        cart.add(orange, 1)
        cart.add(banana, 4)
        
        # 混在時の小計: 100*2 + 80*1 + 120*4 = 200 + 80 + 480 = 760
        self.assertEqual(cart.subtotal(), 760)
        self.assertEqual(cart.count(), 7)
        self.assertEqual(cart.quantities(), {"りんご": 2, "みかん": 1, "バナナ": 4})
        
        # 特定商品の削除と混在状態の変化
        cart.remove(banana)
        self.assertEqual(cart.quantities(), {"りんご": 2, "みかん": 1, "バナナ": 3})
        self.assertEqual(cart.subtotal(), 760 - 120)


if __name__ == "__main__":
    unittest.main()
