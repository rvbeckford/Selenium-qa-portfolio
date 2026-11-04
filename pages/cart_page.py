from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def click_checkout(self):
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()

    def wait_for_items(self, count):
        WebDriverWait(self.driver, 10).until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "cart_item")) == count
        )

    def remove_backpack(self):
        self.driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
