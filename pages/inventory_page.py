# pages/inventory_page.py
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from .base_page import BasePage
from config.config import Locators

class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.cart_icon_locator = Locators.INVENTORY["cart_icon"]


    # Locators para productos
    ADD_TO_CART_PREFIX = "add-to-cart-"
    REMOVE_FROM_CART_PREFIX = "remove-"
    INVENTORY_ITEM_NAME = "inventory_item_name"
    INVENTORY_ITEM_PRICE = "inventory_item_price"
    CART_BADGE = "shopping_cart_badge"

    #Locators para ordenar productos
    SORT_DROPDOWN = "product_sort_container"
    PRODUCT_LABEL = "inventory_item_description"
    PRICE_LABEL = "inventory_item_price"


    def verify_cart_icon(self):
        # Usando el método más óptimo (ID)
        return self.find_element(self.cart_icon_locator["id"],By.ID).is_displayed()

    def add_item_to_cart(self, item_name):
        """Añade un item específico al carrito"""
        items = self.driver.find_elements(By.CLASS_NAME, self.INVENTORY_ITEM_NAME)
        for item in items:
            if item.text.lower() == item_name.lower():
                item_container = item.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inventory_item')]")
                add_button = item_container.find_element(By.CSS_SELECTOR, f"button[id^='{self.ADD_TO_CART_PREFIX}']")
                add_button.click()
                return True
        return False

    def get_item_price(self, item_name):
        """Obtiene el precio de un item específico"""
        items = self.driver.find_elements(By.CLASS_NAME, self.INVENTORY_ITEM_NAME)
        for item in items:
            if item.text.lower() == item_name.lower():
                item_container = item.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inventory_item')]")
                price = item_container.find_element(By.CLASS_NAME, self.INVENTORY_ITEM_PRICE)
                return price.text
        return None

    def get_cart_count(self):
        """
        Obtiene el número de items en el carrito
        Returns:
            int: Número de items en el carrito
        """
        try:
            badge = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, self.CART_BADGE))
            )
            return int(badge.text)
        except (NoSuchElementException, TimeoutException):
            # Si el badge no existe, significa que no hay items
            return 0
        except ValueError as e:
            # Si el texto no se puede convertir a entero
            print(f"Error al convertir el texto del badge a número: {str(e)}")
            return 0
        except StaleElementReferenceException:
            # Si el elemento se vuelve obsoleto, intentar una vez más
            try:
                badge = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, self.CART_BADGE))
                )
                return int(badge.text)
            except:
                return 0


    def go_to_cart(self):
        """Navega a la página del carrito"""
        cart_icon = self.find_element(self.cart_icon_locator["id"], By.ID)
        cart_icon.click()

    def sort_products(self, option):
        """
        Ordena productos según la opción especificada
        Args:
            option (str): Opción de ordenamiento
                'az': Nombre (A a Z)
                'za': Nombre (Z a A)
                'lohi': Precio (menor a mayor)
                'hilo': Precio (mayor a menor)
        Raises:
            ValueError: Si la opción no es válida
            NoSuchElementException: Si no se encuentra el dropdown
        """
        valid_options = ['az', 'za', 'lohi', 'hilo']
        if option not in valid_options:
            raise ValueError(f"Opción de ordenamiento inválida. Opciones válidas: {valid_options}")

        try:
            sort_dropdown = self.find_element(self.SORT_DROPDOWN, By.CLASS_NAME)
            select = Select(sort_dropdown)
            select.select_by_value(option)
        except NoSuchElementException as e:
            raise NoSuchElementException("No se encontró el menú de ordenamiento") from e
        except Exception as e:
            raise Exception(f"Error al ordenar productos: {str(e)}") from e


    def get_product_names(self):
        """Retorna lista de nombres de productos en orden actual"""
        items = self.driver.find_elements(By.CLASS_NAME, self.INVENTORY_ITEM_NAME)
        return [item.text for item in items]

    def get_product_prices(self):
        """Retorna lista de precios en orden actual"""
        prices = self.driver.find_elements(By.CLASS_NAME, self.PRICE_LABEL)
        return [float(price.text.replace('$', '')) for price in prices]

    def filter_by_price_range(self, min_price, max_price):
        """Retorna productos dentro del rango de precios especificado"""
        items = self.driver.find_elements(By.CLASS_NAME, self.INVENTORY_ITEM_NAME)
        filtered_items = []

        for item in items:
            item_container = item.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inventory_item')]")
            price = float(item_container.find_element(By.CLASS_NAME, self.PRICE_LABEL).text.replace('$', ''))
            if min_price <= price <= max_price:
                filtered_items.append({
                    'name': item.text,
                    'price': price
                })

        return filtered_items

