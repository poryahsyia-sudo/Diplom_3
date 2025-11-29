import allure
from pages.base_page import BasePage
from pages.locators import OrderFeedPageLocators
from pages.helpers import to_int
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class OrderFeedPage(BasePage):

    @allure.step("Получение общего счётчика 'Выполнено за всё время'")
    def get_total_done(self, timeout=40):
        self.wait_for_presence(OrderFeedPageLocators.TOTAL_COUNTER, timeout)
        elements = self.find_all(OrderFeedPageLocators.TOTAL_COUNTER)
        for el in elements:
            try:
                label = el.find_element(*OrderFeedPageLocators.COUNTER_LABEL)
                if "за все время" in label.text.lower():
                    return to_int(el.text)
            except Exception:
                continue
        raise Exception("Не найден блок со счётчиком 'Выполнено за всё время'")

    @allure.step("Получение счётчика 'Выполнено за сегодня'")
    def get_today_done(self, timeout=40):
        self.wait_for_presence(OrderFeedPageLocators.TOTAL_COUNTER , timeout)
        elements = self.find_all(OrderFeedPageLocators.TOTAL_COUNTER)
        for el in elements:
            try:
                label = el.find_element(*OrderFeedPageLocators.COUNTER_LABEL)
                if "за сегодня" in label.text.lower():
                    return to_int(el.text)
            except Exception:
                continue
        raise Exception("Не найден блок со счётчиком 'Выполнено за сегодня'")

    @allure.step("Проверка, что заказ с номером {order_number} отображается в ленте заказов")
    def is_order_in_feed(self, order_number, timeout=60):
        """Ожидает появления заказа с указанным номером в ленте заказов"""
        locator = (By.XPATH, f"//*[contains(text(), '#{order_number}')]")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*locator)) > 0,
                f"Заказ #{order_number} не появился в ленте заказов за {timeout} секунд"
            )
            return True
        except Exception:
            return False