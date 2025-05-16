# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

from config.config import Locators

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Obtenemos los locators del diccionario
        self.username_input = Locators.LOGIN["username_input"]
        self.password_input = Locators.LOGIN["password_input"]
        self.login_button = Locators.LOGIN["login_button"]
        self.ERROR_MESSAGE = "[data-test='error']"


    def login(self, username, password):
        # Usando el método más óptimo (ID)
        username_field = self.find_element(
            self.username_input["id"],
            By.ID
        )
        username_field.send_keys(username)

        password_field = self.find_element(
            self.password_input["id"],
            By.ID
        )
        password_field.send_keys(password)

        login_button = self.find_element(
            self.login_button["id"],
            By.ID
        )
        login_button.click()


    def get_error_message(self):
        """Obtiene el mensaje de error del login"""
        error_element = self.find_element(self.ERROR_MESSAGE, By.CSS_SELECTOR)
        return error_element.text
