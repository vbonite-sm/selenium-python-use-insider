"""Base page class with common page object functionality"""
from abc import ABC, abstractmethod
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, List
import logging
from config.config import Config
from utils.decorators import log_action, screenshot_on_failure
from locators.locator_repository import locator_repo
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)


class BasePage(ABC):
    """Base page with common functionality for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.DEFAULT_TIMEOUT)
        self.locator_repo = locator_repo
    
    @abstractmethod
    def get_page_name(self) -> str:
        """Return the page name for locator repository"""
        pass
    
    def get_locator(self, element_name: str, **kwargs) -> Tuple:
        """Get locator from repository"""
        return self.locator_repo.get(self.get_page_name(), element_name, **kwargs)
    
    @log_action
    def find_element(self, locator: Tuple, timeout: int = None):
        """Find single element with explicit wait"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    @log_action
    def find_elements(self, locator: Tuple, timeout: int = None) -> List:
        """Find multiple elements with explicit wait"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    @log_action
    @screenshot_on_failure
    def click(self, locator: Tuple, timeout: int = None):
        """Click on element with wait for clickability"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    
    @log_action
    def get_text(self, locator: Tuple) -> str:
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    @log_action
    def is_element_visible(self, locator: Tuple, timeout: int = None) -> bool:
        """Check if element is visible"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
        
    @log_action
    def is_element_present(self, locator: Tuple, timeout: int = None) -> bool:
        """Check if element is present in DOM"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False    
    
    @log_action
    def scroll_to_element(self, locator: Tuple):
        """Scroll element into view"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @log_action
    def wait_for_url_contains(self, url_part: str, timeout: int = None):
        """Wait for URL to contain specific text"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        WebDriverWait(self.driver, wait_time).until(
            EC.url_contains(url_part)
        )
    
    @log_action
    def switch_to_new_window(self):
        """Switch to newly opened window/tab"""
        self.wait.until(lambda d: len(d.window_handles) > 1)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
    
    @log_action
    def wait_for_element_and_click(self, locator: Tuple, timeout: int = None):
        """Wait for element to be clickable and click it - useful for AJAX loaded elements"""
        wait_time = timeout or Config.DEFAULT_TIMEOUT
        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element
    
    @log_action
    def dismiss_cookie_banner_if_present(self):
        """Dismiss cookie consent banner if it appears"""

        try:
            cookie_banner = self.get_locator("cookie_banner_container")
            if self.is_element_present(cookie_banner):
                accept_btn = self.get_locator("cookie_accept_btn")
                if self.is_element_visible(accept_btn, timeout=5):
                    self.click(accept_btn)
                    time.sleep(1)
        except Exception as e:
            # Silently continue if cookie banner handling fails
            logger.debug(f"Cookie banner handling: {e}")
            pass
        
    @log_action
    def hover_over_element(self, locator):
        """Hover over an element"""
        
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.find_element(locator)
        
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url


class LoadableComponent(BasePage):
    """Loadable Component pattern - ensures page is loaded before use"""
    
    @abstractmethod
    def load(self):
        """Navigate to the page"""
        pass
    
    @abstractmethod
    def is_loaded(self):
        """Verify the page is loaded"""
        pass
    
    def get(self):
        """Load and verify the page"""
        self.load()
        self.is_loaded()
        return self
