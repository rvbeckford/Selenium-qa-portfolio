from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_checkout_happy_path(driver):
    LoginPage(driver).login("standard_user","secret_sauce")
    inventory = InventoryPage(driver)
    inventory.add_backpack()
    inventory.add_bike_light()
    assert inventory.cart_badge_text() == "2"
    inventory.go_to_cart()
    CartPage(driver).click_checkout()
    checkout = CheckoutPage(driver)
    checkout.fill_info("Test", "User", "12345")
    checkout.click_finish()
    assert checkout.complete_header_text() == "Thank you for your order!"

def test_sort_price_low_to_high(driver):
    LoginPage(driver).login("standard_user","secret_sauce")
    inventory = InventoryPage(driver)
    inventory.sort_low_to_high()
    assert inventory.first_item_name() == "Sauce Labs Onesie"
    prices = inventory.prices()
    assert prices[0] == 7.99
    assert prices == sorted(prices)

def test_remove_item_from_cart(driver):
    LoginPage(driver).login("standard_user","secret_sauce")
    inventory = InventoryPage(driver)
    inventory.add_backpack()
    inventory.add_bike_light()
    assert inventory.cart_badge_text() == "2"
    inventory.go_to_cart()
    cart = CartPage(driver)
    cart.wait_for_items(2)
    cart.remove_backpack()
    cart.wait_for_items(1)
    assert inventory.cart_badge_text() == "1"