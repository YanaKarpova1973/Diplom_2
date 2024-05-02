import allure
import requests
import datas

class TestUserLogin:

    @allure.title('Проверка логина существующего пользователя')
    def test_user_login_successful_login(self, user):
        payload = {
            'email': user['email'],
            'password': user['password']
        }
        response = requests.post(datas.user_login, data=payload)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Ошибка при проверке пользователя с некорректным логином')
    def test_login_incorrect_email_failed_result(self, user):
        payload = {
            'email': datas.incorrect_email,
            'password': user['password']
        }
        response = requests.post(datas.user_login, data=payload)
        assert response.status_code == 401
        assert response.json()['message'] == 'email or password are incorrect'
        assert response.json().get("success") is False

    @allure.title('Ошибка при проверке пользователя с некорректным паролем')
    def test_login_incorrect_password_failed_result(self, user):
        payload = {
            'email': user['email'],
            'password': datas.incorrect_password
        }
        response = requests.post(datas.user_login, data=payload)
        assert response.status_code == 401
        assert response.json()['message'] == 'email or password are incorrect'
        assert response.json().get("success") is False
