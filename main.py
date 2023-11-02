from db import Car, Order, Client
import utils
from fastapi import FastAPI
from db_dataclasses import *
app = FastAPI()


@app.get('/get_car', status_code=200, response_model=CarModel)
async def get_car(car_id: int):
    return utils.get_obj_by_pk(Car, car_id, CarModel)


@app.get('/get_order', status_code=200, response_model=OrderModel)
async def get_order(order_id: int):
    return utils.get_obj_by_pk(Order, order_id, OrderModel)


@app.get('/get_client', status_code=200, response_model=ClientModel)
async def get_client(client_id: int):
    return utils.get_obj_by_pk(Client, client_id, ClientModel)


@app.post('/add_order', status_code=200, response_model=AddOrderModel)
def add_order(car_pk: int, client_pk: int, date: str, description: str, status: str):
    return utils.create_model(
        Order,
        car_pk=car_pk,
        client_pk=client_pk,
        date=date,
        description=description,
        status=status
    )


@app.post('/add_car', response_model=AddCarModel, status_code=200)
def add_car(brand: str, model: str, year_of_issue: int, vin_code: str = Query(min_length=17, max_length=17)):
    return utils.create_model(
        Car,
        brand=brand,
        model=model,
        year_of_issue=year_of_issue,
        vin_code=vin_code
    )


@app.post('/add_client', response_model=AddClientModel, status_code=200)
def add_client(first_name: str, last_name: str, address: str, number: str):
    return utils.create_model(
        Client,
        first_name=first_name,
        last_name=last_name,
        address=address,
        number=number
    )


@app.delete('/del_order', response_model=DeleteModel)
def del_order(order_id: int):
    return utils.del_obj_by_pk(Order, order_id)


@app.delete('/del_client', response_model=DeleteModel)
def del_client(client_id: int):
    return utils.del_obj_by_pk(Client, client_id)


@app.delete('/del_car', response_model=DeleteModel)
def del_car(car_id: int):
    return utils.del_obj_by_pk(Car, car_id)


@app.post('/update_car', response_model=CarModel)
def update_car(car_id: int, brand: str = None, model: str = None, year_of_issue: int = None, vin_code: str = None):
    return utils.update_obj_by_pk(
        Car,
        car_id,
        CarModel,
        brand=brand,
        model=model,
        year_of_issue=year_of_issue,
        vin_code=vin_code,
    )


@app.post('/update_order', response_model=OrderModel)
def update_order(order_id: int, car_pk: int = None, client_pk: int = None, date: str = None, description: str = None,
                 status: str = None):
    return utils.update_obj_by_pk(
        Order,
        order_id,
        OrderModel,
        car_pk=car_pk,
        client_pk=client_pk,
        date=date,
        description=description,
        status=status
    )


@app.post('/update_client', response_model=ClientModel)
def update_client(client_id: int, first_name: str = None, last_name: str = None, address: str = None, number: str = None):
    return utils.update_obj_by_pk(
        Client,
        client_id,
        ClientModel,
        first_name=first_name,
        last_name=last_name,
        address=address,
        number=number,
    )


@app.get('/get_client_orders', response_model=ClientOrders)
def get_client_orders(client_id: int):
    return ClientOrders(200, [OrderModel(**i) for i in Order.get_by_client_pk(client_id)])


@app.get('/get_client_cars', response_model=ClientCars)
def get_client_cars(client_id: int):
    cars_id = [OrderModel(**i).car_pk for i in Order.get_by_client_pk(client_id)]
    print(cars_id)
    return ClientCars(200, [CarModel(**i) for i in Car.get_cars(cars_id)])
