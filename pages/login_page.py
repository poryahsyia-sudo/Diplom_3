from pages.base_page import BasePage
from pages.locators import LoginPageLocators
from pages.locators import MainPageLocators

class LoginPage(BasePage):

    def login(self, email, password):
        self.find(LoginPageLocators.EMAIL_FIELD).send_keys(email)
        self.find(LoginPageLocators.PASSWORD_FIELD).send_keys(password)
        self.click(LoginPageLocators.LOGIN_BUTTON)