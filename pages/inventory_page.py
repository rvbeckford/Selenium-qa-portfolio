from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def add_backpack(self):
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    def add_bike_light(self):
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

    def cart_badge_text(self):
        badge = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        return badge.text

    def go_to_cart(self):
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
        )

    def sort_low_to_high(self):
        Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text == "Sauce Labs Onesie"
        )

    def first_item_name(self):
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text

    def prices(self):
        return [float(el.text.replace("$", "")) for el in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
