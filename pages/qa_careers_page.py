"""QA Careers page with job filtering functionality"""
import allure
import logging
from selenium.webdriver.common.by import By
from pages.base_page import LoadableComponent
from utils.decorators import allure_step, screenshot_on_failure
from config.config import Config
from typing import List, Dict

logger = logging.getLogger(__name__)


class QACareersPage(LoadableComponent):
    """QA Careers page with job filtering"""
    
    def get_page_name(self) -> str:
        return "QACareersPage"
    
    @allure_step("Navigate to QA Careers page")
    def load(self):
        """Navigate directly to QA careers page"""
        self.driver.get(Config.CAREERS_QA_URL)
    
    @allure_step("Verify QA Careers page is loaded")
    def is_loaded(self):
        """Verify QA careers page loaded"""
        try:
            assert Config.CAREERS_QA_URL in self.get_current_url(), \
                f"Expected URL {Config.CAREERS_QA_URL}"
            
            see_all_jobs_locator = self.get_locator("see_all_jobs_btn")
            assert self.is_element_visible(see_all_jobs_locator, timeout=10), \
                "'See all QA jobs' button not visible"
        
        except AssertionError as e:
            raise AssertionError(f"QA Careers page failed to load: {str(e)}")
    
    @allure_step("Click 'See all QA jobs' button")
    @screenshot_on_failure
    def click_see_all_jobs(self):
        """Click on 'See all QA jobs' button and wait for job listings to load"""
        see_all_jobs_locator = self.get_locator("see_all_jobs_btn")
        self.scroll_to_element(see_all_jobs_locator)
        self.click(see_all_jobs_locator)
        
        # Wait for transition/page load
        import time
        time.sleep(1)  # Brief wait for transition
        
        # Verify job list loaded
        job_list_locator = self.get_locator("job_list")
        assert self.is_element_visible(job_list_locator, timeout=60), \
            "Job listings did not load after clicking 'See all QA jobs'"
            
        # Dismiss cookie banner if present
        self.dismiss_cookie_banner_if_present()
        
        # Attach screenshot to confirm jobs loaded
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="job_listings_loaded",
            attachment_type=allure.attachment_type.PNG
        )
    
    @allure_step("Filter jobs by location: {location}")
    @screenshot_on_failure
    def filter_by_location(self, location: str):
        """Filter jobs by location using Select2 dropdown with polling"""
        import time
        
        # Poll for dropdown options to load (AJAX can take a long time)
        max_wait = 300  # 5 minutes total
        poll_interval = 30  # Check every 30 seconds
        elapsed = 0
        
        location_filter_locator = self.get_locator("location_filter")
        options_locator = self.get_locator("location_dropdown_options")
        specific_option_locator = self.get_locator("location_option", location=location)
        
        # Scroll to filter element
        self.scroll_to_element(location_filter_locator)
        
        while elapsed < max_wait:
            try:
                # Dismiss cookie banner if present
                self.dismiss_cookie_banner_if_present()
                
                # Click to open dropdown
                self.click(location_filter_locator)
                time.sleep(2)  # Brief wait for dropdown to open
                
                # Check if dropdown options are loaded
                if self.is_element_visible(options_locator, timeout=5):
                    # Options are loaded, try to click the specific one
                    try:
                        self.scroll_to_element(specific_option_locator)
                        self.wait_for_element_and_click(specific_option_locator, timeout=5)
                        logger.info(f"Successfully clicked location: {location}")
                        break
                    except Exception as click_error:
                        logger.warning(f"Options loaded but couldn't click '{location}' yet: {click_error}")
                        # Close dropdown and continue polling
                        self.click(location_filter_locator)
                        time.sleep(1)
                else:
                    # No options loaded yet, close dropdown
                    logger.info(f"No options loaded yet after {elapsed}s, closing dropdown and waiting...")
                    self.click(location_filter_locator)
                    time.sleep(1)
                
                # Wait before next poll
                if elapsed + poll_interval < max_wait:
                    logger.info(f"Waiting {poll_interval}s before next attempt...")
                    time.sleep(poll_interval)
                    elapsed += poll_interval
                else:
                    raise Exception(f"Dropdown options did not load after {max_wait}s")
                    
            except Exception as e:
                if elapsed + poll_interval >= max_wait:
                    logger.error(f"Failed to select location after {max_wait}s: {e}")
                    raise
                # Close dropdown if open
                try:
                    self.click(location_filter_locator)
                except:
                    pass
                time.sleep(poll_interval)
                elapsed += poll_interval
        
        # Wait for filter to apply
        time.sleep(2)
    
    @allure_step("Filter jobs by department: {department}")
    @screenshot_on_failure
    def filter_by_department(self, department: str):
        """Filter jobs by department using Select2 dropdown with polling"""
        import time
        
        # Poll for dropdown options to load (AJAX can take a long time)
        max_wait = 300  # 5 minutes total
        poll_interval = 30  # Check every 30 seconds
        elapsed = 0
        
        department_filter_locator = self.get_locator("department_filter")
        options_locator = self.get_locator("department_dropdown_options")
        specific_option_locator = self.get_locator("department_option", department=department)
        
        # Scroll to filter element
        self.scroll_to_element(department_filter_locator)
        
        while elapsed < max_wait:
            try:
                
                # Dismiss cookie banner if present
                self.dismiss_cookie_banner_if_present()
                
                # Click to open dropdown
                self.click(department_filter_locator)
                time.sleep(2)  # Brief wait for dropdown to open
                
                # Check if dropdown options are loaded
                if self.is_element_visible(options_locator, timeout=5):
                    # Options are loaded, try to click the specific one
                    try:
                        self.scroll_to_element(specific_option_locator)
                        self.wait_for_element_and_click(specific_option_locator, timeout=5)
                        logger.info(f"Successfully clicked department: {department}")
                        break
                    except Exception as click_error:
                        logger.warning(f"Options loaded but couldn't click '{department}' yet: {click_error}")
                        # Close dropdown and continue polling
                        self.click(department_filter_locator)
                        time.sleep(1)
                else:
                    # No options loaded yet, close dropdown
                    logger.info(f"No options loaded yet after {elapsed}s, closing dropdown and waiting...")
                    self.click(department_filter_locator)
                    time.sleep(1)
                
                # Wait before next poll
                if elapsed + poll_interval < max_wait:
                    logger.info(f"Waiting {poll_interval}s before next attempt...")
                    time.sleep(poll_interval)
                    elapsed += poll_interval
                else:
                    raise Exception(f"Dropdown options did not load after {max_wait}s")
                    
            except Exception as e:
                if elapsed + poll_interval >= max_wait:
                    logger.error(f"Failed to select department after {max_wait}s: {e}")
                    raise
                # Close dropdown if open
                try:
                    self.click(department_filter_locator)
                except:
                    pass
                time.sleep(poll_interval)
                elapsed += poll_interval
        
        # Wait for filter to apply
        time.sleep(2)
    
    @allure_step("Get all job listings")
    def get_job_listings(self) -> List[Dict[str, str]]:
        """Get all job listings with their details"""
        job_list_locator = self.get_locator("job_list")
        job_elements = self.find_elements(job_list_locator)
        
        jobs = []
        for job_elem in job_elements:
            try:
                position = job_elem.find_element(*self.get_locator("job_position")).text
                department = job_elem.find_element(*self.get_locator("job_department")).text
                location = job_elem.find_element(*self.get_locator("job_location")).text
                
                jobs.append({
                    'position': position,
                    'department': department,
                    'location': location,
                    'element': job_elem
                })
            except Exception as e:
                continue
        
        allure.attach(
            str(jobs),
            name="job_listings",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return jobs
    
    @allure_step("Verify job listings contain expected values")
    def verify_job_listings(self, expected_position: str, expected_department: str, expected_location: str):
        """Verify all jobs match expected criteria"""
        jobs = self.get_job_listings()
        
        assert len(jobs) > 0, "No jobs found in the list"
        
        for idx, job in enumerate(jobs, 1):
            with allure.step(f"Verify Job #{idx}: {job['position']}"):
                assert expected_position.lower() in job['position'].lower(), \
                    f"Job {idx}: Position '{job['position']}' does not contain '{expected_position}'"
                
                assert expected_department.lower() in job['department'].lower(), \
                    f"Job {idx}: Department '{job['department']}' does not contain '{expected_department}'"
                
                assert expected_location.lower() in job['location'].lower(), \
                    f"Job {idx}: Location '{job['location']}' does not contain '{expected_location}'"
    
    @allure_step("Click 'View Role' button for first job")
    @screenshot_on_failure
    def click_view_role(self):
        """Click View Role button on first job"""
        view_role_locator = self.get_locator("view_role_btn")
        self.scroll_to_element(view_role_locator)
        self.click(view_role_locator)
        
        # Switch to new tab/window
        self.switch_to_new_window()
        
    @allure_step("Click 'View Role' button of specified job")
    @screenshot_on_failure
    def click_view_role_of_specific_job(self, data_location: str, data_team: str):
        """Click View Role button of specified job"""
        job_card_locator = self.get_locator("job_card_by_attributes", data_location=data_location, data_team=data_team)

        # Find job cards matching the criteria
        job_cards = self.find_elements(job_card_locator)
        assert len(job_cards) > 0, f"No job found with location '{data_location}' and department '{data_team}'"

        first_job_card = job_cards[0]
        
        # Hover over the job card to reveal the View Role button
        self.hover_over_element(first_job_card)
        
        # Click the View Role button within that job card
        view_role_locator = self.get_locator("view_role_btn")
        self.click(view_role_locator)

        # Switch to new tab/window
        self.switch_to_new_window()
