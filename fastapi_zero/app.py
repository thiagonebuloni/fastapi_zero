from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import (
    Message,
)

app = FastAPI(title='FastAPI do duno')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/ola_mundo/', status_code=HTTPStatus.OK)
async def ola_mundo():
    html = """
        <html><head>Olá mundo!</head><body><h1>Olá mundo!</h1></body></html>
    """
    return html
