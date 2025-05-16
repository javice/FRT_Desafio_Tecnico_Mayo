# tests/test_cart.py
import allure
import pytest
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from config.config import TestData, Environment, get_chrome_options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@allure.epic("Sauce Demo Testing")
@allure.feature("Shopping Cart")
class TestCart:
    driver: WebDriver
    wait: WebDriverWait
    env_config: dict
    login_page: LoginPage
    inventory_page: InventoryPage
    cart_page: CartPage

    @pytest.fixture(autouse=True)
    def setup(self, setup_driver):
        """Configuración inicial de la prueba"""
        self.driver = setup_driver
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)

        # Navegar y hacer login
        self.driver.get(Environment.get_environment_config()["url"])
        self.login_page.login(
            username=Environment.ENVIRONMENTS["dev"]["username"],
            password=Environment.ENVIRONMENTS["dev"]["password"]
        )

    def log_cart_state(self, items: List[dict], description: str):
        """
        Registra el estado actual del carrito en Allure
        Args:
            items (List[dict]): Items en el carrito
            description (str): Descripción del estado
        """
        content = "Carrito vacío" if not items else \
            '\n'.join(f"Item: {item['name']}, Precio: {item['price']}"
                      for item in items)
        allure.attach(
            content,
            description,
            allure.attachment_type.TEXT
        )

    @allure.story("Operaciones del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("test_case,items,action", [
        (
                "Agregar un item",
                ["Sauce Labs Backpack"],
                "add"
        ),
        (
                "Agregar múltiples items",
                ["Sauce Labs Backpack", "Sauce Labs Bike Light"],
                "add"
        ),
        (
                "Remover items",
                ["Sauce Labs Backpack"],
                "remove"
        )
    ])
    def test_cart_operations(self, test_case: str, items: List[str], action: str):
        """
        Prueba operaciones del carrito
        Args:
            test_case (str): Descripción del caso de prueba
            items (List[str]): Lista de items para la operación
            action (str): Tipo de operación ('add' o 'remove')
        """
        with allure.step(f"Ejecutar {test_case}"):
            if action == "add":
                for item in items:
                    assert self.inventory_page.add_item_to_cart(item), \
                        f"No se pudo agregar el item: {item}"
                self.inventory_page.go_to_cart()

                cart_items = self.cart_page.get_cart_items()
                self.log_cart_state(cart_items, "Estado del carrito después de agregar")
                assert len(cart_items) == len(items), \
                    f"Número incorrecto de items en el carrito"

            elif action == "remove":
                # Primero añadimos los items
                for item in items:
                    self.inventory_page.add_item_to_cart(item)
                self.inventory_page.go_to_cart()

                # Luego los removemos
                for item in items:
                    assert self.cart_page.remove_item(item), \
                        f"No se pudo remover el item: {item}"

                cart_items = self.cart_page.get_cart_items()
                self.log_cart_state(cart_items, "Estado del carrito después de remover")
                assert len(cart_items) == 0, "El carrito debería estar vacío"