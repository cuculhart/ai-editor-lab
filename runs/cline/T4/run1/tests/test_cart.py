import unittest

from omise.cart import Cart
from omise.models import Product


class TestCart(unittest.TestCase):
    def test_add_and_count(self):
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 3)
        self.assertEqual(cart.count(), 3)
        self.assertEqual(cart.count(apple), 3)

    def test_subtotal(self):
        cart = Cart()
        cart.add(Product("りんご", 100), 2)
        cart.add(Product("みかん", 80), 1)
        self.assertEqual(cart.subtotal(), 280)

    def test_add_invalid_quantity(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add(Product("りんご", 100), 0)

    def test_remove_product(self):
        """remove メソッドで商品を削除できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 3)
        cart.add(apple, 2)
        self.assertEqual(cart.count(apple), 5)
        
        # remove を呼ぶ
        cart.remove(apple)
        
        # 削除された製品は存在しない
        self.assertEqual(cart.count(apple), 4)

    def test_quantities(self):
        """quantities メソッドで各商品名の数量を取得できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        cart.add(apple, 2)
        cart.add(banana, 3)
        
        quantities = cart.quantities()
        self.assertEqual(quantities, {"りんご": 2, "バナナ": 3})

    def test_quantities_mixed_products(self):
        """quantities メソッドで複数種類の商品が混在する場合、正しい数量を返すこと"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        cherry = Product("イチゴ", 30)
        cart.add(apple, 2)
        cart.add(banana, 3)
        cart.add(apple, 1)
        cart.add(cherry, 5)
        
        # りんごは合計 3 個、バナナは 3 個、イチゴは 5 個
        quantities = cart.quantities()
        self.assertEqual(quantities, {"りんご": 3, "バナナ": 3, "イチゴ": 5})

    def test_remove_mixed_products(self):
        """remove メソッドで複数種類の商品を削除できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 50)
        cart.add(apple, 2)
        cart.add(banana, 3)
        
        self.assertEqual(cart.count(apple), 2)
        self.assertEqual(cart.count(banana), 3)
        
        # りんごを削除
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 0)
        self.assertEqual(cart.count(banana), 3)


if __name__ == "__main__":
    unittest.main()