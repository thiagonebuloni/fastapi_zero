import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers import auth, todos, users
from fastapi_zero.schemas import (
    Message,
)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(title='FastAPI do duno')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/ola_mundo/', status_code=HTTPStatus.OK)
async def ola_mundo():
    html = """
        <html><head>Olá mundo!</head><body><h1>Olá mundo!</h1></body></html>
    """
    return html
