from playwright.sync_api import Page, expect
from .base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('#user-name')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login-button')
        self.error_message = page.locator('[data-test=\"error\"]')
    
    def load(self):
        '''Загрузка страницы логина'''
        self.navigate(Config.BASE_URL)
        return self
    
    def is_loaded(self) -> bool:
        '''Проверка, что страница логина загружена'''
        return self.login_button.is_visible()
    
    def login(self, username: str, password: str):
        '''Выполнение логина'''
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def get_error_message(self) -> str:
        '''Получение текста ошибки'''
        return self.error_message.text_content()
    
    def has_error_message(self) -> bool:
        '''Проверка наличия сообщения об ошибке'''
        return self.error_message.is_visible()
    
    def clear_fields(self):
        '''Очистка полей ввода'''
        self.username_input.clear()
        self.password_input.clear()
