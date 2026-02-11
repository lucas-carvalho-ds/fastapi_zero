from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import Todo, TodoState, User


@pytest.mark.asyncio
async def test_create_user_db(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret_test'
        )

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'test')
        )

    assert user is not None
    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
        'password': 'secret_test',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo_db(session: AsyncSession, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        new_todo = Todo(
            title='To do Example',
            description='A description about the task.',
            state=TodoState.draft,
            user_id=user.id,
        )

        session.add(new_todo)
        await session.commit()

        todo = await session.scalar(
            select(Todo).where(Todo.title == 'To do Example')
        )

        assert todo is not None
        assert asdict(todo) == {
            'id': 1,
            'title': 'To do Example',
            'description': 'A description about the task.',
            'state': TodoState.draft,
            'created_at': time,
            'updated_at': time,
            'user_id': user.id,
        }


@pytest.mark.asyncio
async def test_user_todo_relationship(session: AsyncSession, user):
    todo = Todo(
        title='To do Example',
        description='A description about the task.',
        state=TodoState.draft,
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]  # type: ignore
