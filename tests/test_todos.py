from http import HTTPStatus

import factory
import factory.fuzzy
import pytest
from factory.base import Factory
from factory.faker import Faker

from fastapi_zero.models import Todo, TodoState


class TodoFactory(Factory):
    class Meta:
        model = Todo

    title = Faker('text')
    description = Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1
    user_id = 1


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            '/todos/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'Test todo',
                'description': 'Test todo description',
                'state': 'draft',
            },
        )

    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    session.commit

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
    )

    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='not')
    )

    await session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_state_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )

    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.trash)
    )

    await session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code - -HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


@pytest.mark.asyncio
async def test_delete_other_user_todo(session, client, other_user, token):
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()

    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code - -HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


@pytest.mark.asyncio
async def test_list_todos_should_return_all_expected_fields(
    session, user, client, token, mock_db_time
):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory.create(user_id=user.id)

        session.add(todo)

        await session.commit()

        await session.refresh(todo)

        response = client.get(
            '/todos/',
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.json()['todos'] == [
        {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'state': todo.state,
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }
    ]


# @pytest.mark.asyncio
# async def test_create_todo_error(session, user: User):
#     todo = Todo(
#         title='Test Todo',
#         description='Test Desc',
#         state='test',
#         user_id=user.id,
#     )

#     session.add(todo)
#     await session.commit()

#     with pytest.raises(LookupError):
#         await session.scalar(select(Todo))
