from http import HTTPStatus

from fastapi_zero.schemas import TodoPublic


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Almoçar 12:00',
            'description': 'Fazer pausa do expediente para almoçar',
            'state': 'todo',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'Almoçar 12:00',
        'description': 'Fazer pausa do expediente para almoçar',
        'state': 'todo',
        'id': 1,
    }


def test_get_todos(client, todo, token):
    todos_schema = TodoPublic.model_validate(todo).model_dump()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'todos': [todos_schema]}
