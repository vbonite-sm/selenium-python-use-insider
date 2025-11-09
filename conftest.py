import pytest
import logging
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
from pathlib import Path
from config.config import Config, Browser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser in headless mode: true or false"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to initialize and teardown WebDriver
    Scope: function (new browser instance for each test)
    """
    # Get command line options
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless").lower() == "true"
    
    # Update config
    Config.BROWSER = Browser[browser_name.upper()]
    Config.HEADLESS = headless
    
    logger.info(f"Initializing {browser_name} browser (headless={headless})")
    
    # Initialize driver based on browser type
    if Config.BROWSER == Browser.CHROME:
        options = Config.get_browser_options()
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif Config.BROWSER == Browser.FIREFOX:
        options = Config.get_browser_options()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Set window size (works in all environments)
    driver.set_window_size(1920, 1080)
    
    # Set page load timeout
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    
    # Attach browser info to Allure report
    allure.attach(
        f"Browser: {browser_name}\nHeadless: {headless}",
        name="Browser Configuration",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield driver
    
    # Teardown
    logger.info("Closing browser")
    driver.quit()


@pytest.fixture(scope="function", autouse=True)
def test_setup(request, driver):
    """
    Auto-fixture that runs before/after each test
    Handles screenshots on failure
    """
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    yield
    
    # Check if test failed
    if request.node.rep_call.failed:
        logger.error(f"Test failed: {test_name}")
        
        # Take screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{timestamp}.png"
        screenshot_path = Path(Config.SCREENSHOT_DIR) / screenshot_name
        
        # Create directory if not exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save screenshot
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        # Attach to Allure report
        allure.attach(
            driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        
        # Attach page source
        allure.attach(
            driver.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.HTML
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution result
    Needed for test_setup fixture to know if test failed
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)