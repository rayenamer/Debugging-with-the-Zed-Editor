from fastapi import FastAPI

from orders import build_order

app = FastAPI()


@app.get("/order")
def order(item: str):
    return build_order(item)
