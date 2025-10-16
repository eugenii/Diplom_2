import allure
import requests

from data import ORDERS_URL, INGREDIENTS_URL


class OrderMethods:
    @allure.step('Создание заказа')
    def create_order(self, ingredients, auth_token=None):
        """Создание заказа."""
        payload = {
            "ingredients": ingredients
        }
        
        headers = {}
        if auth_token:
            headers['Authorization'] = auth_token
        
        try:
            response = requests.post(ORDERS_URL, json=payload, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при создании заказа: {e}")
            return None

    @allure.step('Получение заказов пользователя')
    def get_user_orders(self, auth_token):
        """Получение заказов конкретного пользователя."""
        headers = {'Authorization': auth_token}
        
        try:
            response = requests.get(ORDERS_URL, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении заказов: {e}")
            return None

    @allure.step('Получение списка ингредиентов')
    def get_ingredients(self):
        """Получение списка всех ингредиентов."""
        try:
            response = requests.get(INGREDIENTS_URL)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении ингредиентов: {e}")
            return None