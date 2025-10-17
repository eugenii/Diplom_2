import allure
import pytest

from methods.user_methods import UserMethods
from data import TestUser


class TestUserUpdate:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_methods = UserMethods()

    @pytest.fixture
    def registered_user(self):
        """Фикстура для зарегистрированного пользователя"""
        email = TestUser.generate_unique_email()
        
        register_response = self.user_methods.create_user(
            email=email,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        
        assert register_response.status_code == 200
        register_data = register_response.json()
        auth_token = register_data['accessToken']
        
        yield email, auth_token
        
        # Очистка после теста
        delete_response = self.user_methods.delete_user(auth_token)
        if delete_response and delete_response.status_code in [200, 202]:
            print(f"Пользователь {email} удалён")

    @pytest.fixture
    def auth_token(self, registered_user):
        """Фикстура для токена авторизации"""
        email, token = registered_user
        return token

    @allure.title('Обновление email авторизованного пользователя')
    def test_update_user_email_with_auth(self, registered_user):
        """Тест обновления email авторизованного пользователя."""
        email, auth_token = registered_user
        
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
    def test_update_user_name_with_auth(self, registered_user):
        """Тест обновления name авторизованного пользователя."""
        email, auth_token = registered_user
        
        # Обновляем name
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token,
            name=TestUser.NEW_NAME
        )
        
        assert update_response.status_code == 200
        update_data = update_response.json()
        
        assert update_data['success'] == True
        assert update_data['user']['email'] == email  # Email не должен измениться
        assert update_data['user']['name'] == TestUser.NEW_NAME

    @allure.title('Обновление password авторизованного пользователя')
    def test_update_user_password_with_auth(self, registered_user):
        """Тест обновления password авторизованного пользователя."""
        email, auth_token = registered_user
        
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
            email=email,
            password=TestUser.NEW_PASSWORD
        )
        
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert login_data['success'] == True

    @allure.title('Обновление всех полей авторизованного пользователя')
    def test_update_all_user_fields_with_auth(self, registered_user):
        """Тест одновременного обновления всех полей авторизованного пользователя."""
        email, auth_token = registered_user
        
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
    def test_update_user_to_existing_email(self, registered_user):
        """Тест обновления email на уже существующий в системе."""
        # Первый пользователь из фикстуры
        email1, auth_token1 = registered_user
        
        # Создаем второго пользователя
        email2 = TestUser.generate_unique_email()
        register_response2 = self.user_methods.create_user(
            email=email2,
            password=TestUser.VALID_PASSWORD,
            name=TestUser.VALID_NAME
        )
        assert register_response2.status_code == 200
        
        # Получаем токен второго пользователя для очистки
        register_data2 = register_response2.json()
        auth_token2 = register_data2['accessToken']
        
        # Пытаемся обновить email первого пользователя на email второго пользователя
        update_response = self.user_methods.update_user_data(
            auth_token=auth_token1,
            email=email2
        )
        
        assert update_response.status_code == 403
        update_data = update_response.json()
        
        assert update_data['success'] == False
        assert update_data['message'] == 'User with such email already exists'
        
        # Удаляем второго пользователя
        self.user_methods.delete_user(auth_token2)

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
    def test_get_user_data_with_auth(self, registered_user):
        """Тест получения данных пользователя с авторизацией."""
        email, auth_token = registered_user
        
        # Получаем данные пользователя
        get_response = self.user_methods.get_user_data(auth_token=auth_token)
        
        assert get_response.status_code == 200
        get_data = get_response.json()
        
        assert get_data['success'] == True
        assert get_data['user']['email'] == email
        assert get_data['user']['name'] == TestUser.VALID_NAME