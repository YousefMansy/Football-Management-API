import json
from jose import jwt
from app.footballfantasyapi.core.config import settings


def test_create_user(client, user_data):
    response = client.post('/auth/signup', json.dumps(user_data))
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['user']['email'] == 'test@footballfantasyapi.com'
    assert len(response_json['players']) == settings.INITIAL_PLAYERS_COUNT
    assert response_json['team']['funds'] == settings.INITIAL_TEAM_FUNDS
    assert response_json['team']['value'] == sum(p['market_value'] for p in response_json['players'])


def test_user_can_login_successfully_and_receives_valid_token(client, user_data):
    client.post('/auth/signup', json.dumps(user_data))
    client.headers['content-type'] = 'application/x-www-form-urlencoded'
    login_data = {'username': 'test@footballfantasyapi.com', 'password': 'testing'}
    res = client.post('/auth/login', data=login_data)
    assert res.status_code == 200
    token = res.json().get('access_token')  # check that token exists in response
    assert jwt.decode(token, str(settings.JWT_SECRET), algorithms=[settings.ALGORITHM], options={'verify_aud': False})
    assert 'token_type' in res.json()  # check that token is of the proper type
    assert res.json().get('token_type') == 'bearer'


def test_user_with_wrong_creds_doesnt_receive_token(client, login_data):
    res = client.post('/auth/login', data=login_data)
    assert res.status_code == 400
    assert "access_token" not in res.json()


def test_authenticated_user_can_read_profile(authorized_client, user_data):
    response = authorized_client.get('/auth/profile')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['user']['email'] == user_data['email']
    assert len(response_json['players']) == settings.INITIAL_PLAYERS_COUNT
    assert response_json['team']['funds'] == settings.INITIAL_TEAM_FUNDS
    assert response_json['team']['value'] == sum(p['market_value'] for p in response_json['players'])
