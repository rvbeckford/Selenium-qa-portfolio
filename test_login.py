from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_standard_user_login():
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
    finally:
        driver.quit()

def login_error_text(driver, username, password):
    driver.get("https://www.saucedemo.com")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
    )
    return error.text


def test_locked_out_user():
    driver = webdriver.Chrome()
    try:
        assert login_error_text(driver, "locked_out_user", "secret_sauce") == "Epic sadface: Sorry, this user has been locked out."
    finally:
        driver.quit()


def test_wrong_password():
    driver = webdriver.Chrome()
    try:
        assert login_error_text(driver, "standard_user", "wrong_password") == "Epic sadface: Username and password do not match any user in this service"
    finally:
        driver.quit()


def test_empty_username():
    driver = webdriver.Chrome()
    try:
        assert login_error_text(driver, "", "secret_sauce") == "Epic sadface: Username is required"
    finally:
        driver.quit()
