# tests/test_login.py
import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from typing import Tuple
from config.config import TestData, Environment, get_chrome_options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import os

@allure.epic("Sauce Demo Testing")
@allure.feature("Authentication")
class TestLogin:
    driver: WebDriver
    wait: WebDriverWait
    env_config: dict
    login_page: LoginPage
    inventory_page: InventoryPage

    @pytest.fixture(autouse=True)
    def setup(self, setup_driver):
        """Configurar pages objects"""
        self.driver = setup_driver
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.driver.get(Environment.get_environment_config()["url"])

    @allure.story("Intentos de login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("test_case,credentials,expected_message,should_succeed", [
        ("Login exitoso",
         {"username": Environment.ENVIRONMENTS["dev"]["username"],
          "password": Environment.ENVIRONMENTS["dev"]["password"]},
         None, True),
        ("Login inválido",
         {"username": "invalid_user", "password": "invalid_password"},
         TestData.ERROR_MESSAGES["login_error"], False),
        ("Usuario bloqueado",
         {"username": "locked_out_user",
          "password": Environment.ENVIRONMENTS["dev"]["password"]},
         TestData.ERROR_MESSAGES["locked_user"], False)
    ])
    def test_login_scenarios(self, test_case: str, credentials: dict,
                             expected_message: str, should_succeed: bool):
        """
        Prueba diferentes escenarios de login
        Args:
            test_case (str): Descripción del caso de prueba
            credentials (dict): Credenciales a usar
            expected_message (str): Mensaje de error esperado si aplica
            should_succeed (bool): Si se espera que el login sea exitoso
        """
        with allure.step(f"Ejecutar {test_case}"):
            self.login_page.login(**credentials)

            if should_succeed:
                with allure.step("Verificar login exitoso"):
                    assert self.inventory_page.verify_cart_icon(), \
                        "El ícono del carrito no está visible después del login"
            else:
                with allure.step("Verificar mensaje de error"):
                    actual_message = self.login_page.get_error_message()
                    allure.attach(
                        f"Mensaje esperado: {expected_message}\n" +
                        f"Mensaje actual: {actual_message}",
                        'Verificación de mensaje de error',
                        allure.attachment_type.TEXT
                    )
                    assert actual_message == expected_message, \
                        "El mensaje de error no coincide con el esperado"