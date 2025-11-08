"""QA Careers page with job filtering functionality"""
import allure
from pages.base_page import LoadableComponent
from utils.decorators import allure_step, screenshot_on_failure
from config.config import Config
from typing import List, Dict


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
        """Click on 'See all QA jobs' button"""
        see_all_jobs_locator = self.get_locator("see_all_jobs_btn")
        self.scroll_to_element(see_all_jobs_locator)
        self.click(see_all_jobs_locator)
        
        # Wait for job list to load
        job_list_locator = self.get_locator("job_list")
        self.is_element_visible(job_list_locator, timeout=10)
    
    @allure_step("Filter jobs by location: {location}")
    @screenshot_on_failure
    def filter_by_location(self, location: str):
        """Filter jobs by location"""
        # Click location dropdown
        location_filter_locator = self.get_locator("location_filter")
        self.click(location_filter_locator)
        
        # Select location option
        location_option_locator = self.get_locator("location_option", location=location)
        self.click(location_option_locator)
        
        # Wait for results to update
        import time
        time.sleep(2)  # Allow filter to apply
    
    @allure_step("Filter jobs by department: {department}")
    @screenshot_on_failure
    def filter_by_department(self, department: str):
        """Filter jobs by department"""
        # Click department dropdown
        department_filter_locator = self.get_locator("department_filter")
        self.click(department_filter_locator)
        
        # Select department option
        department_option_locator = self.get_locator("department_option", department=department)
        self.click(department_option_locator)
        
        # Wait for results to update
        import time
        time.sleep(2)  # Allow filter to apply
    
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
