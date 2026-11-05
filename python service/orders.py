def build_order(item, items=[]):
    items.append(item)
    return {"items": items, "count": len(items)}
