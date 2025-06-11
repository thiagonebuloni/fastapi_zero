from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA) triple A
    - A: Arrange
    - A: Act
    - A: Assert
    """
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_ola_mundo_deve_retornar_ola_mundo(client):
    response = client.get('/ola_mundo/')

    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá mundo!</h1>' in response.text
