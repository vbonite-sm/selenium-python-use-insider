"""Base page class with common page object functionality"""
from abc import ABC


class BasePage(ABC):
    """Base page with common functionality for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
