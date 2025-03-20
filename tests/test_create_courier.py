import allure
import requests
from helper import Helper
from urls import Urls


class TestCreateCourier:
    @allure.title("Создание нового курьера")
    def test_create_courier(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("POST на создание курьера"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 201
        with allure.step("Проверяем текст ответа"):
            expected_text = '{"ok":true}'
            assert response.text == expected_text

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_same_couriers(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("POST на создание курьера"):
            requests.post(Urls.URL_COURIER_CREATE, data=payload)
        with allure.step("POST на создание курьера с теми же данными"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response_data['code'] == 409
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Этот логин уже используется. Попробуйте другой.'
            assert response_data['message'] == expected_text

    @allure.title("Ошибка при создании без логина")
    def test_cannot_create_courier_without_login(self, generate_random_data):
        payload = {
            "login": '',
            "password": generate_random_data[1],
            "firstName": generate_random_data[2]
        }
        with allure.step("POST на создание курьера"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 400
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Недостаточно данных для создания учетной записи'
            assert response_data['message'] == expected_text

    @allure.title("Ошибка при создании без пароля")
    def test_cannot_create_courier_without_password(self, generate_random_data):
        payload = {
            "login": generate_random_data[0],
            "password": '',
            "firstName": generate_random_data[2]
        }
        with allure.step("POST на создание курьера"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 400
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Недостаточно данных для создания учетной записи'
            assert response_data['message'] == expected_text

    @allure.title("Ошибка при создании с существующим логином")
    def test_cannot_create_courier_with_already_exist_login(self, generate_random_data):
        with allure.step("Подготовка данных"):
            helper = Helper()
            password_2 = helper.generate_random_string(10)
            firstName_2 = helper.generate_random_string(10)
            payload = {
                "login": generate_random_data[0],
                "password": generate_random_data[1],
                "firstName": generate_random_data[2]
            }
            payload_for_error = {
                "login": generate_random_data[0],
                "password": password_2,
                "firstName": firstName_2
            }
        with allure.step("POST на создание курьера"):
            requests.post(Urls.URL_COURIER_CREATE, data=payload)
        with allure.step("POST на создание курьера c тем же логином"):
            response = requests.post(Urls.URL_COURIER_CREATE, data=payload_for_error)
            response_data = response.json()
        with allure.step("Проверяем статус код ответа"):
            assert response.status_code == 409
        with allure.step("Проверяем текст ответа"):
            expected_text = 'Этот логин уже используется. Попробуйте другой.'
            assert response_data['message'] == expected_text