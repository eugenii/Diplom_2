import pytest

# @pytest.fixture
# def courier_fixture():
#     """Фикстура создаёт курьера и возвращает его данные, затем удаляет после завершения теста."""
#     # Генерируем данные для курьера
#     login, password, firstname = register_new_courier_and_return_login_password()
#     courier_methods = CourierMethods()

#     # Отправляем запрос на создание курьера
#     response = courier_methods.create_courier(login, password, firstname)
#     # if response[0] != 201:  # Если курьер не создан
#     #     pytest.fail(f"Не удалось создать курьера. Ответ сервера: {response[1]}")

#     yield login, password, firstname, response

#     # Удаляем курьера после завершения теста
#     try:
#         courier_id = courier_methods.get_courier_id(login, password)
#         if courier_id:
#             # print(f"Удаляем курьера с ID={courier_id}")
#             courier_methods.delete_courier(courier_id)
#         else:
#             print("Курьер не найден для удаления.")
#     except Exception as e:
#         print(f"Ошибка при удалении курьера: {e}")