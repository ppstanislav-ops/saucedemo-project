import pytest
import allure
from playwright.sync_api import expect
from utils.config import Config


@allure.epic("Авторизация")
@allure.feature("Логин")
class TestLogin:
    
    @allure.story('Успешный логин')
    @allure.title('Успешная авторизация с корректными данными')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, login_page, inventory_page):
        '''Тест: Успешный логин с корректными данными'''
        with allure.step('1. Открыть страницу логина'):
            login_page.load()
            assert login_page.is_loaded()

        with allure.step('2. Ввести корректные данные пользователя'):
            user = Config.STANDARD_USER
            login_page.login(user['username'], user['password'])

        with allure.step('3. Проверить успешный логин'):
            # Ждем перехода на страницу инвентаря
            inventory_page.page.wait_for_url(f"{Config.BASE_URL}inventory.html", timeout=10000)

            # Ждем видимости элементов
            inventory_page.title.wait_for(state='visible', timeout=10000)
            inventory_page.inventory_container.wait_for(state='visible', timeout=10000)

            assert inventory_page.is_loaded()

            expect(inventory_page.page).to_have_url(f"{Config.BASE_URL}inventory.html")

            # Проверка заголовка
            page_title = inventory_page.get_page_title()
            assert 'Products' in page_title, f'Ожидалось "Products" в заголовке, получил: {page_title}'

            # Проверка количества товаров
            product_count = inventory_page.get_product_count()
            assert product_count > 0, f'На странице должно быть товаров больше 0, получил: {product_count}'

    @allure.story("Неверный пароль")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_password(self, login_page):
        """
        Тест: Логин с неверным паролем
        Ожидаемый результат: Сообщение об ошибке
        """
        with allure.step("1. Открыть страницу логина"):
            login_page.load()
        
        with allure.step("2. Ввести корректный логин и неверный пароль"):
            login_page.login(Config.STANDARD_USER["username"], "wrong_password")
        
        with allure.step("3. Проверить сообщение об ошибке"):
            assert login_page.has_error_message()
            error_text = login_page.get_error_message()
            assert "Username and password do not match" in error_text
    
    @allure.story("Заблокированный пользователь")
    @allure.title("Логин заблокированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_locked_out_user(self, login_page):
        """
        Тест: Логин заблокированного пользователя
        Ожидаемый результат: Сообщение о блокировке пользователя
        """
        with allure.step("1. Открыть страницу логина"):
            login_page.load()
        
        with allure.step("2. Ввести данные заблокированного пользователя"):
            user = Config.LOCKED_OUT_USER
            login_page.login(user["username"], user["password"])
        
        with allure.step("3. Проверить сообщение о блокировке"):
            assert login_page.has_error_message()
            error_text = login_page.get_error_message()
            assert "Sorry, this user has been locked out" in error_text
    
    @allure.story("Пустые поля")
    @allure.title("Логин с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_fields(self, login_page):
        """
        Тест: Логин с пустыми полями
        Ожидаемый результат: Сообщение о необходимости ввести данные
        """
        with allure.step("1. Открыть страницу логина"):
            login_page.load()
        
        with allure.step("2. Нажать кнопку логина без ввода данных"):
            login_page.login_button.click()
        
        with allure.step("3. Проверить сообщение об ошибке"):
            assert login_page.has_error_message()
            error_text = login_page.get_error_message()
            assert "Username is required" in error_text
    
    @allure.story("Пользователь с задержками")
    @allure.title("Логин пользователем performance_glitch_user")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.performance
    def test_performance_glitch_user(self, login_page, inventory_page):
        """
        Тест: Логин пользователем с возможными задержками
        Ожидаемый результат: Успешный логин, несмотря на задержки
        """
        with allure.step("1. Открыть страницу логина"):
            login_page.load()
        
        with allure.step("2. Ввести данные пользователя performance_glitch_user"):
            user = Config.PERFORMANCE_GLITCH_USER
            login_page.login(user["username"], user["password"])
        
        with allure.step("3. Проверить успешный логин (с увеличенным таймаутом)"):
            # Увеличиваем таймаут для пользователя с задержками
            inventory_page.page.wait_for_url(
                f"{Config.BASE_URL}inventory.html",
                timeout=30000  # 30 секунд
            )
            
            # Ждем загрузки страницы
            assert inventory_page.is_loaded(), "Страница инвентаря не загрузилась"
            
            # Проверяем URL
            expect(inventory_page.page).to_have_url(f"{Config.BASE_URL}inventory.html")
            
            # Проверяем заголовок
            page_title = inventory_page.get_page_title()
            assert 'Products' in page_title, f'Ожидалось "Products" в заголовке, получил: {page_title}'
            
            # Проверяем наличие товаров
            product_count = inventory_page.get_product_count()
            assert product_count > 0, f'На странице должно быть товаров больше 0, получил: {product_count}'
            