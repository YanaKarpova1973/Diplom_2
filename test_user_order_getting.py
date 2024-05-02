import allure
import requests
import datas

class TestUserOrderGetting:

    @allure.title('Успешная проверка получения заказов авторизованного пользователя')
    def test_getting_order_authorized_user(self, user, order_making):
        headers = {'Authorization': user['access_token']}
        response = requests.get(datas.user_order, headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['orders'][0]['number'] == order_making

    @allure.title('Ошибка проверки получения заказов неавторизованного пользователя')
    def test_getting_order_unauthorized_user(self):
        response = requests.get(datas.user_order)
        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'You should be authorised'
