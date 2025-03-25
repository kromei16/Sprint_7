import pytest
import requests
import random
import string

from helper import Helper
from urls import Urls


@pytest.fixture
# Метод регистрации нового курьера возвращает список из логина и пароля
# Если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # Создаём список, чтобы метод мог его вернуть
    login_pass = []

    # Генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(Urls.URL_COURIER_CREATE, data=payload)

    # Если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    yield login_pass

    payload = {
        "login": login_pass[0],
        "password": login_pass[1]
    }

    # Логиним курьера
    response = requests.post(Urls.URL_COURIER_LOGIN, data=payload)
    response_data = response.json()
    courier_id = response_data['id']

    # Удаляем курьера
    response = requests.delete(f"{Urls.URL_COURIER_DELETE}/{courier_id}")


@pytest.fixture
def generate_random_data():
    helper = Helper()
    login = helper.generate_random_string(10)
    password = helper.generate_random_string(10)
    first_name = helper.generate_random_string(10)
    user_data = []
    user_data.append(login)
    user_data.append(password)
    user_data.append(first_name)
    return user_data
