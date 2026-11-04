from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage


def create_driver():
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-save-password-bubble")
    return webdriver.Chrome(options=options)


def test_standard_user_login():
    driver = create_driver()
    try:
        LoginPage(driver).login("standard_user", "secret_sauce")
        assert "inventory.html" in driver.current_url
    finally:
        driver.quit()


def test_locked_out_user():
    driver = create_driver()
    try:
        assert LoginPage(driver).error_text_for("locked_out_user", "secret_sauce") == "Epic sadface: Sorry, this user has been locked out."
    finally:
        driver.quit()


def test_wrong_password():
    driver = create_driver()
    try:
        assert LoginPage(driver).error_text_for("standard_user", "wrong_password") == "Epic sadface: Username and password do not match any user in this service"
    finally:
        driver.quit()


def test_empty_username():
    driver = create_driver()
    try:
        assert LoginPage(driver).error_text_for("", "secret_sauce") == "Epic sadface: Username is required"
    finally:
        driver.quit()
