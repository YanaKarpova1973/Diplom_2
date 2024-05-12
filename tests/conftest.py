import pytest
import requests
import supporter
import datas

@pytest.fixture
def user_creating():
    email = supporter.generate_random_login()
    password = supporter.generate_random_password()
    name = supporter.generate_random_user_name(7)
    yield {
        'email': email,
        'password': password,
        'name': name
    }
    payload = {
        'email': email,
        'password': password
        }
    response = requests.post(datas.user_login, data=payload)
    access_token = response.json().get("accessToken")
    headers = {'Authorization': access_token}
    requests.delete(datas.user_info, headers=headers)

@pytest.fixture
def user(user_creating):
    payload = {
        'email': user_creating['email'],
        'password': user_creating['password'],
        'name': user_creating['name']
    }
    response = requests.post(datas.user_register, data=payload)
    access_token = response.json().get("accessToken")
    yield {
        'email': payload['email'],
        'password': payload['password'],
        'name': payload['name'],
        'access_token': access_token
    }
    headers = {'Authorization': access_token}
    requests.delete(datas.user_info, headers=headers)

@pytest.fixture
def order_making(user):
    order_payload = {
        'ingredients': ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
    }
    headers = {'Authorization': user['access_token']}
    response = requests.post(datas.user_order, data=order_payload, headers=headers)
    order_number = response.json()['order']['number']
    return order_number

@pytest.fixture
def get_ingredients():
    bun = None
    main = None
    sauce = None
    response = requests.get(datas.ingredients_getting)
    ingredients = response.json()['data']
    for ingredient in ingredients:
        if ingredient['type'] == 'bun':
            bun = ingredient['_id']
        elif ingredient['type'] == 'main':
            main = ingredient['_id']
        elif ingredient['type'] == 'sauce':
            sauce = ingredient['_id']
    return bun, main, sauce
