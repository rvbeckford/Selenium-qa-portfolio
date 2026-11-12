import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report

@pytest.fixture
def driver(request):
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-save-password-bubble")
    if os.environ.get("CI"):
        options.add_argument("--headless==new")
    driver = webdriver.Chrome(options=options)
    yield driver
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(f"screenshots/{request.node.name}.png")
    driver.quit()