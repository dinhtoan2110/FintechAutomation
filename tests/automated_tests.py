"""
AQX Trader - Automated Test Suite
All test cases in single file, run automatically via loop
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPagePOM
# from pages.webtrade_page import WebTradePagePOM
# from pages.market_page import MarketPagePOM
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# ============================================
# TEST DATA
# ============================================

VALID_USERNAME = "1001186"
VALID_PASSWORD = "pJoD#m8HB6#o"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "wrong_password"
TEST_SYMBOL = "AUDUSD"
TEST_VOLUME = "100"


# ============================================
# SETUP BROWSER DRIVER
# ============================================

def setup_driver():
    """Initialize Chrome WebDriver - Disable password save popup"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # ===== DISABLE PASSWORD SAVE POPUP =====
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-credential-manager")
    options.add_argument("--disable-credential-manager-ui")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    return driver


def teardown_driver(driver):
    """Close Chrome WebDriver"""
    driver.quit()


# ============================================
# LOGIN TESTS
# ============================================

def test_AUTH_001_login_success(driver):
    """AUTH-001: Successful login"""
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded(), "Login page should load"
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    success = login_page.wait_for_success()
    assert success, "User should be redirected to dashboard"
    return True


def test_AUTH_002_invalid_username(driver):
    """AUTH-002: Login with invalid username"""
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded()
    login_page.login(INVALID_USERNAME, VALID_PASSWORD)
    error_msg = login_page.get_error_message()
    assert error_msg is not None, "Error message should be displayed"
    return True


def test_AUTH_003_invalid_password(driver):
    """AUTH-003: Login with invalid password"""
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded()
    login_page.login(VALID_USERNAME, INVALID_PASSWORD)
    error_msg = login_page.get_error_message()
    assert error_msg is not None, "Error message should be displayed"
    return True


def test_AUTH_004_empty_credentials(driver):
    """AUTH-004: Login with empty credentials"""
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded()
    login_page.click_login()
    error_msg = login_page.get_error_message()
    assert error_msg is not None, "Error message should be displayed"
    return True


def test_AUTH_005_web_available(driver):
    """AUTH-005: Web server available"""
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded(), "Login page should load"
    current_url = login_page.get_current_url()
    assert "aqxtrader" in current_url.lower(), "Should be on AQX Trader domain"
    return True


# ============================================
# TEST CASES ARRAY - Define all tests
# ============================================

TEST_CASES = [
    {
        "id": "AUTH-001",
        "name": "Login with valid credentials",
        "function": test_AUTH_001_login_success,
        "category": "Authentication"
    },
    {
        "id": "AUTH-002",
        "name": "Login with invalid username",
        "function": test_AUTH_002_invalid_username,
        "category": "Authentication"
    },
    {
        "id": "AUTH-003",
        "name": "Login with invalid password",
        "function": test_AUTH_003_invalid_password,
        "category": "Authentication"
    },
    {
        "id": "AUTH-004",
        "name": "Login with empty credentials",
        "function": test_AUTH_004_empty_credentials,
        "category": "Authentication"
    },
    {
        "id": "AUTH-005",
        "name": "Web server available",
        "function": test_AUTH_005_web_available,
        "category": "Authentication"
    },
]


# ============================================
# TEST RUNNER - Loop to run all tests
# ============================================

def run_all_tests(test_list=None, filter_by_id=None, filter_by_category=None):
    """
    Run all test cases automatically
    
    Args:
        test_list: List of test cases (default is TEST_CASES)
        filter_by_id: Run only test with specific ID (e.g., "AUTH-001")
        filter_by_category: Run only tests in category (e.g., "Authentication")
    """
    if test_list is None:
        test_list = TEST_CASES
    
    # Filter tests if needed
    if filter_by_id:
        test_list = [t for t in test_list if t["id"] == filter_by_id]
    
    if filter_by_category:
        test_list = [t for t in test_list if t["category"] == filter_by_category]
    
    if not test_list:
        print("❌ No tests found to run!")
        return
    
    # Setup driver once
    driver = setup_driver()
    
    # Counters
    passed = 0
    failed = 0
    errors = []
    
    print("\n" + "="*80)
    print("🚀 STARTING TEST SUITE - {} Tests".format(len(test_list)))
    print("="*80)
    
    # Loop to run each test
    for idx, test in enumerate(test_list, 1):
        test_id = test["id"]
        test_name = test["name"]
        test_func = test["function"]
        
        print(f"\n[{idx}/{len(test_list)}] Running {test_id}: {test_name}")
        print("-" * 80)
        
        try:
            # Run test function
            result = test_func(driver)
            
            if result:
                print(f"✅ PASSED: {test_id}")
                passed += 1
            else:
                print(f"❌ FAILED: {test_id}")
                failed += 1
                errors.append(test_id)
        
        except AssertionError as e:
            print(f"❌ FAILED: {test_id}")
            print(f"   Error: {str(e)}")
            failed += 1
            errors.append((test_id, str(e)))
        
        except Exception as e:
            print(f"❌ ERROR: {test_id}")
            print(f"   Exception: {str(e)}")
            failed += 1
            errors.append((test_id, str(e)))
        
        time.sleep(1)  # Pause between tests
    
    # Cleanup
    teardown_driver(driver)
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total:  {len(test_list)}")
    print(f"🎯 Success Rate: {(passed/len(test_list)*100):.1f}%")
    
    if errors:
        print("\n❌ Failed Tests:")
        for error in errors:
            if isinstance(error, tuple):
                print(f"   - {error[0]}: {error[1]}")
            else:
                print(f"   - {error}")
    
    print("="*80 + "\n")
    
    return {
        "passed": passed,
        "failed": failed,
        "total": len(test_list),
        "errors": errors
    }


def print_test_list():
    """Print list of all tests"""
    print("\n" + "="*80)
    print("📋 AVAILABLE TESTS")
    print("="*80)
    
    # Group by category
    categories = {}
    for test in TEST_CASES:
        cat = test["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(test)
    
    for category, tests in categories.items():
        print(f"\n🏷️  {category}")
        for test in tests:
            print(f"   {test['id']:12} - {test['name']}")
    
    print(f"\n💡 Total: {len(TEST_CASES)} tests")
    print("="*80 + "\n")


# ============================================
# MAIN - Main program
# ============================================

if __name__ == "__main__":
    import sys
    
    print("\n╔════════════════════════════════════════════════════════════════════════════╗")
    print("║   AQX TRADER - AUTOMATED TEST SUITE                                       ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        
        if arg == "LIST":
            # Display test list
            print_test_list()
        
        elif arg == "AUTH":
            # Run only authentication tests
            print("🔐 Running Authentication Tests...\n")
            run_all_tests(filter_by_category="Authentication")
        
        elif arg == "WORKFLOW":
            # Run only workflow tests
            print("🔄 Running Workflow Tests...\n")
            run_all_tests(filter_by_category="Workflow")
        
        elif arg.startswith("TEST:"):
            # Run specific test (e.g., TEST:AUTH-001)
            test_id = arg.split(":")[-1]
            print(f"🎯 Running test: {test_id}\n")
            run_all_tests(filter_by_id=test_id)
        
        elif arg == "HELP":
            print("""
🆘 USAGE GUIDE:

  python automated_tests.py              # Run all tests
  python automated_tests.py LIST         # View test list
  python automated_tests.py AUTH         # Run only authentication tests
  python automated_tests.py WORKFLOW     # Run only workflow tests
  python automated_tests.py TEST:AUTH-001 # Run specific test
  python automated_tests.py HELP         # View this guide

📊 Results:
  - Each test runs sequentially
  - Automatically generate final report
  - Report failed tests if any
""")
        else:
            print(f"❓ Unknown argument: {arg}\n")
            run_all_tests()
    
    else:
        # Run all tests by default
        run_all_tests()
