import random
import string
import time

# Базовые URL API
BASE_URL = "https://stellarburgers.education-services.ru/api"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
USER_URL = f"{BASE_URL}/auth/user"
ORDERS_URL = f"{BASE_URL}/orders"
INGREDIENTS_URL = f"{BASE_URL}/ingredients"
PASSWORD_RESET_URL = f"{BASE_URL}/password-reset"
LOGOUT_URL = f"{BASE_URL}/auth/logout"
TOKEN_URL = f"{BASE_URL}/auth/token"

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

class TestOrder:
    VALID_INGREDIENTS = ["60d3463f7034a000269f45e7", "60d3463f7034a000269f45e9"]
    INVALID_INGREDIENTS = ["invalid_ingredient_id_123", "another_invalid_id_456"]
    EMPTY_INGREDIENTS = []