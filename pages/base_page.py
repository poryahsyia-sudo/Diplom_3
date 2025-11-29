import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть страницу по адресу: {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Найти элемент по локатору: {locator}")
    def find(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Найти все элементы по локатору: {locator}")
    def find_all(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_visibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидание присутствия элемента в DOM: {locator}")
    def wait_for_presence(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Ожидание невидимости элемента: {locator}")
    def wait_for_invisibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Ожидание выполнения произвольного условия")
    def wait_until(self, condition, timeout=15):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator, timeout=15):
        element = self.find(locator, timeout)
        return element.text.strip()

    @allure.step("Клик по элементу: {locator}")
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

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_and_drop(self, ingredient, constructor):
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
            actions = ActionChains(self.driver)
            actions.click_and_hold(ingredient).move_to_element(constructor).pause(0.2).release().perform()

    @allure.step("Ожидание увеличения значения счётчика (текущее: {old_value})")
    def wait_counter_greater(self, counter_method, old_value, timeout=60):
        def condition(driver):
            with allure.step("Проверка, что значение счётчика увеличилось"):
                try:
                    return counter_method() > old_value
                except Exception:
                    return False

        WebDriverWait(self.driver, timeout, poll_frequency=2).until(
            condition,
            f"Счётчик не увеличился в течение {timeout} секунд (было {old_value})"
        )
