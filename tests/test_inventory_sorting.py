# tests/test_inventory_sorting.py
import allure
import pytest
from typing import List, Tuple, Dict
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config.config import TestData, Environment, get_chrome_options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@allure.epic("Sauce Demo Testing")
@allure.feature("Inventory Management")
class TestInventorySorting:
    driver: WebDriver
    wait: WebDriverWait
    env_config: dict
    login_page: LoginPage
    inventory_page: InventoryPage


    @pytest.fixture(autouse=True)
    def setup(self, setup_driver):
        """Configuración inicial de la prueba"""
        self.driver = setup_driver
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)

        # Navegar y hacer login
        self.driver.get(Environment.get_environment_config()["url"])
        self.login_page.login(
            username=Environment.ENVIRONMENTS["dev"]["username"],
            password=Environment.ENVIRONMENTS["dev"]["password"]
        )


    def get_products_info(self) -> Tuple[List[str], List[float]]:
        """
        Obtiene la información actual de productos y precios
        Returns:
            Tuple[List[str], List[float]]: Tupla con listas de productos y precios
        """
        products = self.inventory_page.get_product_names()
        prices = self.inventory_page.get_product_prices()
        return products, prices

    def log_products_state(self, products: List[str], prices: List[float], description: str):
        """
        Registra el estado actual de productos en Allure
        Args:
            products (List[str]): Lista de nombres de productos
            prices (List[float]): Lista de precios
            description (str): Descripción del estado
        """
        allure.attach(
            '\n'.join(f"{product}: ${price}" for product, price in zip(products, prices)),
            description,
            allure.attachment_type.TEXT
        )

    def verify_sorting(self, current_prices: List[float], expected_prices: List[float],
                       sort_type: str, reverse: bool = False):
        """
        Verifica el ordenamiento de productos
        Args:
            current_prices (List[float]): Precios actuales
            expected_prices (List[float]): Precios esperados
            sort_type (str): Tipo de ordenamiento
            reverse (bool): Si el orden es reverso
        """
        expected = sorted(expected_prices, reverse=reverse)
        is_sorted = current_prices == expected

        allure.attach(
            f"Tipo de ordenamiento: {sort_type}\n" +
            f"¿Están ordenados correctamente?: {is_sorted}\n" +
            f"Secuencia esperada: {expected}\n" +
            f"Secuencia actual: {current_prices}",
            'Verificación de ordenamiento',
            allure.attachment_type.TEXT
        )

        assert is_sorted, f"Los productos no están ordenados correctamente ({sort_type})"

    @allure.story("Ordenamiento de productos por precio")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("sort_option,sort_type,reverse", [
        ('lohi', 'menor a mayor', False),
        ('hilo', 'mayor a menor', True)
    ])
    def test_sort_products_by_price(self, sort_option: str, sort_type: str, reverse: bool):
        """
        Prueba el ordenamiento de productos por precio
        Args:
            sort_option (str): Opción de ordenamiento ('lohi' o 'hilo')
            sort_type (str): Descripción del tipo de ordenamiento
            reverse (bool): Si el orden es reverso
        """
        with allure.step("Obtener lista inicial de productos y precios"):
            initial_products, initial_prices = self.get_products_info()
            self.log_products_state(initial_products, initial_prices, 'Estado inicial de productos')

        with allure.step(f"Ordenar productos por precio ({sort_type})"):
            self.inventory_page.sort_products(sort_option)
            sorted_products, sorted_prices = self.get_products_info()
            self.log_products_state(
                sorted_products,
                sorted_prices,
                f'Productos ordenados por precio ({sort_type})'
            )
            self.verify_sorting(sorted_prices, initial_prices, sort_type, reverse)

    @allure.story("Ordenamiento alfabético de productos")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("sort_option,sort_type,reverse", [
        ('az', 'A a Z', False),
        ('za', 'Z a A', True)
    ])
    def test_sort_products_alphabetically(self, sort_option: str, sort_type: str, reverse: bool):
        """
        Prueba el ordenamiento alfabético de productos
        Args:
            sort_option (str): Opción de ordenamiento ('az' o 'za')
            sort_type (str): Descripción del tipo de ordenamiento
            reverse (bool): Si el orden es reverso
        """
        with allure.step("Obtener lista inicial de productos"):
            initial_products, _ = self.get_products_info()
            allure.attach(
                '\n'.join(initial_products),
                'Lista inicial de productos',
                allure.attachment_type.TEXT
            )

        with allure.step(f"Ordenar productos alfabéticamente ({sort_type})"):
            self.inventory_page.sort_products(sort_option)
            sorted_products, _ = self.get_products_info()

            allure.attach(
                '\n'.join(sorted_products),
                f'Productos ordenados alfabéticamente ({sort_type})',
                allure.attachment_type.TEXT
            )

            expected = sorted(initial_products, reverse=reverse)
            is_sorted = sorted_products == expected

            allure.attach(
                f"¿Están ordenados correctamente?: {is_sorted}\n" +
                f"Secuencia esperada: {expected}\n" +
                f"Secuencia actual: {sorted_products}",
                'Verificación de ordenamiento alfabético',
                allure.attachment_type.TEXT
            )

            assert is_sorted, f"Los productos no están ordenados alfabéticamente ({sort_type})"
