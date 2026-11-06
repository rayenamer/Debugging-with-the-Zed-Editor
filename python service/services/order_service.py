from data import catalog, order_repository
from domain import pricing


class OrderError(Exception):
    pass


def place_order(customer, tier, items):
    order = _new_order(customer)
    for item in items:
        order["lines"].append(_build_line(item, tier))
    order["total"] = round(sum(line["total"] for line in order["lines"]), 2)
    return order_repository.save(order)


def _new_order(customer, lines=[]):
    return {"customer": customer, "lines": lines}


def _build_line(item, tier):
    sku = item["sku"]
    quantity = item["quantity"]

    product = catalog.find_product(sku)
    if product is None:
        raise OrderError(f"Unknown product: {sku}")
    if product["stock"] < quantity:
        raise OrderError(f"Not enough stock for {sku}")

    catalog.reduce_stock(sku, quantity)
    priced = pricing.apply_tier(product, tier)
    return {
        "sku": sku,
        "quantity": quantity,
        "unit_price": priced["price"],
        "total": pricing.line_total(priced["price"], quantity),
    }
