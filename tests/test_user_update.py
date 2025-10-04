import allure
import pytest
from methods.user_methods import UserMethods
from data import TestUser

class TestUserUpdate:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_methods = UserMethods()
        self.auth_token = None
        self.registered_email = None
    
    def register_and_login_user(self):
        """Вспомогательный метод для регистрации и логина пользователя."""
        # Регистрируем пользователя
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

    @allure.title('Обновление email авторизованного пользователя')
    def test_update_user_email_with_auth(self):
        """Тест обновления email авторизованного пользователя."""
        # Регистрируем и логиним пользователя
        auth_token = self.register_and_login_user()
        
        # Обновляем email
        new_email = TestUser.generate_unique_email()
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token,
            email=new_email
        )
        
        assert update_response.status_code == 200
        update_data = update_response.json()
        
        assert update_data['success'] == True
        assert update_data['user']['email'] == new_email
        assert update_data['user']['name'] == TestUser.VALID_NAME  # Имя не должно измениться

    @allure.title('Обновление name авторизованного пользователя')
    def test_update_user_name_with_auth(self):
        """Тест обновления name авторизованного пользователя."""
        # Регистрируем и логиним пользователя
        auth_token = self.register_and_login_user()
        
        # Обновляем name
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token,
            name=TestUser.NEW_NAME
        )
        
        assert update_response.status_code == 200
        update_data = update_response.json()
        
        assert update_data['success'] == True
        assert update_data['user']['email'] == self.registered_email  # Email не должен измениться
        assert update_data['user']['name'] == TestUser.NEW_NAME

    @allure.title('Обновление password авторизованного пользователя')
    def test_update_user_password_with_auth(self):
        """Тест обновления password авторизованного пользователя."""
        # Регистрируем и логиним пользователя
        auth_token = self.register_and_login_user()
        
        # Обновляем password
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token,
            password=TestUser.NEW_PASSWORD
        )
        
        assert update_response.status_code == 200
        update_data = update_response.json()
        
        assert update_data['success'] == True
        
        # Проверяем, что с новым паролем можно залогиниться
        login_response = self.user_methods.login_user(
            email=self.registered_email,
            password=TestUser.NEW_PASSWORD
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert login_data['success'] == True

    @allure.title('Обновление всех полей авторизованного пользователя')
    def test_update_all_user_fields_with_auth(self):
        """Тест одновременного обновления всех полей авторизованного пользователя."""
        # Регистрируем и логиним пользователя
        auth_token = self.register_and_login_user()
        
        # Обновляем все поля
        new_email = TestUser.generate_unique_email()
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token,
            email=new_email,
            password=TestUser.NEW_PASSWORD,
            name=TestUser.NEW_NAME
        )
        
        assert update_response.status_code == 200
        update_data = update_response.json()
        
        assert update_data['success'] == True
        assert update_data['user']['email'] == new_email
        assert update_data['user']['name'] == TestUser.NEW_NAME
        
        # Проверяем, что с новыми данными можно залогиниться
        login_response = self.user_methods.login_user(
            email=new_email,
            password=TestUser.NEW_PASSWORD
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert login_data['success'] == True

    @allure.title('Обновление данных без авторизации')
    def test_update_user_data_without_auth(self):
        """Тест обновления данных пользователя без авторизации."""
        # Пытаемся обновить данные без токена
        update_response = self.user_methods.update_user_data(
            auth_token="",  # Пустой токен
            email=TestUser.NEW_EMAIL
        )
        
        assert update_response.status_code == 401
        update_data = update_response.json()
        
        assert update_data['success'] == False
        assert update_data['message'] == 'You should be authorised'

    @allure.title('Обновление email на уже существующий')
    def test_update_user_to_existing_email(self):
        """Тест обновления email на уже существующий в системе."""
        # Создаем первого пользователя
        auth_token1 = self.register_and_login_user()
        first_user_email = self.registered_email
        
        # Создаем второго пользователя
        second_user_email = TestUser.generate_unique_email()
        register_response2 = self.user_methods.create_user(
            email=second_user_email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        assert register_response2.status_code == 200
        
        # Пытаемся обновить email первого пользователя на email второго пользователя
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token1,
            email=second_user_email
        )
        
        assert update_response.status_code == 403
        update_data = update_response.json()
        
        assert update_data['success'] == False
        assert update_data['message'] == 'User with such email already exists'

    @allure.title('Получение данных пользователя без авторизации')
    def test_get_user_data_without_auth(self):
        """Тест получения данных пользователя без авторизации."""
        # Пытаемся получить данные без токена
        get_response = self.user_methods.get_user_data(auth_token="")
        
        assert get_response.status_code == 401
        get_data = get_response.json()
        
        assert get_data['success'] == False
        assert get_data['message'] == 'You should be authorised'

    @allure.title('Получение данных пользователя с авторизацией')
    def test_get_user_data_with_auth(self):
        """Тест получения данных пользователя с авторизацией."""
        # Регистрируем и логиним пользователя
        auth_token = self.register_and_login_user()
        
        # Получаем данные пользователя
        get_response = self.user_methods.get_user_data(auth_token=auth_token)
        
        assert get_response.status_code == 200
        get_data = get_response.json()
        
        assert get_data['success'] == True
        assert get_data['user']['email'] == self.registered_email
        assert get_data['user']['name'] == TestUser.VALID_NAME