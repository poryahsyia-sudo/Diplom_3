import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from pages.urls import BASE_URL

@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.story("Новый заказ появляется в разделе 'В работе'")
    @allure.title("Проверка появления нового заказа")
    def test_new_order_in_work(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        ingredient = main.find(MainPageLocators.FIRST_INGREDIENT)
        constructor = main.find(MainPageLocators.CONSTRUCTOR_TOP)
        main.drag_and_drop_universal(ingredient, constructor)
        main.click(MainPageLocators.PLACE_ORDER_BUTTON)
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER))
        WebDriverWait(driver, 30).until(lambda d: len(main.find(MainPageLocators.ORDER_NUMBER).text.strip()) >= 6)
        order_number = main.find(MainPageLocators.ORDER_NUMBER).text
        main.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        main.go_to_order_feed()
        WebDriverWait(driver, 30).until(lambda d: order_number in d.page_source,
                                        f"Заказ {order_number} не появился в ленте заказов")
        assert order_number in driver.page_source, f"Заказ {order_number} не найден в ленте заказов"

    @allure.story("Счётчик 'Выполнено за сегодня'")
    @allure.title("Проверка увеличения счётчика за сегодня")
    def test_complited_today_counter(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        main.go_to_order_feed()
        counter_before = feed.get_today_done()
        main.go_to_constructor()
        ingredient = main.find(MainPageLocators.FIRST_INGREDIENT)
        constructor = main.find(MainPageLocators.CONSTRUCTOR_TOP)
        main.drag_and_drop_universal(ingredient, constructor)
        main.click(MainPageLocators.PLACE_ORDER_BUTTON)
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER))
            main.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        except Exception:
            pass
        main.go_to_order_feed()
        feed.wait_counter_greater(feed.get_today_done, counter_before, timeout=30)
        counter_after = feed.get_today_done()
        assert counter_after >= counter_before + 1, \
            f"Счётчик 'Выполнено за сегодня' не увеличился корректно: before={counter_before}, after={counter_after}"

    @allure.story("Счётчик 'Выполнено за всё время'")
    @allure.title("Проверка увеличения счётчика за всё время")
    def test_completed_all_time_counter(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        main.go_to_order_feed()
        counter_before = feed.get_total_done()
        main.go_to_constructor()
        ingredient = main.find(MainPageLocators.FIRST_INGREDIENT)
        constructor = main.find(MainPageLocators.CONSTRUCTOR_TOP)
        main.drag_and_drop_universal(ingredient, constructor)
        main.click(MainPageLocators.PLACE_ORDER_BUTTON)
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER)
        )
        try:
            main.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        except Exception:
            pass
        main.go_to_order_feed()
        WebDriverWait(driver, 60).until(
            lambda d: feed.get_total_done() > counter_before,
            f"Счётчик 'Выполнено за всё время' не увеличился в течение 60 секунд"
        )
        counter_after = feed.get_total_done()
        assert counter_after >= counter_before + 1, \
            f"Счётчик 'Выполнено за всё время' не увеличился: before={counter_before}, after={counter_after}"