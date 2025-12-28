from playwright.sync_api import Page
import yaml
import os

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.page.goto(config['base_url'])

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.text_content() if self.error_message.is_visible() else None

    def is_logged_in(self):
        return self.page.url.endswith("/inventory.html")