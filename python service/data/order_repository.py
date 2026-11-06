_orders = []


def save(order):
    order["id"] = len(_orders) + 1
    _orders.append(order)
    return order


def find_all():
    return _orders
