from fastapi import APIRouter
import services
from database.business_logic import Order
from db_dataclasses import OrderModel, AddOrderModel, DeleteModel, ClientOrders

router = APIRouter()


@router.get('/get_order', status_code=200, response_model=OrderModel)
async def get_order(order_id: int):
    return services.get_obj_by_pk(Order, order_id, OrderModel)


@router.post('/add_order', status_code=200, response_model=AddOrderModel)
def add_order(car_pk: int, client_pk: int, date: str, description: str, status: str):
    return services.create_model(
        Order,
        car_pk=car_pk,
        client_pk=client_pk,
        date=date,
        description=description,
        status=status
    )


@router.delete('/del_order', response_model=DeleteModel)
def del_order(order_id: int):
    return services.del_obj_by_pk(Order, order_id)


@router.post('/update_order', response_model=OrderModel)
def update_order(order_id: int, car_pk: int = None, client_pk: int = None, date: str = None, description: str = None,
                 status: str = None):
    return services.update_obj_by_pk(
        Order,
        order_id,
        OrderModel,
        car_pk=car_pk,
        client_pk=client_pk,
        date=date,
        description=description,
        status=status
    )


@router.get('/get_client_orders', response_model=ClientOrders)
def get_client_orders(client_id: int):
    return ClientOrders(200, [OrderModel(**i) for i in Order.get_by_client_pk(client_id)])
