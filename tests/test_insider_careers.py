import pytest
import allure
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
from pages.lever_page import LeverPage


@allure.feature("Insider Careers")
class TestInsiderCareers:
    """
    Test suite for Insider Careers QA job application flow
    Follows AAA (Arrange-Act-Assert) pattern
    """
    
    def test_01_home_page_loads(self, driver):
        """
        Test Step 1: Visit https://useinsider.com/ and verify home page opens
        """
        # Arrange
        home_page = HomePage(driver)
        
        # Act
        home_page.get()
        
        # Assert
        current_url = home_page.get_current_url()
        assert "useinsider.com" in current_url, \
            f"Expected URL to contain 'useinsider.com', got: {current_url}"
        
        allure.attach(current_url, name="Home Page URL", 
                     attachment_type=allure.attachment_type.TEXT)
    
    
    def test_02_careers_page_navigation_and_blocks(self, driver):
        """
        Test Step 2: Navigate to Careers page and verify Locations, Teams, 
        and Life at Insider blocks are present
        """
        # Arrange
        home_page = HomePage(driver)
        home_page.get()
        
        # Act
        careers_page = home_page.navigate_to_careers()
        
        # Assert
        careers_page.is_loaded()  # Verifies all three blocks internally
        current_url = careers_page.get_current_url()
        assert "careers" in current_url.lower(), \
            f"Expected URL to contain 'careers', got: {current_url}"
        
        allure.attach(current_url, name="Careers Page URL",
                     attachment_type=allure.attachment_type.TEXT)
    
    
    def test_03_filter_qa_jobs(self, driver):
        """
        Test Step 3: Go to QA careers page, click "See all QA jobs",
        filter by Istanbul/Turkiye and Quality Assurance department
        """
        # Arrange
        qa_page = QACareersPage(driver)
        qa_page.get()
        
        # Act
        qa_page.click_see_all_jobs()
        qa_page.filter_by_location("Istanbul, Turkiye")
        qa_page.filter_by_department("Quality Assurance")
        
        # Assert
        jobs = qa_page.get_job_listings()
        assert len(jobs) > 0, "No jobs found after applying filters"
        
        allure.attach(f"Total jobs found: {len(jobs)}", name="Job Count",
                     attachment_type=allure.attachment_type.TEXT)
    
    
    def test_04_verify_job_listings_criteria(self, driver):
        """
        Test Step 4: Verify all jobs contain "Quality Assurance" in Position,
        "Quality Assurance" in Department, and "Istanbul, Turkiye" in Location
        """
        # Arrange
        qa_page = QACareersPage(driver)
        qa_page.get()
        qa_page.click_see_all_jobs()
        qa_page.filter_by_location("Istanbul, Turkiye")
        qa_page.filter_by_department("Quality Assurance")
        
        # Act
        jobs = qa_page.get_job_listings()
        
        # Assert
        assert len(jobs) > 0, "No jobs found to verify"
        
        for idx, job in enumerate(jobs, 1):
            position = job['position']
            department = job['department']
            location = job['location']
            
            assert "quality assurance" in position.lower(), \
                f"Job {idx}: Position '{position}' does not contain 'Quality Assurance'"
            
            assert "quality assurance" in department.lower(), \
                f"Job {idx}: Department '{department}' does not contain 'Quality Assurance'"
            
            assert "istanbul" in location.lower() and "turkiye" in location.lower(), \
                f"Job {idx}: Location '{location}' does not contain 'Istanbul, Turkiye'"
        
        allure.attach(str(jobs), name="Verified Job Listings",
                     attachment_type=allure.attachment_type.JSON)
    
    
    def test_05_view_role_lever_redirect(self, driver):
        """
        Test Step 5: Click "View Role" button and verify redirect to 
        Lever Application form page
        """
        # Arrange
        qa_page = QACareersPage(driver)
        qa_page.get()
        qa_page.click_see_all_jobs()
        qa_page.filter_by_location("Istanbul, Turkiye")
        qa_page.filter_by_department("Quality Assurance")
        
        # Act
        qa_page.click_view_role_of_specific_job("istanbul-turkiye", "qualityassurance")

        # Assert
        lever_page = LeverPage(driver)
        lever_page.is_loaded()
        
        current_url = lever_page.get_current_url()
        assert "lever" in current_url.lower() or "jobs.lever.co" in current_url, \
            f"Expected Lever application page, got: {current_url}"
        
        allure.attach(current_url, name="Lever Application URL",
                     attachment_type=allure.attachment_type.TEXT)
    
    
    def test_06_complete_e2e_flow(self, driver):
        """
        Complete end-to-end test covering all steps from home page to Lever application
        """
        # ===== STEP 1: Home Page =====
        # Arrange
        home_page = HomePage(driver)
        
        # Act
        home_page.get()
        
        # Assert
        assert "useinsider.com" in home_page.get_current_url(), \
            "Home page did not load correctly"
        
        
        # ===== STEP 2: Careers Page =====
        # Act
        careers_page = home_page.navigate_to_careers()
        
        # Assert
        careers_page.is_loaded()
        assert "careers" in careers_page.get_current_url().lower(), \
            "Careers page did not load correctly"
        
        
        # ===== STEP 3: QA Jobs Page =====
        # Arrange
        qa_page = QACareersPage(driver)
        
        # Act
        qa_page.get()
        qa_page.click_see_all_jobs()
        qa_page.filter_by_location("Istanbul, Turkiye")
        qa_page.filter_by_department("Quality Assurance")
        
        # Assert - jobs are present
        jobs = qa_page.get_job_listings()
        assert len(jobs) > 0, "No jobs found after filtering"
        
        
        # ===== STEP 4: Verify Job Criteria =====
        # Assert - all jobs meet criteria
        for idx, job in enumerate(jobs, 1):
            assert "quality assurance" in job['position'].lower(), \
                f"Job {idx} position validation failed"
            assert "quality assurance" in job['department'].lower(), \
                f"Job {idx} department validation failed"
            assert "istanbul" in job['location'].lower() and "turkiye" in job['location'].lower(), \
                f"Job {idx} location validation failed"
        
        
        # ===== STEP 5: Lever Redirect =====
        # Act
        qa_page.click_view_role_of_specific_job("istanbul-turkiye", "qualityassurance")
        
        # Assert
        lever_page = LeverPage(driver)
        lever_page.is_loaded()
        current_url = lever_page.get_current_url()
        assert "lever" in current_url.lower() or "jobs.lever.co" in current_url, \
            f"Lever redirect failed. Current URL: {current_url}"
        
        allure.attach(current_url, name="Final Lever URL",
                     attachment_type=allure.attachment_type.TEXT)