# config/config.py

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os



class TestData:
    # Configuración del navegador
    BROWSER = "chrome"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'

    # URL y credenciales
    BASE_URL = "https://www.saucedemo.com"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"

    # Configuración de reportes
    REPORTS_PATH = "reports"
    SCREENSHOTS_PATH = "reports/screenshots"

    # Mensajes de error personalizados
    ERROR_MESSAGES = {
        "login_error": "Epic sadface: Username and password do not match any user in this service",
        "locked_user": "Epic sadface: Sorry, this user has been locked out."
    }


class Locators:
    """
    Proporciona una colección centralizada de definiciones de localizadores
    para elementos en las diferentes páginas de la aplicación. Estos localizadores
    pueden ser utilizados para identificar elementos en páginas web durante
    las pruebas automatizadas.

    Esta clase está organizada en diccionarios que representan distintas
    secciones o páginas de la aplicación, como la Página de Login y la
    Página de Inventario. Cada diccionario contiene localizadores para
    los elementos de la página respectiva usando tres métodos principales:

    1. ID:
    Ventajas:
    ✅ Mejor rendimiento en tiempo de ejecución
    ✅ Garantiza unicidad en el DOM
    ✅ Menor probabilidad de cambios durante actualizaciones
    ✅ Sintaxis simple y directa
    Inconvenientes:
    ❌ No siempre está disponible en todos los elementos
    ❌ Puede cambiar en implementaciones dinámicas

    2. CSS Selector:
    Ventajas:
    ✅ Mayor flexibilidad que ID
    ✅ Mejor rendimiento que XPath
    ✅ Soporta selección por múltiples atributos
    ✅ Sintaxis más concisa
    Inconvenientes:
    ❌ Puede ser afectado por cambios en el estilo
    ❌ No puede navegar hacia elementos padres

    3. XPath:
    Ventajas:
    ✅ Máxima flexibilidad en la navegación del DOM
    ✅ Puede localizar elementos sin atributos
    ✅ Soporta búsquedas complejas y condicionales
    Inconvenientes:
    ❌ Rendimiento más lento
    ❌ Sintaxis más compleja
    ❌ Muy sensible a cambios en la estructura HTML

    Este enfoque de múltiples métodos asegura una mejor mantenibilidad y
    adaptabilidad de los localizadores para los diversos flujos de automatización,
    permitiendo elegir el metodo más apropiado según el contexto y las
    características del elemento a localizar.
    """
    # Login Page
    LOGIN = {
        "username_input": {
            "id": "user-name",
            "css": "input[data-test='username']",
            "xpath": "//input[@id='user-name']"
        },
        "password_input": {
            "id": "password",
            "css": "input[data-test='password']",
            "xpath": "//input[@id='password']"
        },
        "login_button": {
            "id": "login-button",
            "css": "input[type='submit']",
            "xpath": "//input[@value='Login']"
        }
    }

    # Inventory Page
    INVENTORY = {
        "cart_icon": {
            "id": "shopping_cart_container",
            "css": ".shopping_cart_link",
            "xpath": "//a[@class='shopping_cart_link']"
        },
        "menu_button": {
            "id": "react-burger-menu-btn",
            "css": "#react-burger-menu-btn",
            "xpath": "//button[@id='react-burger-menu-btn']"
        }
    }
    # Cart Page
    CART = {
        "cart_item": {
            "class": "cart_item",
            "css": ".cart_item",
            "xpath": "//div[@class='cart_item']"
        },
        "item_name": {
            "class": "inventory_item_name",
            "css": ".inventory_item_name",
            "xpath": "//div[@class='inventory_item_name']"
        },
        "item_price": {
            "class": "inventory_item_price",
            "css": ".inventory_item_price",
            "xpath": "//div[@class='inventory_item_price']"
        },
        "checkout_button": {
            "id": "checkout",
            "css": "#checkout",
            "xpath": "//button[@id='checkout']"
        },
        "remove_button": {
            "css": "button[id^='remove-']",
            "xpath": "//button[starts-with(@id, 'remove-')]"
        }
    }

    # Checkout Page
    CHECKOUT = {
        "first_name": {
            "id": "first-name",
            "css": "#first-name",
            "xpath": "//input[@id='first-name']"
        },
        "last_name": {
            "id": "last-name",
            "css": "#last-name",
            "xpath": "//input[@id='last-name']"
        },
        "postal_code": {
            "id": "postal-code",
            "css": "#postal-code",
            "xpath": "//input[@id='postal-code']"
        },
        "continue_button": {
            "id": "continue",
            "css": "#continue",
            "xpath": "//input[@id='continue']"
        },
        "finish_button": {
            "id": "finish",
            "css": "#finish",
            "xpath": "//button[@id='finish']"
        },
        "cancel_button": {
            "id": "cancel",
            "css": "#cancel",
            "xpath": "//button[@id='cancel']"
        },
        "complete_header": {
            "class": "complete-header",
            "css": ".complete-header",
            "xpath": "//h2[@class='complete-header']"
        },
        "summary": {
            "item_total": {
                "class": "summary_subtotal_label",
                "css": ".summary_subtotal_label",
                "xpath": "//div[@class='summary_subtotal_label']"
            },
            "tax": {
                "class": "summary_tax_label",
                "css": ".summary_tax_label",
                "xpath": "//div[@class='summary_tax_label']"
            },
            "total": {
                "class": "summary_total_label",
                "css": ".summary_total_label",
                "xpath": "//div[@class='summary_total_label']"
            }
        }
    }


class Environment:
    # Configuración para diferentes ambientes (desarrollo, pruebas, producción)
    ENVIRONMENTS = {
        "dev": {
            "url": "https://www.saucedemo.com",
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "qa": {
            "url": "https://qa.saucedemo.com",
            "username": "qa_user",
            "password": "qa_password"
        },
        "prod": {
            "url": "https://www.saucedemo.com",
            "username": "standard_user",
            "password": "secret_sauce"
        }
    }

    # Ambiente actual (cambiar según necesidad)
    CURRENT_ENV = "dev"

    @classmethod
    def get_environment_config(cls):
        """Retorna la configuración del ambiente actual"""
        return cls.ENVIRONMENTS[cls.CURRENT_ENV]

def get_chrome_options():
    """
    Configuración optimizada para Chrome
    Returns:
        Options: Opciones configuradas para Chrome
    """
    options = Options()

    # Configuración básica
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')

    # Configuración para modo headless
    if TestData.HEADLESS:
        options.add_argument('--headless=new')  # Nueva sintaxis para Chrome
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')


    # Deshabilitar gestor de contraseñas y notificaciones
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.default_content_setting_values.notifications': 2
    })

    # Deshabilitar mensajes de automatización
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    return options
