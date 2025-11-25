from pages.base_page import BasePage
from pages.locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pages.urls import BASE_URL
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class MainPage(BasePage):

    def open(self, url=BASE_URL):
        self.driver.get(url)

    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_NAV_BUTTON)

    def go_to_order_feed(self):
        element = self.find(MainPageLocators.ORDER_FEED_BUTTON)
        ActionChains(self.driver).move_to_element(element).perform()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.ORDER_FEED_BUTTON)
        )
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)


    def open_ingredient_modal(self):
        self.click(MainPageLocators.FIRST_INGREDIENT)

    def close_ingredient_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)

    def add_ingredient_to_constructor(self, position="top"):
        ingredient = self.find(MainPageLocators.FIRST_INGREDIENT)
        constructor = self.find(MainPageLocators.CONSTRUCTOR_TOP if position == "top" else MainPageLocators.CONSTRUCTOR_BOTTOM)
        self.drag_and_drop_universal(ingredient, constructor)

    def is_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def is_not_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except:
            return False
        

    def drag_and_drop_universal(self, ingredient, constructor):
        self.scroll_into_view(ingredient)
        self.scroll_into_view(constructor)
        js = """
            const src = arguments[0];
            const tgt = arguments[1];
            const dataTransfer = new DataTransfer();
            function fire(el, type, dt){
                const e = new DragEvent(type, {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dt
                });
                el.dispatchEvent(e);
            }
            fire(src, 'dragstart', dataTransfer);
            fire(tgt, 'dragenter', dataTransfer);
            fire(tgt, 'dragover', dataTransfer);
            fire(tgt, 'drop', dataTransfer);
            fire(src, 'dragend', dataTransfer);
        """
        try:
            self.driver.execute_script(js, ingredient, constructor)
        except Exception:
            # Fallback: классический ActionChains
            actions = ActionChains(self.driver)
            actions.click_and_hold(ingredient).move_to_element(constructor).pause(0.2).release().perform()