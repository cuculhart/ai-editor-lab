import unittest

from omise.cart import Cart
from omise.models import Product


class TestCart(unittest.TestCase):
    def test_remove_product(self):
        """商品を削除するテスト"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        cart.add(apple, 2)
        cart.add(banana, 1)
        
        self.assertEqual(cart.count(apple), 2)
        self.assertEqual(cart.count(banana), 1)
        
        cart.remove(apple)
        
        self.assertEqual(cart.count(apple), 0)
        self.assertEqual(cart.count(banana), 1)
        self.assertEqual(cart.count(), 1)
        self.assertEqual(cart.quantities(), {"banana": 1})

    def test_remove_product_already_removed(self):
        """既に削除済みの商品を再度削除した場合"""
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 2)
        cart.remove(apple)
        cart.remove(apple)  # 次に削除
        self.assertEqual(cart.count(apple), 0)

    def test_quantities_mixed_products(self):
        """複数種類の商品が混在するケースの quantities()"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        orange = Product("オレンジ", 70)
        cart.add(apple, 2)
        cart.add(banana, 1)
        cart.add(orange, 3)
        
        self.assertEqual(cart.quantities(), {"りんご": 2, "バナナ": 1, "オレンジ": 3})
        self.assertEqual(cart.quantities(), dict(sorted(cart.quantities().items())))

    def test_quantities_empty_cart(self):
        """空のカートでの quantities() テスト"""
        cart = Cart()
        self.assertEqual(cart.quantities(), {})

    def test_quantities_same_product_multiple_times(self):
        """同じ商品名を複数回追加した場合の quantities()"""
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 5)  # 同じ商品名を複数回追加

        self.assertEqual(cart.quantities(), {"りんご": 5})

    def test_subtotal_mixed_products(self):
        """複数種類の商品が混在する subtotal() テスト"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        cart.add(apple, 2)
        cart.add(banana, 1)
        
        self.assertEqual(cart.subtotal(), 250)
        
        cart.remove(banana)
        self.assertEqual(cart.subtotal(), 200)


if __name__ == "__main__":
    unittest.main()
