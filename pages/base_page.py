from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000
    
    def navigate(self, url: str):
        """Переход по URL"""
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Получение заголовка страницы"""
        return self.page.title()
    
    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.page.url
    
    def wait_for_url(self, url: str, timeout: int = None):
        """Ожидание URL"""
        timeout = timeout or self.timeout
        self.page.wait_for_url(url, timeout=timeout)
    
    def take_screenshot(self, name: str):
        """Скриншот страницы"""
        self.page.screenshot(path=f"screenshots/{name}.png")