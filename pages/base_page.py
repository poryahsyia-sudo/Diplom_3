import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открытие страницы по URL: {1}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Поиск элемента: {1}")
    def find(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Поиск всех элементов: {1}")
    def find_all(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    @allure.step("Ожидание видимости элемента: {1}")
    def wait_for_visibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание невидимости элемента: {1}")
    def wait_for_invisibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Ожидание выполнения произвольного условия")
    def wait_until(self, condition, timeout=15):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Получение текста элемента: {1}")
    def get_text(self, locator, timeout=15):
        element = self.find(locator, timeout)
        return element.text.strip()

    @allure.step("Клик по элементу: {1}")
    def click(self, locator, timeout=15):
        element_to_click = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element_to_click.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element_to_click)

    @allure.step("Прокрутка к элементу")
    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'center'});", element
        )

    @allure.step("Перетаскивание элемента мышью")
    def drag_and_drop(self, source_element, target_element):
        self.scroll_into_view(source_element)
        self.scroll_into_view(target_element)
        actions = ActionChains(self.driver)
        actions.click_and_hold(source_element).move_to_element(target_element).pause(0.2).release().perform()
