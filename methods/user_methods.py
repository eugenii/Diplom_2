import allure
import requests
from data import LOGIN_URL, REGISTER_URL, USER_URL


class UserMethods:
    
    @allure.step('Регистрация пользователя')
    def create_user(self, email, password, name):
        """Создание пользователя."""
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(REGISTER_URL, json=payload)
        return response
    
    @allure.step('Логин пользователя')
    def login_user(self, email, password):
        """Авторизация пользователя."""
        payload = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(LOGIN_URL, json=payload)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    @allure.step('Получение данных пользователя')
    def get_user_data(self, auth_token):
        """Получение данных пользователя по токену."""
        headers = {'Authorization': auth_token}
        
        try:
            response = requests.get(USER_URL, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    @allure.step('Обновление данных пользователя')
    def update_user_data(self, auth_token, email=None, password=None, name=None):
        """Обновление данных пользователя."""
        headers = {'Authorization': auth_token}
        payload = {}
        
        if email is not None:
            payload['email'] = email
        if password is not None:
            payload['password'] = password
        if name is not None:
            payload['name'] = name
        
        try:
            response = requests.patch(USER_URL, headers=headers, json=payload)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
    