_products = {
    "apple": {"sku": "apple", "price": 2.0, "stock": 20},
    "pear": {"sku": "pear", "price": 1.5, "stock": 50},
    "mango": {"sku": "mango", "price": 5.0, "stock": 3},
}


def list_products():
    return list(_products.values())


def find_product(sku):
    return _products.get(sku)


def reduce_stock(sku, quantity):
    _products[sku]["stock"] -= quantity
