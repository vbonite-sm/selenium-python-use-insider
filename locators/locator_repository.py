"""Locator repository for managing test locators"""
import json
from typing import Tuple, Dict
from pathlib import Path


class LocatorRepository:
    """Repository pattern for managing locators"""
    
    def __init__(self, locator_file: str = "locators/locators.json"):
        self._locators: Dict[str, Dict[str, Tuple]] = {}
        self._load_locators(locator_file)
    
    def _load_locators(self, locator_file: str):
        """Load locators from JSON file"""
        file_path = Path(locator_file)
        if not file_path.exists():
            raise FileNotFoundError(f"Locator file not found: {locator_file}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            for page, elements in data.items():
                self._locators[page] = {}
                for elem_name, locator_data in elements.items():
                    # Convert list to tuple (By strategy, locator value)
                    self._locators[page][elem_name] = tuple(locator_data)
    
    def get(self, page_name: str, element_name: str, **kwargs) -> Tuple:
        """Get locator for a specific element with support for dynamic placeholders"""
        try:
            locator = self._locators[page_name][element_name]
            # Handle dynamic locators
            if kwargs:
                by, value = locator
                for key, val in kwargs.items():
                    value = value.replace(f'{{{key}}}', str(val))
                return (by, value)
            return locator
        except KeyError:
            raise ValueError(f"Locator not found: {page_name}.{element_name}")

    def get_all(self, page_name: str) -> Dict[str, Tuple]:
        """Get all locators for a page"""
        return self._locators.get(page_name, {})


# Singleton instance
locator_repo = LocatorRepository()
