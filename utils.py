import sqlite3
from typing import Type
from db import DefaultDBTable
from fastapi.responses import JSONResponse

from db_dataclasses import DeleteModel, DefaultUpdate


def get_all_res(obj: Type[DefaultDBTable]):
    return JSONResponse(content={'status': 200, 'result': obj.get_all()})


def create_model(obj: Type[DefaultDBTable], **kwargs):
    try:
        d = obj.create(**kwargs)
        return JSONResponse(content={'status': 200, 'result': d})
    except sqlite3.IntegrityError:
        return JSONResponse(content={'status': 400, 'error': 'Value in database'}, status_code=400)


def get_obj_by_pk(obj: Type[DefaultDBTable], pk: int, dataclass_model):
    try:
        return dataclass_model(*obj.get_by_pk(pk))
    except TypeError:
        return JSONResponse({'status': 404, 'error': 'Not found'}, status_code=404)


def del_obj_by_pk(obj: Type[DefaultDBTable], pk: int):
    obj.delete_by_pk(pk)
    return DeleteModel(pk=pk, status=200)


def update_obj_by_pk(obj: Type[DefaultDBTable], pk: int, dataclass_model, **kwargs):
    obj.update_by_pk(pk, **kwargs)
    return get_obj_by_pk(obj, pk, dataclass_model)
