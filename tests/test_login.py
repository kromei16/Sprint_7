import allure
import requests
from urls import Urls


class TestLogin:
    @allure.title("Успешный логин курьера")
    def test_login_courier_successful(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": courier_data[0],
                "password": courier_data[1]
            }
        with allure.step("POST для логина курьера"):
            response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 200
        with allure.step("Проверяем наличие id в ответе"):
            assert 'id' in response_data

    @allure.title("Логин курьера без логина")
    def test_login_courier_without_login(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": '',
                "password": courier_data[1]
            }
        with allure.step("POST для логина курьера"):
            response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 400
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Недостаточно данных для входа'
            assert response_data['message'] == expected_text

    @allure.title("Логин курьера без пароля")
    def test_login_courier_without_password(self, register_new_courier_and_return_login_password):
        with allure.step("Подготовка данных"):
            courier_data = register_new_courier_and_return_login_password
            payload = {
                "login": courier_data[0],
                "password": ''
            }
        with allure.step("POST для логина курьера"):
            response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 400
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Недостаточно данных для входа'
            assert response_data['message'] == expected_text

    @allure.title("Логин не существующего курьера")
    def test_login_non_existent_courier(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("Отправляем запрос на логин курьера"):
            response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 404
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Учетная запись не найдена'
            assert response_data['message'] == expected_text