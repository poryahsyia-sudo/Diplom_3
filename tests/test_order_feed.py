import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.urls import BASE_URL

@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.story("Новый заказ появляется в разделе 'В работе'")
    @allure.title("Проверка появления нового заказа")
    def test_new_order_in_work(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        main.add_ingredient_to_constructor("top")
        main.place_order()
        main.wait_for_order_number()
        order_number = main.get_order_number()
        main.close_order_modal()
        main.go_to_order_feed()
        feed.wait_until(lambda d: order_number in d.page_source, timeout=30)
        assert order_number in driver.page_source, \
            f"Заказ {order_number} не найден в ленте заказов"

    @allure.story("Счётчик 'Выполнено за сегодня'")
    @allure.title("Проверка увеличения счётчика за сегодня после оформления заказа")
    def test_completed_today_counter(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        main.go_to_order_feed()
        counter_before = feed.get_today_done()
        main.go_to_constructor()
        main.add_ingredient_to_constructor("top")
        main.place_order()
        main.wait_for_order_number()
        main.close_order_modal()
        main.go_to_order_feed()
        feed.wait_counter_greater(feed.get_today_done, counter_before, timeout=30)
        counter_after = feed.get_today_done()
        assert counter_after >= counter_before + 1, \
            f"Счётчик 'Выполнено за сегодня' не увеличился: before={counter_before}, after={counter_after}"

    @allure.story("Счётчик 'Выполнено за всё время'")
    @allure.title("Проверка увеличения общего счётчика после оформления заказа")
    def test_completed_all_time_counter(self, driver, login):
        main = MainPage(driver)
        feed = OrderFeedPage(driver)
        main.go_to_order_feed()
        counter_before = feed.get_total_done()
        main.go_to_constructor()
        main.add_ingredient_to_constructor("top")
        main.place_order()
        main.wait_for_order_number()
        main.close_order_modal()
        main.go_to_order_feed()
        feed.wait_counter_greater(feed.get_total_done, counter_before, timeout=60)
        counter_after = feed.get_total_done()
        assert counter_after >= counter_before + 1, \
            f"Счётчик 'Выполнено за всё время' не увеличился: before={counter_before}, after={counter_after}"