import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os
from pages.login_page import LoginPage
from pages.urls import LOGIN_URL
from data.users import VALID_USER

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
        # Попытка автоматически скачать geckodriver (без использования токена)
        try:
            gecko_path = GeckoDriverManager().install()
        except Exception as e:
            # Если скачивание не удалось — даём понятное сообщение с подсказкой
            raise RuntimeError(
                "Не удалось автоматически скачать geckodriver.\n"
                "Возможные причины: rate limit на GitHub или отсутствие соединения.\n"
                "Решение:\n"
                "  1) Установите geckodriver вручную и добавьте его в PATH, или\n"
                "  2) установите GH_TOKEN в .env (если вы хотите использовать токен для увеличения лимита).\n"
                f"Техническая ошибка: {e}"
            )

        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver_instance = webdriver.Firefox(
            service=FirefoxService(gecko_path),
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