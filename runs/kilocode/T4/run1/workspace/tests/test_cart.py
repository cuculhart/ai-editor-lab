import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartOperations(unittest.TestCase):
    def test_remove_product(self):
        """商品を削除できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)
        cart.add(apple, 2)
        cart.add(banana, 1)
        self.assertEqual(cart.count(), 3)
        cart.remove(apple)
        self.assertEqual(cart.count(), 2)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(banana), 1)

    def test_quantities_method(self):
        """各商品の数量が辞書形式で正しく取得できること"""
        cart = Cart()
        apple = Product("りんご", 100)
        mikan = Product("みかん", 80)
        cart.add(apple, 3)
        cart.add(mikan, 2)
        qs = cart.quantities()
        self.assertEqual(qs, {"りんご": 3, "みかん": 2})

    def test_mixed_products_and_subtotal(self):
        """複数種類の商品が混在するケースで小計や数量管理が正しく動作すること"""
        cart = Cart()
        coffee = Product("コーヒー", 300)
        bread = Product("パン", 200)
        cart.add(coffee, 1)
        cart.add(bread, 2)
        self.assertEqual(cart.subtotal(), 700)
        self.assertEqual(cart.count(), 3)
        self.assertEqual(cart.quantities(), {"コーヒー": 1, "パン": 2})
        cart.remove(bread)
        self.assertEqual(cart.quantities(), {"コーヒー": 1, "パン": 1})
        self.assertEqual(cart.subtotal(), 500)


if __name__ == "__main__":
    unittest.main()
