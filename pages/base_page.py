"""
BasePage - Base class for all Page Objects
Base class containing common methods used in all Page Objects
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Base class for all Page Object Models
    Contains common methods using WebDriverWait and expected conditions
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    def type(self, locator, text):
        """
        Wait for element to be visible, clear it, and enter text
        
        Args:
            locator: Tuple (By method, selector string)
            text: Text to input
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """
        Wait for element to be visible then get its text
        
        Args:
            locator: Tuple (By method, selector string)
            
        Returns:
            str: Text content
        """
        return self.wait.until(EC.visibility_of_element_located(locator)).text
    
    def wait_until_disappear(self, locator):
        """
        Wait for element to disappear
        
        Args:
            locator: Tuple (By method, selector string)
        """
        self.wait.until(EC.invisibility_of_element_located(locator))
    
    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator: Tuple (By method, selector string)
            timeout: Maximum wait time
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """
        Check if element is present in DOM
        
        Args:
            locator: Tuple (By method, selector string)
            timeout: Maximum wait time
            
        Returns:
            bool: True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False
