import json
from typing import List, Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .db import database, dblogs, engine, metadata

app = FastAPI()


ListOrInt = Union[int, List]
ListOrIntRecursive = Union[int, List['ListOrIntRecursive']]


def flatten(result: List, unflatten_list: ListOrIntRecursive) -> List[int]:
    """
    because a recursive list is like a tree, use a infix traversal
    for build a flat list of its elements
    Notes:
        dont validate the first parameter,
        because fastapi validate it at request model level

    Args:
        result (list): the list where this function put the result.
        unflatten_list (list): The second parameter.

    Returns:
        None:  use the result var passed as arg1
    """
    for item in unflatten_list:
        if isinstance(item, int):
            result.append(item)
        elif isinstance(item, List):
            flatten(result, item)
        else:
            raise ValueError(item)


class RequestModel(BaseModel):
    """
    notes:
        Fastapi not support recursive typing yet
        the right way is:
            items: ListOrIntRecursive
    """
    items: ListOrInt


class ResponseModel(BaseModel):
    result: List[int]


@app.post("/flatten", response_model=ResponseModel)
async def main(request_model: RequestModel) -> ResponseModel:
    flatted_list = []
    try:
        flatten(flatted_list, request_model.items)
        query = dblogs.insert().values(
            request=json.dumps(request_model.items),
            response=json.dumps(flatted_list))
        await database.execute(query)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=jsonable_encoder(
                [{
                    "loc": ["body", "items", str(e)],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer"
                 },
                 {
                    "loc": ["body", "items", str(e)],
                    "msg": "value is not a valid list",
                    "type": "type_error.list"
                 }]))
    return JSONResponse({"results": flatted_list})


@app.get("/flatten_logs")
async def get_logs():
    query = dblogs.select()
    return await database.fetch_all(query)


@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
