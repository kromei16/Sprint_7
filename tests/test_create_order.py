import allure
import pytest
import requests
from urls import Urls

class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([]),
    ],)
    @allure.title("Создание заказа")
    def test_create_order_successful(self, color):
        with allure.step("Подготовка данных"):
            payload = {
                "firstName": "Kirill",
                "lastName": "Lavka",
                "address": "Dobro, 1 apt.",
                "metroStation": 5,
                "phone": "+7 900 789 11 55",
                "rentTime": 2,
                "deliveryDate": "2025-03-25",
                "comment": "Ne pridymal",
                "color": color
            }
        with allure.step("POST для создание заказа"):
            response = requests.post(Urls.URL_ORDERS_CREATE, json=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 201
        with allure.step("Проверяем что track есть в теле ответа"):
            assert 'track' in response_data