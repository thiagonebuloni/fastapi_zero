from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.schemas import Message

app = FastAPI(title="FastAPI do duno")


@app.get(
        '/',
         status_code=HTTPStatus.OK,
        response_model=Message
         )
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
        '/ola_mundo',
        status_code=HTTPStatus.OK,
        # response_model=Message
         )
def ola_mundo():
    return "Olá mundo!"
