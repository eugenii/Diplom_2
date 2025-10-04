import allure
import pytest
from methods.user_methods import UserMethods
from data import TestUser

class TestUserLogin:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_methods = UserMethods()
        self.registered_user = None
    
    def teardown_method(self):
        """Очистка после каждого теста"""
        # Здесь позже добавим удаление пользователя
        pass

    @allure.title('Успешный логин пользователя')
    def test_login_user_success(self):
        """Тест успешной авторизации пользователя."""
        # Сначала регистрируем пользователя
        unique_email = TestUser.generate_unique_email()
        
        register_response = self.user_methods.create_user(
            email=unique_email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        
        assert register_response.status_code == 200
        self.registered_user = unique_email
        
        # Теперь пробуем залогиниться
        login_response = self.user_methods.login_user(
            email=unique_email,
            password=TestUser.VALID_PASSWORD
        )
        
        assert login_response.status_code == 200
        response_data = login_response.json()
        
        assert response_data['success'] == True
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert response_data['user']['email'] == unique_email
        assert response_data['user']['name'] == TestUser.VALID_NAME

    @allure.title('Логин с неправильным паролем')
    def test_login_wrong_password(self):
        """Тест авторизации с неправильным паролем."""
        # Сначала регистрируем пользователя
        unique_email = TestUser.generate_unique_email()
        
        register_response = self.user_methods.create_user(
            email=unique_email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        
        assert register_response.status_code == 200
        self.registered_user = unique_email
        
        # Пробуем залогиниться с неправильным паролем
        login_response = self.user_methods.login_user(
            email=unique_email,
            password="wrong_password"
        )
        
        assert login_response.status_code == 401
        response_data = login_response.json()
        
        assert response_data['success'] == False
        assert response_data['message'] == 'email or password are incorrect'

    @allure.title('Логин с неправильным email')
    def test_login_wrong_email(self):
        """Тест авторизации с неправильным email."""
        # Сначала регистрируем пользователя
        unique_email = TestUser.generate_unique_email()
        
        register_response = self.user_methods.create_user(
            email=unique_email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        
        assert register_response.status_code == 200
        self.registered_user = unique_email
        
        # Пробуем залогиниться с неправильным email
        login_response = self.user_methods.login_user(
            email="wrong_email@yandex.ru",
            password=TestUser.VALID_PASSWORD
        )
        
        assert login_response.status_code == 401
        response_data = login_response.json()
        
        assert response_data['success'] == False
        assert response_data['message'] == 'email or password are incorrect'

    @allure.title('Логин без пароля')
    def test_login_missing_password(self):
        """Тест авторизации без пароля."""
        login_response = self.user_methods.login_user(
            email=TestUser.generate_unique_email(),
            password=""
        )
        
        assert login_response.status_code == 401
        response_data = login_response.json()
        
        assert response_data['success'] == False
        assert response_data['message'] == 'email or password are incorrect'

    @allure.title('Логин без email')
    def test_login_missing_email(self):
        """Тест авторизации без email."""
        login_response = self.user_methods.login_user(
            email="",
            password=TestUser.VALID_PASSWORD
        )
        
        assert login_response.status_code == 401
        response_data = login_response.json()
        
        assert response_data['success'] == False
        assert response_data['message'] == 'email or password are incorrect'

    @allure.title('Логин незарегистрированного пользователя')
    def test_login_unregistered_user(self):
        """Тест авторизации незарегистрированного пользователя."""
        login_response = self.user_methods.login_user(
            email="unregistered_user@yandex.ru",
            password=TestUser.VALID_PASSWORD
        )
        
        assert login_response.status_code == 401
        response_data = login_response.json()
        
        assert response_data['success'] == False
        assert response_data['message'] == 'email or password are incorrect'