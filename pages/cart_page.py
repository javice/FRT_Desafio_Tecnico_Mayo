# pages/cart_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.config import Locators

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = Locators.CART

    def get_cart_items(self):
        """Retorna una lista de diccionarios con nombre y precio de cada item"""
        items = []
        cart_items = self.driver.find_elements(By.CLASS_NAME, self.locators["cart_item"]["class"])

        for item in cart_items:
            name = item.find_element(By.CLASS_NAME, self.locators["item_name"]["class"]).text
            price = item.find_element(By.CLASS_NAME, self.locators["item_price"]["class"]).text
            items.append({"name": name, "price": price})

        return items

    def remove_item(self, item_name):
        """Elimina un item específico del carrito"""
        cart_items = self.driver.find_elements(By.CLASS_NAME, self.locators["cart_item"]["class"])
        for item in cart_items:
            name = item.find_element(By.CLASS_NAME, self.locators["item_name"]["class"]).text
            if name.lower() == item_name.lower():
                remove_button = item.find_element(By.CSS_SELECTOR, self.locators["remove_button"]["css"])
                remove_button.click()
                return True
        return False

    def proceed_to_checkout(self):
        """Procede al checkout"""
        checkout_button = self.find_element(self.locators["checkout_button"]["id"], By.ID)
        checkout_button.click()