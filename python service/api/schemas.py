from pydantic import BaseModel


class OrderItem(BaseModel):
    sku: str
    quantity: int


class OrderRequest(BaseModel):
    customer: str
    tier: str = "standard"
    items: list[OrderItem]
