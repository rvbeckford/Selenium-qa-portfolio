from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

def create_driver():
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-save-password-bubble")
    return webdriver.Chrome(options=options)


def login(driver):
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    
def go_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
    )


def cart_badge_text(driver):
    badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    return badge.text


def test_checkout_happy_path():
    driver = create_driver()
    try:
        login(driver)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
        assert cart_badge_text(driver) == "2"

        go_to_cart(driver)
        checkout_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()

        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        WebDriverWait(driver, 20).until(EC.url_contains("checkout-step-two"))
        print("URL after continue:", driver.current_url)
        finish_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='finish']"))
        )
        finish_button.click()


        header = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert header.text == "Thank you for your order!"
    finally:
        driver.quit()


def test_sort_price_low_to_high():
    driver = create_driver()
    try:
        login(driver)
        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text == "Sauce Labs Onesie"
        )

        names = [el.text for el in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        prices = [float(el.text.replace("$", "")) for el in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        assert names[0] == "Sauce Labs Onesie"
        assert prices[0] == 7.99
        assert prices == sorted(prices)
    finally:
        driver.quit()

def test_remove_item_from_cart():
    driver = create_driver()
    try:
        login(driver)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
        assert cart_badge_text(driver) == "2"

        go_to_cart(driver)
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "cart_item")) == 2
        )
        driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CLASS_NAME, "cart_item")) == 1
        )
        assert cart_badge_text(driver) == "1"
    finally:
        driver.quit()