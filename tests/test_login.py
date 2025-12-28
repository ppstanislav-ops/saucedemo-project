import pytest
import yaml
import os
from datetime import datetime

# Загрузка конфигурации
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)


@pytest.mark.parametrize("user_type, expected_success, expected_error", [
    ("standard_user", True, None),
    ("invalid_user", False, "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", False, "Epic sadface: Sorry, this user has been locked out."),
    ("empty_fields", False, "Epic sadface: Username is required"),
    ("problem_user", True, None),
    ("performance_glitch_user", True, None),
])
def test_login_scenarios(page, user_type, expected_success, expected_error):
    """
    Параметризованный тест для проверки различных сценариев логина
    """
    # Инициализация страницы
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.navigate()

    # Обработка пустых полей
    if user_type == "empty_fields":
        login_page.login("", "")
    else:
        user = config['users'][user_type]
        login_page.login(user['username'], user['password'])

    # Проверка результата
    if expected_success:
        assert login_page.is_logged_in(), "Ожидается успешный вход"

        # Дополнительная проверка для пользователей с проблемами производительности
        if user_type in ["problem_user", "performance_glitch_user"]:
            # Ждём полной загрузки страницы
            try:
                start_time = datetime.now()
                page.wait_for_load_state("load", timeout=15000)  # Увеличенный таймаут
                load_duration = (datetime.now() - start_time).total_seconds()
                
                # Логируем время загрузки (можно убрать, если не нужно)
                print(f"Страница загружалась: {load_duration:.2f} секунд")

                # Опционально: добавить ограничение по времени
                # assert load_duration < 8, f"Слишком долгая загрузка: {load_duration:.2f}s"
            except Exception as e:
                pytest.fail(f"Ошибка при ожидании загрузки страницы: {e}")

    else:
        error_msg = login_page.get_error_message()
        assert error_msg is not None, "Ожидалось сообщение об ошибке"
        assert expected_error in error_msg, f"Ожидалось: '{expected_error}', получено: '{error_msg}'"