import random
import string
import time
# Базовые URL API
BASE_URL = "https://stellarburgers.nomoreparties.site/api"  # Базовый URL API
REGISTER_URL = f"{BASE_URL}/auth/register"  # URL для регистрации пользователя
LOGIN_URL = f"{BASE_URL}/auth/login"  # URL для авторизации пользователя
USER_URL = f"{BASE_URL}/auth/user"  # URL для работы с данными пользователя 

# Тестовые данные пользователей


class TestUser:
    VALID_PASSWORD = "securepassword123" 
    VALID_NAME = "Test User"
    NEW_EMAIL = "updated_user@yandex.ru"
    NEW_PASSWORD = "newpassword123"
    NEW_NAME = "Updated User"
    
    @staticmethod
    def generate_unique_email():
        """Генерация действительно уникального email"""
        timestamp = int(time.time() * 1000)
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"test_{timestamp}_{random_suffix}@yandex.ru"