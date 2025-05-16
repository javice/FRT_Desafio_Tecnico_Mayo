# tests/test_checkout.py
import allure
import pytest
from typing import Dict
from selenium import webdriver
from config.config import TestData, Environment, get_chrome_options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


@allure.epic("Sauce Demo Testing")
@allure.feature("Checkout Process")
class TestCheckout:
    driver: WebDriver
    wait: WebDriverWait
    env_config: dict
    login_page: LoginPage
    inventory_page: InventoryPage
    cart_page: CartPage
    checkout_page: CheckoutPage

    @pytest.fixture(autouse=True)
    def setup(self, setup_driver):
        """Configuración inicial de la prueba"""
        self.driver = setup_driver
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)

        # Navegar y hacer login
        self.driver.get(Environment.get_environment_config()["url"])
        self.login_page.login(
            username=Environment.ENVIRONMENTS["dev"]["username"],
            password=Environment.ENVIRONMENTS["dev"]["password"]
        )


    def log_purchase_summary(self, summary: Dict[str, str]):
        """
        Registra el resumen de la compra en Allure
        Args:
            summary (Dict[str, str]): Información del resumen de compra
        """
        allure.attach(
            '\n'.join(f"{key}: {value}" for key, value in summary.items()),
            'Resumen de compra',
            allure.attachment_type.TEXT
        )

    @allure.story("Proceso de checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("customer_info,items", [
        (
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "postal_code": "12345"
                },
                ["Sauce Labs Backpack"]
        ),
        (
                {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "postal_code": "54321"
                },
                ["Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        )
    ])
    def test_checkout_process(self, customer_info: Dict[str, str], items: list):
        """
        Prueba el proceso completo de checkout
        Args:
            customer_info (Dict[str, str]): Información del cliente
            items (list): Lista de items a comprar
        """
        with allure.step("Agregar items al carrito"):
            for item in items:
                assert self.inventory_page.add_item_to_cart(item), \
                    f"No se pudo agregar el item: {item}"
                allure.attach(
                    f"Item agregado: {item}",
                    'Agregar al carrito',
                    allure.attachment_type.TEXT
                )
            self.inventory_page.go_to_cart()

        with allure.step("Iniciar checkout"):
            self.cart_page.proceed_to_checkout()

        with allure.step("Completar información de envío"):
            self.checkout_page.fill_checkout_info(**customer_info)
            """
            allure.attach(
                str(customer_info),
                'Información del cliente',
                allure.attachment_type.TEXT
            )
            """

        with allure.step("Verificar resumen de compra"):
            summary = self.checkout_page.get_summary_info()
            self.log_purchase_summary(summary)
            assert "$" in summary["total"], "El total no incluye el símbolo de dólar"

        with allure.step("Completar compra"):
            self.checkout_page.complete_purchase()
            assert self.checkout_page.is_purchase_successful(), \
                "La compra no se completó exitosamente"