import allure
import pytest
from methods.user_methods import UserMethods
from methods.order_methods import OrderMethods
from data import TestUser, TestOrder

class TestOrders:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_methods = UserMethods()
        self.order_methods = OrderMethods()
        self.auth_token = None
        self.registered_email = None
    
    def register_and_login_user(self):
        """Вспомогательный метод для регистрации и логина пользователя."""
        self.registered_email = TestUser.generate_unique_email()
        
        register_response = self.user_methods.create_user(
            email=self.registered_email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        
        assert register_response.status_code == 200
        register_data = register_response.json()
        self.auth_token = register_data['accessToken']
        
        return self.auth_token

    def get_valid_ingredients(self):
        """Получение валидных ID ингредиентов."""
        response = self.order_methods.get_ingredients()
        if response.status_code == 200:
            ingredients_data = response.json()
            if ingredients_data['success'] and len(ingredients_data['data']) > 0:
                # Берем первые два ингредиента
                return [ingredient['_id'] for ingredient in ingredients_data['data'][:2]]
        # Если не удалось получить ингредиенты, используем тестовые
        return TestOrder.VALID_INGREDIENTS

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth_and_ingredients(self):
        """Тест создания заказа авторизованным пользователем с ингредиентами."""
        auth_token = self.register_and_login_user()
        valid_ingredients = self.get_valid_ingredients()
        
        create_response = self.order_methods.create_order(
            ingredients=valid_ingredients,
            auth_token=auth_token
        )
        
        assert create_response.status_code == 200
        order_data = create_response.json()
        
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data
        assert 'number' in order_data['order']

    @allure.title('Создание заказа без авторизации с ингредиентами')
    def test_create_order_without_auth_with_ingredients(self):
        """Тест создания заказа без авторизации с ингредиентами."""
        valid_ingredients = self.get_valid_ingredients()
        
        create_response = self.order_methods.create_order(
            ingredients=valid_ingredients,
            auth_token=None  # Без авторизации
        )
        
        # ИСПРАВЛЕНИЕ: Неавторизованные пользователи МОГУТ создавать заказы
        assert create_response.status_code == 200
        order_data = create_response.json()
        
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data
        assert 'number' in order_data['order']

    @allure.title('Создание заказа с авторизацией без ингредиентов')
    def test_create_order_with_auth_without_ingredients(self):
        """Тест создания заказа авторизованным пользователем без ингредиентов."""
        auth_token = self.register_and_login_user()
        
        create_response = self.order_methods.create_order(
            ingredients=TestOrder.EMPTY_INGREDIENTS,
            auth_token=auth_token
        )
        
        assert create_response.status_code == 400
        order_data = create_response.json()
        
        assert order_data['success'] == False
        assert order_data['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа без авторизации и без ингредиентов')
    def test_create_order_without_auth_without_ingredients(self):
        """Тест создания заказа без авторизации и без ингредиентов."""
        create_response = self.order_methods.create_order(
            ingredients=TestOrder.EMPTY_INGREDIENTS,
            auth_token=None
        )
        
        # ИСПРАВЛЕНИЕ: Неавторизованные пользователи получают ошибку валидации (400)
        assert create_response.status_code == 400
        order_data = create_response.json()
        
        assert order_data['success'] == False
        assert order_data['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash(self):
        """Тест создания заказа с невалидным хешем ингредиентов."""
        auth_token = self.register_and_login_user()
        
        create_response = self.order_methods.create_order(
            ingredients=TestOrder.INVALID_INGREDIENTS,
            auth_token=auth_token
        )
        
        assert create_response.status_code == 500
        
        # ИСПРАВЛЕНИЕ: Аккуратная обработка 500 ошибки
        # Сервер может вернуть HTML вместо JSON при 500 ошибке
        try:
            if create_response.text and create_response.text.strip():
                order_data = create_response.json()
                # Если есть JSON, проверяем его
                if 'success' in order_data:
                    assert order_data['success'] == False
        except Exception as e:
            # Если не удалось распарсить JSON, это нормально для 500 ошибки
            print(f"Не удалось распарсить ответ при 500 ошибке: {e}")
            # Проверяем, что это действительно Internal Server Error
            assert "Internal Server Error" in create_response.text

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_user_orders_with_auth(self):
        """Тест получения заказов авторизованного пользователя.
        Примечание: неавторизованные пользователи могут создавать заказы,
        но для получения истории заказов требуется авторизация.
        """
        auth_token = self.register_and_login_user()
        
        # Сначала создаем заказ, чтобы у пользователя была история
        valid_ingredients = self.get_valid_ingredients()
        create_response = self.order_methods.create_order(
            ingredients=valid_ingredients,
            auth_token=auth_token
        )
        assert create_response.status_code == 200
        
        # Получаем заказы пользователя
        orders_response = self.order_methods.get_user_orders(auth_token=auth_token)
        
        assert orders_response.status_code == 200
        orders_data = orders_response.json()
        
        assert orders_data['success'] == True
        assert 'orders' in orders_data
        assert isinstance(orders_data['orders'], list)

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_user_orders_without_auth(self):
        """Тест получения заказов неавторизованного пользователя."""
        orders_response = self.order_methods.get_user_orders(auth_token=None)
        
        assert orders_response.status_code == 401
        orders_data = orders_response.json()
        
        assert orders_data['success'] == False
        assert orders_data['message'] == 'You should be authorised'

    @allure.title('Создание заказа с одним ингредиентом')
    def test_create_order_with_single_ingredient(self):
        """Тест создания заказа с одним ингредиентом."""
        auth_token = self.register_and_login_user()
        valid_ingredients = self.get_valid_ingredients()
        
        # Берем только первый ингредиент
        single_ingredient = [valid_ingredients[0]]
        
        create_response = self.order_methods.create_order(
            ingredients=single_ingredient,
            auth_token=auth_token
        )
        
        assert create_response.status_code == 200
        order_data = create_response.json()
        
        assert order_data['success'] == True
        assert 'name' in order_data
        assert 'order' in order_data