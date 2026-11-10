from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


BASE_URL = "http://the-internet.herokuapp.com"

def test_js_alert(driver):
    driver.get(f"{BASE_URL}/javascript_alerts")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    driver.switch_to.alert.accept()
    assert driver.find_element(By.ID, "result").text == "You successfully clicked an alert"

def test_js_confirm_dismiss(driver):
    driver.get(f"{BASE_URL}/javascript_alerts")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    driver.switch_to.alert.dismiss()
    assert driver.find_element(By.ID, "result").text == "You clicked: Cancel"

def test_js_prompt(driver):
    driver.get(f"{BASE_URL}/javascript_alerts")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    alert = driver.switch_to.alert
    alert.send_keys("Hello")
    alert.accept()
    assert driver.find_element(By.ID, "result").text == "You entered: Hello"

def test_dropdown(driver):
    driver.get(f"{BASE_URL}/dropdown")
    dropdown = Select(driver.find_element(By.ID, "dropdown"))
    dropdown.select_by_visible_text("Option 2")
    assert dropdown.first_selected_option.text == "Option 2"

def test_checkboxes(driver):
    driver.get(f"{BASE_URL}/checkboxes")
    boxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    boxes[0].click()
    assert boxes[0].is_selected()
    assert boxes[1].is_selected()
    boxes[1].click()
    assert not boxes[1].is_selected()

def test_file_upload(tmp_path, driver):
    sample = tmp_path / "sample.txt"
    sample.write_text("Hello from Selenium")
    driver.get(f"{BASE_URL}/upload")
    driver.find_element(By.ID, "file-upload").send_keys(str(sample))
    driver.find_element(By.ID, "file-submit").click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME,"h3"), "File Uploaded!"))
    assert driver.find_element(By.ID,"uploaded-files").text == "sample.txt"

def test_add_remove_elements(driver):
    driver.get(f"{BASE_URL}/add_remove_elements/")
    driver.find_element(By.CSS_SELECTOR, "button[onclick='addElement()']").click()
    delete_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='deleteElement()']")
    assert delete_button.is_displayed()
    delete_button.click()
    assert driver.find_elements(By.CSS_SELECTOR, "button[onclick='deleteElement()']") == []

def test_dynamic_loading(driver):
    driver.get(f"{BASE_URL}/dynamic_loading/2")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    wait = WebDriverWait(driver, 10)
    hello = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4")))
    assert hello.text == "Hello World!"

def test_hovers(driver):
    driver.get(f"{BASE_URL}/hovers")
    avatar = driver.find_element(By.CSS_SELECTOR, ".figure")
    ActionChains(driver).move_to_element(avatar).perform()
    caption = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".figcaption"))
    )
    assert "name: user1" in caption.text