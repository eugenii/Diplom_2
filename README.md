# API Tests for Stellar Burgers

Этот проект содержит автоматизированные тесты для API Stellar Burgers.

## Структура проекта
DIPLOM_2/
├── methods/
│ ├── init.py
│ ├── order_methods.py
│ └── user_methods.py
├── tests/
│ ├── init.py
│ ├── test_orders.py
│ ├── test_user_login.py
│ ├── test_user_registration.py
│ └── test_user_update.py
├── conftest.py
├── data.py
├── requirements.txt
└── README.md


## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt

2. Запустите тесты:
```bash
pytest
```. Установите зависимости:
pytest tests/ -v

3. Тесты с генерацией отчёта:

pytest tests/ --alluredir=allure-results

4. просмотреть отчет:

allure serve allure-results

