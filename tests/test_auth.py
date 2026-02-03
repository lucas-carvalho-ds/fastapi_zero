from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'user_inexistent', 'password': 'inexistent123'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password.'}


def test_login_incorrect_credentials(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'incorrect_password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password.'}
