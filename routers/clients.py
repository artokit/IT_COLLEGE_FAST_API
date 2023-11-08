from fastapi import APIRouter
import services
from database.business_logic import Client
from db_dataclasses import ClientModel, DeleteModel, AddClientModel

router = APIRouter()


@router.get('/get_client', status_code=200, response_model=ClientModel)
async def get_client(client_id: int):
    return services.get_obj_by_pk(Client, client_id, ClientModel)


@router.post('/add_client', response_model=AddClientModel, status_code=200)
def add_client(first_name: str, last_name: str, address: str, number: str):
    return services.create_model(
        Client,
        first_name=first_name,
        last_name=last_name,
        address=address,
        number=number
    )


@router.delete('/del_client', response_model=DeleteModel)
def del_client(client_id: int):
    return services.del_obj_by_pk(Client, client_id)


@router.post('/update_client', response_model=ClientModel)
def update_client(client_id: int, first_name: str = None, last_name: str = None, address: str = None, number: str = None):
    return services.update_obj_by_pk(
        Client,
        client_id,
        ClientModel,
        first_name=first_name,
        last_name=last_name,
        address=address,
        number=number,
    )
