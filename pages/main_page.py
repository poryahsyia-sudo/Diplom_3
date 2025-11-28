import allure
from pages.base_page import BasePage
from pages.locators import MainPageLocators
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators  # доступ к локаторам через self.locators

    @allure.step("Открытие главной страницы")
    def open(self, url):
        super().open(url)

    @allure.step("Переход в конструктор бургеров")
    def go_to_constructor(self):
        self.click(self.locators.CONSTRUCTOR_NAV_BUTTON)

    @allure.step("Переход в ленту заказов")
    def go_to_order_feed(self):
        element = self.find(self.locators.ORDER_FEED_BUTTON)
        ActionChains(self.driver).move_to_element(element).perform()
        self.wait_until(EC.element_to_be_clickable(self.locators.ORDER_FEED_BUTTON))
        self.click(self.locators.ORDER_FEED_BUTTON)

    @allure.step("Открытие модального окна ингредиента")
    def open_ingredient_modal(self):
        self.click(self.locators.FIRST_INGREDIENT)

    @allure.step("Закрытие модального окна ингредиента")
    def close_ingredient_modal(self):
        self.click(self.locators.MODAL_CLOSE_BUTTON)

    @allure.step("Добавление ингредиента в конструктор ({position})")
    def add_ingredient_to_constructor(self, position="top"):
        ingredient = self.find(self.locators.FIRST_INGREDIENT)
        constructor = self.find(
            self.locators.CONSTRUCTOR_TOP
            if position == "top"
            else self.locators.CONSTRUCTOR_BOTTOM
        )
        self.drag_and_drop(ingredient, constructor)

    @allure.step("Проверка видимости элемента")
    def is_visible(self, locator, timeout=5):
        try:
            self.wait_for_visibility(locator, timeout)
            return True
        except Exception:
            return False

    @allure.step("Проверка невидимости элемента")
    def is_not_visible(self, locator, timeout=5):
        try:
            self.wait_for_invisibility(locator, timeout)
            return True
        except Exception:
            return False

    @allure.step("Ожидание появления номера заказа")
    def wait_for_order_number(self, timeout=30):
        self.wait_for_visibility(self.locators.ORDER_NUMBER, timeout)

    @allure.step("Получение номера заказа")
    def get_order_number(self, timeout=30):
        self.wait_for_visibility(self.locators.ORDER_NUMBER, timeout)
        return self.get_text(self.locators.ORDER_NUMBER, timeout)

    @allure.step("Нажатие кнопки 'Оформить заказ'")
    def place_order(self):
        self.click(self.locators.PLACE_ORDER_BUTTON)

    @allure.step("Закрытие модального окна заказа")
    def close_order_modal(self):
        self.click(self.locators.MODAL_CLOSE_BUTTON)
