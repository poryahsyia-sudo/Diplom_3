import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import allure
import os
from dotenv import load_dotenv  # <- импортируем dotenv
from pages.login_page import LoginPage
from pages.urls import LOGIN_URL
from data.users import VALID_USER

# загружаем переменные окружения из .env
load_dotenv()

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver_instance = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser == "firefox":
        gh_token = os.getenv("GH_TOKEN")
        if not gh_token:
            raise ValueError(
                "В файле .env не найден GH_TOKEN. Добавьте токен."
            )
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver_instance = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Browser {browser} is not supported")
    driver_instance.browser_name = browser
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def login(driver):
    page = LoginPage(driver)
    page.open(LOGIN_URL)
    page.login(VALID_USER["email"], VALID_USER["password"])
    return page