"""Home page object"""
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object for useinsider.com"""
    
    def __init__(self, driver):
        super().__init__(driver)
