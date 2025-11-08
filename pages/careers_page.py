"""Careers page object"""
import allure
from pages.base_page import LoadableComponent
from utils.decorators import allure_step, screenshot_on_failure


class CareersPage(LoadableComponent):
    """Careers page object"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_page_name(self) -> str:
        return "CareersPage"
    
    @allure_step("Wait for Careers page to load")
    def load(self):
        """Careers page loaded via navigation, not direct URL"""
        self.wait_for_url_contains("careers", timeout=10)
    
    @allure_step("Verify Careers page blocks are visible")
    def is_loaded(self):
        """Verify all required blocks are present"""
        try:
            # Verify URL
            assert "careers" in self.get_current_url().lower(), \
                "URL does not contain 'careers'"
            
            # Verify all three blocks
            self._verify_locations_block()
            self._verify_teams_block()
            self._verify_life_at_insider_block()
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="careers_page_loaded",
                attachment_type=allure.attachment_type.PNG
            )
        except AssertionError as e:
            raise AssertionError(f"Careers page verification failed: {str(e)}")
    
    def _verify_locations_block(self):
        """Verify Locations block is visible"""
        locations_locator = self.get_locator("locations_block")
        self.scroll_to_element(locations_locator)
        assert self.is_element_visible(locations_locator), \
            "Locations block is not visible"
    
    def _verify_teams_block(self):
        """Verify Teams block is visible"""
        teams_locator = self.get_locator("teams_block")
        self.scroll_to_element(teams_locator)
        assert self.is_element_visible(teams_locator), \
            "Teams block is not visible"
    
    def _verify_life_at_insider_block(self):
        """Verify Life at Insider block is visible"""
        life_locator = self.get_locator("life_at_insider_block")
        self.scroll_to_element(life_locator)
        assert self.is_element_visible(life_locator), \
            "Life at Insider block is not visible"
