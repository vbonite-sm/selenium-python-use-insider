import os
from enum import Enum
from typing import Dict, Any

class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"

class Config:
    """Central configuration for the test framework"""
    
    # URLs - only what we need
    BASE_URL = "https://useinsider.com"
    CAREERS_QA_URL = f"{BASE_URL}/careers/quality-assurance/"
    
    # Browser settings
    BROWSER = Browser[os.getenv("BROWSER", "CHROME").upper()]
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Timeouts
    DEFAULT_TIMEOUT = 30
    PAGE_LOAD_TIMEOUT = 60
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_DIR = "screenshots"
    
    # Reporting
    ALLURE_RESULTS_DIR = "reports/allure-results"
    
    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """Get browser-specific options"""
        if cls.BROWSER == Browser.CHROME:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if cls.HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")  # Explicit size
            options.add_argument("--start-maximized")        # Start maximized
            return options
        
        elif cls.BROWSER == Browser.FIREFOX:
            from selenium.webdriver.firefox.options import Options
            options = Options()
            if cls.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--width=1920")   # Explicit size
            options.add_argument("--height=1080")
            return options
        
        return None