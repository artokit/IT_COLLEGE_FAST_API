from dataclasses import dataclass
from fastapi import Query


@dataclass
class CarModel:
    pk: int
    brand: str
    model: str
    year_of_issue: int
    vin_code: str = Query(min_length=17, max_length=17)


@dataclass
class OrderModel:
    pk: int
    car_pk: int
    client_pk: int
    date: str
    description: str
    status: str


@dataclass
class ClientModel:
    pk: int
    first_name: str
    last_name: str
    address: str
    number: str


@dataclass
class AddOrderModel:
    status: int
    result: OrderModel


@dataclass
class AddCarModel:
    status: int
    result: CarModel


@dataclass
class AddClientModel:
    status: int
    result: ClientModel


@dataclass
class DeleteModel:
    pk: int
    status: int
    operation = 'delete'


@dataclass
class DefaultUpdate:
    pk: int
    status: int
    operation = 'update'


@dataclass
class UpdateCarModel(DefaultUpdate):
    obj: CarModel


@dataclass
class UpdateClientModel(DefaultUpdate):
    obj: ClientModel


@dataclass
class UpdateOrderModel(DefaultUpdate):
    obj: OrderModel


@dataclass
class ClientOrders:
    status: int
    orders: list[OrderModel]


@dataclass
class ClientCars:
    status: int
    cars: list[CarModel]
