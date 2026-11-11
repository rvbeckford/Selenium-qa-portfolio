import requests

BASE_URL = "https://jsonplaceholder.typicode.com/"

from selenium.webdriver.common.by import By


def test_get_single_post():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["userId"] == 1
    assert data["title"] == "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"

def test_get_posts_by_user():
    response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 10
    assert all(post["userId"] == 1 for post in posts)

def test_create_post():
    payload = {"title": "Selenium API test", "body": "Created by Selenium suite", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Selenium API test"
    assert data["id"] == 101

def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    assert response.json() == {}

def test_hybrid_api_data_in_browser(driver):
    response = requests.get(f"{BASE_URL}/posts/1")
    title = response.json()["title"]
    driver.get(f"{BASE_URL}/posts/1")
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert title in body_text