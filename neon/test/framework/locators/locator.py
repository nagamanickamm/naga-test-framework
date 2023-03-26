from selenium.webdriver.common.by import By


class Locator:
    xpath = By.XPATH
    id = By.ID
    css = By.CSS_SELECTOR
    name = By.NAME
    tag_name = By.TAG_NAME
    link_text = By.LINK_TEXT
    partial_link_text = By.PARTIAL_LINK_TEXT
    class_name = By.CLASS_NAME
