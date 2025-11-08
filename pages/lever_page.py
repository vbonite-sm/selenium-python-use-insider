"""Lever Application Form page"""
import allure
from pages.base_page import LoadableComponent
from utils.decorators import allure_step


class LeverPage(LoadableComponent):
    """Lever Application Form page"""
    
    def get_page_name(self) -> str:
        return "LeverPage"
    
    def load(self):
        """Lever page is opened via View Role button"""
        pass  # Not directly navigated to
    
    @allure_step("Verify Lever application form is displayed")
    def is_loaded(self):
        """Verify Lever application page loaded"""
        try:
            # Verify URL contains 'lever'
            current_url = self.get_current_url()
            assert "lever" in current_url.lower() or "jobs.lever.co" in current_url, \
                f"Expected Lever URL, got: {current_url}"
            
            # Verify application form is present
            form_locator = self.get_locator("application_form")
            assert self.is_element_visible(form_locator, timeout=10), \
                "Application form not visible"
            
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="lever_application_page",
                attachment_type=allure.attachment_type.PNG
            )
        
        except AssertionError as e:
            raise AssertionError(f"Lever page verification failed: {str(e)}")
