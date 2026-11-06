BULK_MIN_QUANTITY = 10
BULK_RATE = 0.05
TIER_RATES = {"standard": 0.0, "gold": 0.10}


def apply_tier(product, tier):
    rate = TIER_RATES.get(tier, 0.0)
    product["price"] = round(product["price"] * (1 - rate), 2)
    return product


def line_total(unit_price, quantity):
    total = unit_price * quantity
    if quantity > BULK_MIN_QUANTITY:
        total = total * (1 - BULK_RATE)
    return round(total, 2)
