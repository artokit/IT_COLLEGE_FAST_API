from fastapi import FastAPI
from routers import cars, clients, orders

app = FastAPI()
app.include_router(cars.router)
app.include_router(clients.router)
app.include_router(orders.router)
