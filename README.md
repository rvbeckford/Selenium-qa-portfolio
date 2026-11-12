# Selenium QA Portfolio

![Selenium tests](https://github.com/rvbeckford/Selenium-qa-portfolio/actions/workflows/selenium.yml/badge.svg)(https://github.com/rvbeckford/Selenium-qa-portfolio/actions/workflows/selenium.yml)

A Selenium WebDriver + pytest test suite: the SauceDemo journeys from the Playwright portfolio, rebuilt in Selenium so the learning is comparative — explicit waits instead of auto-waiting, raw locators instead of semantic ones.
##Coverage — 21 tests

-    **SauceDemo (7):** login happy path, 3 negative login cases (locked-out user, wrong password, empty username), checkout happy path, price sort low-to-high, remove item from cart — Page Object Model in pages/.
-    The Internet (9): JavaScript alerts, dropdown, checkboxes, file upload, add/remove elements, dynamic loading, hovers — the tricky widgets.
-    API (5): GET, POST, and DELETE against JSONPlaceholder with requests, plus a hybrid test that verifies the same API data in the browser.

##Failure evidence

A failing test saves a screenshot to screenshots/<test-name>.png before the browser quits, via a pytest_runtest_makereport hook in conftest.py.
##Security testing

The locked_out_user login test is an access-control case: a locked-out account cannot get in, and the app says so plainly.
##Project structure

```pages/                  Page objects (Login, Inventory, Cart, Checkout)
test_login.py           SauceDemo login tests
test_cart_checkout.py   SauceDemo cart and checkout tests
test_the_internet.py    The-internet widget tests
test_api.py             JSONPlaceholder API + hybrid tests
conftest.py             Driver fixture, screenshot-on-failure hook
```
##Running locally

1.    python -m venv .venv
2.    .venv\Scripts\activate
3.    pip install -r requirements.txt
4.    pytest -v
5.    pytest --html=report.html --self-contained-html — opens as a readable test report

##CI

GitHub Actions runs the full suite on every push to main (Python 3.14, Chrome, headless) and uploads the HTML report as an artifact.