from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_NAV_BUTTON = (By.XPATH, "//p[text()='Конструктор']") 
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']") 
    FIRST_INGREDIENT = (By.XPATH, "(//img[@alt='Флюоресцентная булка R2-D3'])") 
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class,'Modal')]")    
    CONSTRUCTOR_TOP = (By.XPATH, "//span[text()='Перетяните булочку сюда (верх)']")
    CONSTRUCTOR_BOTTOM = (By.XPATH, "//span[text()='Перетяните булочку сюда (низ)']")  
    MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    INGREDIENT_COUNTER = (By.XPATH, "//div[contains(@class,'counter_counter')]/p")
    INGREDIENT_CARD = (By.XPATH, "(//div[contains(@class,'IngredientCard')])[1]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class,'Modal_modal__title') and contains(@class,'digits-large')]")

class OrderFeedPageLocators:
    TOTAL_COUNTER = (By.XPATH, "//p[normalize-space(text())='Выполнено за всё время:']/following-sibling::p[contains(@class,'digits-large')]")
    TODAY_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за сегодня')]/following::p[contains(@class,'OrderFeed_number__')][1]")
    IN_PROGRESS_ORDERS = (By.XPATH, "//h3[text()='В работе']/following-sibling::ul/li")

class LoginPageLocators:
    EMAIL_FIELD = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']") 
