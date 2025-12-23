from playwright.sync_api import Page, expect
from .base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.locator('.title')
        # ИСПРАВЛЕНО: используем правильный селектор
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.burger_menu = page.locator('#react-burger-menu-btn')
        self.logout_button = page.locator('#logout_sidebar_link')
    
    def is_loaded(self) -> bool:
        """Проверка, что страница инвентаря загружена"""
        try:
            # Ждем загрузки страницы
            self.page.wait_for_load_state('domcontentloaded')
            
            # Ждем появления ключевых элементов
            self.title.wait_for(state='visible', timeout=10000)
            self.inventory_container.wait_for(state='visible', timeout=10000)
            
            # ИСПРАВЛЕНО: is_visible вместо is_vizible
            return self.title.is_visible() and self.inventory_container.is_visible()
        except Exception as e:
            print(f"Ошибка при загрузке страницы инвентаря: {e}")
            return False
    
    def get_page_title(self) -> str:
        """Получение заголовка страницы"""
        return self.title.text_content()
    
    def logout(self):
        """Выполнение логаута"""
        self.burger_menu.click()
        self.logout_button.click()
    
    def get_product_count(self) -> int:
        """Получение количества товаров на странице"""
        return self.page.locator('.inventory_item').count()