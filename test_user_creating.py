import allure
import pytest
import requests
import datas

class TestUserCreating:

    @allure.title('Успешная проверка создания нового пользователя')
    def test_register_successful_result(self, user_creating):
        payload = {
            'email': user_creating['email'],
            'password': user_creating['password'],
            'name': user_creating['name']
        }
        response = requests.post(datas.user_register, data=payload)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Ошибка при попытке повторного создания существующего пользователя')
    def test_register_double_user_failed_result(self, user):
        payload = {
            'email': user['email'],
            'password': user['password'],
            'name': user['name']
        }
        response = requests.post(datas.user_register, data=payload)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Ошибка при создании пользователя без заполнения обязательных полей: email, password и name')
    @pytest.mark.parametrize('payload', [
        {'email': 'login@ya.ru', 'name': 'username'},
        {'email': 'login@ya.ru', 'password': 123456},
        {'password': 123456, 'name': 'username'}
    ])
    def test_register_without_one_field_failed_result(self, payload):
        response = requests.post(datas.user_register, data=payload)
        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json()['message'] == 'Email, password and name are required fields'
