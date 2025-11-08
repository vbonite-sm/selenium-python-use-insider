"""Utility decorators for test framework"""
import functools
import logging
import time
import allure
from datetime import datetime
from pathlib import Path
from config.config import Config

logger = logging.getLogger(__name__)


def log_action(func):
    """Decorator to log function execution"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func_name = func.__name__
        class_name = self.__class__.__name__
        logger.info(f"[{class_name}] Executing: {func_name} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(self, *args, **kwargs)
            logger.info(f"[{class_name}] Completed: {func_name}")
            return result
        except Exception as e:
            logger.error(f"[{class_name}] Failed: {func_name} - Error: {str(e)}")
            raise
    
    return wrapper


def screenshot_on_failure(func):
    """Decorator to capture screenshot on failure"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            if Config.SCREENSHOT_ON_FAILURE and hasattr(self, 'driver'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"{func.__name__}_{timestamp}.png"
                screenshot_path = Path(Config.SCREENSHOT_DIR) / screenshot_name
                
                # Create directory if not exists
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save screenshot
                self.driver.save_screenshot(str(screenshot_path))
                logger.error(f"Screenshot saved: {screenshot_path}")
                
                # Attach to Allure report
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
            
            raise
    
    return wrapper


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Decorator to retry function on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Max retries ({max_attempts}) reached for {func.__name__}")
                        raise
                    logger.warning(f"Retry {attempts}/{max_attempts} for {func.__name__}: {str(e)}")
                    time.sleep(delay)
        
        return wrapper
    return decorator


def allure_step(step_name=None):
    """Decorator to add Allure steps"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = step_name or func.__name__.replace('_', ' ').title()
            with allure.step(name):
                return func(*args, **kwargs)
        return wrapper
    return decorator
