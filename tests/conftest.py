import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """
    Pytest fixture - provides WebDriver instance for each test
    Automatic setup and teardown
    Disable password save popup from browser
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # ===== DISABLE PASSWORD SAVE POPUP =====
    # Disable password manager
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    # Disable credential save
    options.add_argument("--disable-credential-manager")
    options.add_argument("--disable-credential-manager-ui")
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    
    # Yield driver to test
    yield driver
    
    # Cleanup - quit browser after test
    driver.quit()