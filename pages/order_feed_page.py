import re
from pages.base_page import BasePage
from pages.locators import OrderFeedPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class OrderFeedPage(BasePage):

    def _to_int(self, text: str) -> int:
        # Оставляем только цифры (на случай "12 345" или "\n1 234")
        digits = re.sub(r"[^\d]", "", text or "")
        return int(digits) if digits else 0

    def get_total_done(self, timeout=40):   
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//p[contains(@class,'digits-large')]")
            )
        )
        elements = self.driver.find_elements(By.XPATH, "//p[contains(@class,'digits-large')]")
        if len(elements) >= 1:
            raw = elements[0].text  
            return int(''.join(ch for ch in raw if ch.isdigit()))
        raise Exception("Счётчик 'Выполнено за всё время' не найден")


    def get_today_done(self):
        raw = self.find(OrderFeedPageLocators.TODAY_COUNTER).text
        return self._to_int(raw)

    def wait_counter_greater(self, getter, baseline, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda d: getter() > baseline
        )

    def get_in_progress_orders(self):
        return self.find_all(OrderFeedPageLocators.IN_PROGRESS_ORDERS)