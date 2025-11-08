"""Home page object"""
import allure
from pages.base_page import LoadableComponent
from utils.decorators import allure_step, screenshot_on_failure
from config.config import Config


class HomePage(LoadableComponent):
    """Home page object for useinsider.com"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_name(self) -> str:
        return "HomePage"
    
    @allure_step("Navigate to Insider home page")
    def load(self):
        """Navigate to home page"""
        self.driver.get(Config.BASE_URL)
        self._handle_cookies()
    
    @allure_step("Verify home page is loaded")
    def is_loaded(self):
        """Verify home page loaded successfully"""
        try:
            # Verify URL
            assert Config.BASE_URL in self.get_current_url(), \
                f"Expected URL to contain {Config.BASE_URL}"
            
            # Verify page title or main element
            company_menu_locator = self.get_locator("company_menu")
            assert self.is_element_visible(company_menu_locator, timeout=10), \
                "Company menu not visible on home page"
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="home_page_loaded",
                attachment_type=allure.attachment_type.PNG
            )
        except AssertionError as e:
            raise AssertionError(f"Home page failed to load: {str(e)}")
    
    def _handle_cookies(self):
        """Handle cookie consent if present"""
        try:
            cookies_btn_locator = self.get_locator("accept_cookies_btn")
            if self.is_element_visible(cookies_btn_locator, timeout=3):
                self.click(cookies_btn_locator)
        except:
            pass  # Cookie banner not present
    
    @allure_step("Navigate to Careers page")
    @screenshot_on_failure
    def navigate_to_careers(self):
        """Navigate to Careers page via Company menu"""
        # Click Company menu
        company_menu_locator = self.get_locator("company_menu")
        self.click(company_menu_locator)
        
        # Click Careers link
        careers_link_locator = self.get_locator("careers_link")
        self.click(careers_link_locator)
        
        # Import here to avoid circular import
        from pages.careers_page import CareersPage
        return CareersPage(self.driver)
