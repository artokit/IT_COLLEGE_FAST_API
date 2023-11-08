from fastapi import APIRouter, Query
import services
from database.business_logic import Order, Car
from db_dataclasses import ClientCars, CarModel, OrderModel, AddCarModel, DeleteModel

router = APIRouter()


@router.get('/get_client_cars', response_model=ClientCars)
def get_client_cars(client_id: int):
    cars_id = [OrderModel(**i).car_pk for i in Order.get_by_client_pk(client_id)]
    return ClientCars(200, [CarModel(**i) for i in Car.get_cars(cars_id)])


@router.get('/get_car', status_code=200, response_model=CarModel)
async def get_car(car_id: int):
    return services.get_obj_by_pk(Car, car_id, CarModel)


@router.post('/add_car', response_model=AddCarModel, status_code=200)
def add_car(brand: str, model: str, year_of_issue: int, vin_code: str = Query(min_length=17, max_length=17)):
    return services.create_model(
        Car,
        brand=brand,
        model=model,
        year_of_issue=year_of_issue,
        vin_code=vin_code
    )


@router.delete('/del_car', response_model=DeleteModel)
def del_car(car_id: int):
    return services.del_obj_by_pk(Car, car_id)


@router.post('/update_car', response_model=CarModel)
def update_car(car_id: int, brand: str = None, model: str = None, year_of_issue: int = None, vin_code: str = None):
    return services.update_obj_by_pk(
        Car,
        car_id,
        CarModel,
        brand=brand,
        model=model,
        year_of_issue=year_of_issue,
        vin_code=vin_code,
    )
