import allure
from pages.base_page import BasePage
from pages.locators import OrderFeedPageLocators
from helpers import to_int


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
        self.wait_for_presence(OrderFeedPageLocators.TOTAL_COUNTER, timeout)
        elements = self.find_all(OrderFeedPageLocators.TOTAL_COUNTER)
        for el in elements:
            try:
                label = el.find_element(*OrderFeedPageLocators.COUNTER_LABEL)
                if "за сегодня" in label.text.lower():
                    return to_int(el.text)
            except Exception:
                continue
        raise Exception("Не найден блок со счётчиком 'Выполнено за сегодня'")
