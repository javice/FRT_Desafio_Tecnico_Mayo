# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Environment, TestData, get_chrome_options
import os
import allure

@pytest.fixture(scope="function")
def setup_driver(request):
    """
    Fixture principal para configurar el WebDriver
    """
    driver = webdriver.Chrome(options=get_chrome_options())
    driver.implicitly_wait(TestData.IMPLICIT_WAIT)

    # Configurar wait explícito
    wait = WebDriverWait(driver, TestData.EXPLICIT_WAIT)

    # Obtener configuración del ambiente
    env_config = Environment.get_environment_config()

    # Adjuntar a la clase de test
    request.cls.driver = driver
    request.cls.wait = wait
    request.cls.env_config = env_config

    yield driver

    # Capturar screenshot en caso de fallo
    if request.node.rep_call.failed:
        take_screenshot(driver, request.node.name)

    driver.quit()

def take_screenshot(driver, name):
    """Utilidad para tomar screenshots"""
    os.makedirs(TestData.SCREENSHOTS_PATH, exist_ok=True)
    screenshot_path = f"{TestData.SCREENSHOTS_PATH}/failure_{name}.png"
    driver.save_screenshot(screenshot_path)
    allure.attach.file(
        screenshot_path,
        name="Screenshot",
        attachment_type=allure.attachment_type.PNG
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar el estado de la prueba
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)