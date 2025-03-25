import allure
import requests
from urls import Urls


class TestGetListOfOrders():
    @allure.title("В теле ответа возвращается список заказов")
    def test_get_list_of_orders(self):
        with allure.step("GET для получения списка заказов"):
            response = requests.get(Urls.URL_GET_LIST_OF_ORDERS)
            response_data = response.json()
        with allure.step("Проверяем, что в теле ответа есть список заказов"):
            assert response.status_code == 200
            assert 'orders' in response_data
            assert isinstance(response_data['orders'], list)