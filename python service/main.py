from fastapi import FastAPI

from api.orders import router

app = FastAPI(title="Order Service")
app.include_router(router)
