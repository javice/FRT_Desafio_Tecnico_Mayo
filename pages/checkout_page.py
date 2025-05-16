# pages/checkout_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.config import Locators

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = Locators.CHECKOUT

    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Completa el formulario de información de checkout"""
        self.find_element(self.locators["first_name"]["id"], By.ID).send_keys(first_name)
        self.find_element(self.locators["last_name"]["id"], By.ID).send_keys(last_name)
        self.find_element(self.locators["postal_code"]["id"], By.ID).send_keys(postal_code)
        self.find_element(self.locators["continue_button"]["id"], By.ID).click()

    def get_summary_info(self):
        """Obtiene la información del resumen de compra"""
        item_total = self.find_element(self.locators["summary"]["item_total"]["class"], By.CLASS_NAME).text
        tax = self.find_element(self.locators["summary"]["tax"]["class"], By.CLASS_NAME).text
        total = self.find_element(self.locators["summary"]["total"]["class"], By.CLASS_NAME).text
        return {
            "item_total": item_total,
            "tax": tax,
            "total": total
        }

    def complete_purchase(self):
        """Completa la compra"""
        self.find_element(self.locators["finish_button"]["id"], By.ID).click()

    def is_purchase_successful(self):
        """Verifica si la compra fue exitosa"""
        complete_header = self.find_element(self.locators["complete_header"]["class"], By.CLASS_NAME)
        return "Thank you for your order" in complete_header.text