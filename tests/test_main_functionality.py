import pytest
import allure
from pages.main_page import MainPage
from pages.urls import BASE_URL, LOGIN_URL


@pytest.mark.usefixtures("driver")
@allure.feature("Основной функционал страницы конструктора")
class TestMainPage:

    @allure.story("Переход по кнопке 'Конструктор'")
    @allure.title("Проверка перехода в конструктор со страницы логина")
    def test_constructor_navigation(self, driver):
        page = MainPage(driver)
        page.open(LOGIN_URL)
        page.go_to_constructor()
        assert page.is_first_ingredient_visible(), \
            "Первый ингредиент не появился после перехода в Конструктор"

    @allure.story("Переход по кнопке 'Лента заказов'")
    @allure.title("Проверка перехода в ленту заказов")
    def test_order_feed_navigation(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.go_to_order_feed()
        assert "feed" in page.driver.current_url, \
            "Переход по кнопке 'Лента заказов' не произошёл"

    @allure.story("Модальное окно ингредиента")
    @allure.title("Проверка открытия модального окна ингредиента")
    def test_open_ingredient_modal(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.open_ingredient_modal()
        assert page.is_ingredient_modal_open(), \
            "Модальное окно ингредиента не открылось"

    @allure.story("Модальное окно ингредиента")
    @allure.title("Проверка закрытия модального окна ингредиента")
    def test_close_ingredient_modal(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        page.open_ingredient_modal()
        page.close_ingredient_modal()
        assert page.is_ingredient_modal_closed(), \
            "Модальное окно ингредиента не закрылось"

    @allure.story("Счётчик ингредиента")
    @allure.title("Проверка увеличения счётчика ингредиента при добавлении")
    def test_ingredient_counter(self, driver):
        page = MainPage(driver)
        page.open(BASE_URL)
        counter_before = page.get_ingredient_counter()
        page.add_ingredient_to_constructor("top")
        counter_after = page.get_ingredient_counter()
        assert counter_after > counter_before, \
            f"Счётчик ингредиента не увеличился: before={counter_before}, after={counter_after}"
