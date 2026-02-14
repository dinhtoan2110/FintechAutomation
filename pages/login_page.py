"""
LoginPagePOM - Page Object Model for Login Page
Handles all interactions with AQX Trader login page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
import time

class LoginPagePOM(BasePage):
    
    # ============================================
    # 1️⃣ LOCATORS (Element locators)
    # ============================================
    
    USERNAME_FIELD = (By.NAME, "userId")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@data-testid='login-submit']")
    ERROR_MESSAGE = (By.XPATH, "//div[@id='root']/div[1]")
    LOGIN_FORM = (By.XPATH, "//div[normalize-space(text())='Log in']")
    PAGE_TITLE_BEGIN = (By.XPATH, "//span[contains(.,'AQX Announcement: Welcome to AQX Trader!')]")
    POPUP_ERROR_TEXT_CREDENTIALS = (By.XPATH, "//div[contains(text(), 'Invalid credentials')]")

    # ============================================
    # 2️⃣ INITIALIZATION (__init__)
    # ============================================

    def __init__(self, driver):
        super().__init__(driver) 
        self.url = "https://aqxtrader.aquariux.com"
    
    # ============================================
    # 3️⃣ METHODS (Actions)
    # ============================================
    
    def open_page(self):
        """Open login page"""
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))
        print(f"[✓] Opened login page: {self.url}")
        return self
    
    def goto_page(self, url="https://aqxtrader.aquariux.com/web/login"):
        """Navigate to specific URL with login page path"""
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))
        print(f"[✓] Navigated to: {url}")
        return self
    
    def enter_username(self, username):
        """Enter username into username field"""
        self.type(self.USERNAME_FIELD, username)
        print(f"[✓] Entered username: {username}")
        return self
    
    def enter_password(self, password):
        """Enter password into password field"""
        self.type(self.PASSWORD_FIELD, password)
        print(f"[✓] Entered password")
        return self
    
    def click_login(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        print("[✓] Clicked login button")
        time.sleep(2)
        return self
    
    def get_error_message_with_popup(self, timeout=10):
        """Get error message text from popup if displayed"""
        try:
            error = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.POPUP_ERROR_TEXT_CREDENTIALS)
            )
            error_text = error.text
            print(f"[!] Popup error message: {error_text}")
            return error_text
        except Exception as e:
            print(f"[!] Popup error message not found: {str(e)}")
            return None
    
    def login(self, username, password):
        """Complete login process with username and password"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def verify_page_loaded(self):
        """Verify login page is loaded correctly"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
            print("[✓] Login page loaded correctly")
            return True
        except Exception as e:
            print(f"[✗] Login page not loaded: {str(e)}")
            return False
    
    def wait_for_success(self, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout)
            page_title = wait.until(
                EC.visibility_of_element_located(self.PAGE_TITLE_BEGIN)
            )
            print(f"[✓] Login successful - PAGE_TITLE_BEGIN found: {page_title.text}")
            return True
        except Exception as e:
            print(f"[✗] Login failed or timeout - PAGE_TITLE_BEGIN not found")
            print(f"    Error: {str(e)}")
            return False
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh the page"""
        self.driver.refresh()
        self.verify_page_loaded()
        print("[✓] Page refreshed")
        return self
