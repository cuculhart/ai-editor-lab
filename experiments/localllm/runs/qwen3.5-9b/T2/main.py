from cart import Cart

cart = Cart()
cart.add_item("apple", 100, 3)
cart.add_item("tea", 250, 2)

print("subtotal:", cart.subtotal())
print("total (10% member discount):", cart.total(0.1))
