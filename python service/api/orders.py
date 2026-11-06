from fastapi import APIRouter, HTTPException

from api.schemas import OrderRequest
from data import catalog, order_repository
from services import order_service
from services.order_service import OrderError

router = APIRouter()


@router.get("/products")
def get_products():
    return catalog.list_products()


@router.get("/orders")
def get_orders():
    return order_repository.find_all()


@router.post("/orders")
def create_order(request: OrderRequest):
    items = [item.model_dump() for item in request.items]
    try:
        return order_service.place_order(request.customer, request.tier, items)
    except OrderError as error:
        raise HTTPException(status_code=400, detail=str(error))
