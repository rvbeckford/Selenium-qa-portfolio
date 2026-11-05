import pytest
from pages.login_page import LoginPage

def test_standard_user_login(driver):
    page = LoginPage(driver)
    page.login("standard_user", "secret_sauce")
    assert "inventory.html" in driver.current_url

@pytest.mark.parametrize("username, password,expected", [
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
    ("standard_user", "wrong_password", "Epic sadface: Username and password do not match any user in this service"),
    ("", "secret_sauce", "Epic sadface: Username is required"),
])

def test_login_errors(driver, username, password, expected):
    page = LoginPage(driver)
    assert page.error_text_for(username, password) == expected