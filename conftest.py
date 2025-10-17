import pytest
import allure

from methods.user_methods import UserMethods
from data import TestUser

@pytest.fixture
def registered_user():
    """Фикстура создаёт пользователя и возвращает его данные, затем удаляет после завершения теста."""
    user_methods = UserMethods()
    
    # Генерируем данные для пользователя
    email = TestUser.generate_unique_email()
    password = TestUser.VALID_PASSWORD
    name = TestUser.VALID_NAME
    
    # Регистрируем пользователя
    response = user_methods.create_user(email, password, name)
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя. Ответ сервера: {response.status_code} - {response.text}")
    
    response_data = response.json()
    auth_token = response_data['accessToken']
    
    yield email, password, name, auth_token
    
    # Здесь можно добавить удаление пользователя, если API поддерживает эту функцию
    # В текущем API нет эндпоинта для удаления пользователя, поэтому просто завершаем
    print(f"Тестовый пользователь {email} завершил работу")

@pytest.fixture
def auth_token():
    """Фикстура возвращает токен авторизации для зарегистрированного пользователя."""
    user_methods = UserMethods()
    
    email = TestUser.generate_unique_email()
    password = TestUser.VALID_PASSWORD
    name = TestUser.VALID_NAME
    
    # Регистрируем пользователя
    response = user_methods.create_user(email, password, name)
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя. Ответ сервера: {response.status_code}")
    
    response_data = response.json()
    token = response_data['accessToken']
    
    yield token

    delete_response = user_methods.delete_user(token)
    if delete_response and delete_response.status_code == 200:
        print(f"Тестовый пользователь {email} успешно удалён")
    else:
        print(f"Не удалось удалить тестового пользователя {email}")