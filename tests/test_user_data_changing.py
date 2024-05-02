import allure
import pytest
import requests
import datas
import supporter

class TestUserDataChanging:

    @allure.title('Успешная проверка изменения почты существующего пользователя')
    def test_user_changed_email_successful_result(self, user):
        new_email = supporter.generate_random_login()
        payload = {'email': new_email}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(datas.user_info, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['user']['email'] == new_email

    @allure.title('Успешная проверка изменения имени существующего пользователя')
    @pytest.mark.parametrize('name', ['new_name'])
    def test_user_changed_name_successful_result(self, user, name):
        payload = {'name': name}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(datas.user_info, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['user']['name'] == name

    @allure.title('Успешная проверка изменения пароля существующего пользователя')
    def test_user_changed_password_successful_result(self, user):
        new_password = supporter.generate_random_password()
        payload = {'password': new_password}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(datas.user_info, data=payload, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Ошибка при попытке изменения почты, пароля и имени неавторизованного пользователя')
    def test_unauthorized_user_changed_datas(self):
        email = supporter.generate_random_login()
        password = supporter.generate_random_password()
        name = supporter.generate_random_user_name(6)
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.patch(datas.user_info, data=payload)
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'You should be authorised'
