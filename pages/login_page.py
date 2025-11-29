import allure
from pages.base_page import BasePage
from pages.locators import LoginPageLocators


class LoginPage(BasePage):

    @allure.step("Авторизация пользователя с email: {email}")
    def login(self, email, password):
        self.fill_email(email)
        self.fill_password(password)
        self.submit_login()

    @allure.step("Ввод email")
    def fill_email(self, email):
        field = self.find(LoginPageLocators.EMAIL_FIELD)
        field.clear()
        field.send_keys(email)

    @allure.step("Ввод пароля")
    def fill_password(self, password):
        field = self.find(LoginPageLocators.PASSWORD_FIELD)
        field.clear()
        field.send_keys(password)

    @allure.step("Нажатие кнопки 'Войти'")
    def submit_login(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)