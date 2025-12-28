import sys
import os

# КРИТИЧЕСКО ВАЖНО: Добавляем корневую директорию в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import pytest
from playwright.sync_api import Page
import allure
from datetime import datetime

# Теперь импорты должны работать
try:
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from utils.config import Config
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print(f"Текущая директория: {current_dir}")
    print(f"Содержимое директории: {os.listdir(current_dir)}")
    raise


@pytest.fixture
def page_context(playwright):
    """Фикстура для создания контекста браузера"""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
    browser.close()


@pytest.fixture
def login_page(page_context: Page):
    """Фикстура для страницы логина"""
    return LoginPage(page_context)


@pytest.fixture
def inventory_page(page_context: Page):
    """Фикстура для страницы инвентаря"""
    return InventoryPage(page_context)


# ============== Хук для скриншотов при падении ==============
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для прикрепления скриншотов при падении теста
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        try:
            if "page_context" in item.funcargs:
                page = item.funcargs["page_context"]

                # Создаем директорию для скриншотов
                os.makedirs("allure-results/screenshots", exist_ok=True)

                # Снимок экрана
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"allure-results/screenshots/{item.name}_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)

                # Прикрепляем к Allure
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"Не удалось создать скриншот: {e}")


# ============== Динамическое добавление информации в Allure ==============
@pytest.fixture(scope="function", autouse=True)
def attach_test_info(request):
    """Автоматически прикрепляет название и описание теста к Allure"""
    yield

    allure.dynamic.title(request.node.name)
    if request.node.function.__doc__:
        allure.dynamic.description(request.node.function.__doc__)
        