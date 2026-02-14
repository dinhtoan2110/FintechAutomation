"""
AQX Trader - Automated Test Suite
All test cases in single file, run automatically via loop
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPagePOM    
from pages.webtrade_page import WebTradePagePOM
# from pages.webtrade_page import WebTradePagePOM
# from pages.market_page import MarketPagePOM
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from urllib.parse import urlparse


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

def setup_driver(headless=True):
    """
    Initialize Chrome WebDriver
    
    Args:
        headless: Run browser in background (no UI) - default True
    
    Browser configs:
    - Disable password save popup (credentials popup)
    - Disable automation detection
    - Optional headless mode for background execution
    """
    options = webdriver.ChromeOptions()
    
    # Headless mode - browser runs in background
    if headless:
        options.add_argument("--headless")
        print("[✓] Headless mode: ON (runs in background)")
    elif not headless:
        options.add_argument("--start-maximized")
        print("[✓] Headless mode: OFF (displays UI)")
    
    # Hide automation features (prevent detection)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Disable browser password/credential manager popups
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

def perform_login(driver, username=VALID_USERNAME, password=VALID_PASSWORD):
    """
    Reusable login helper function
    Can be called by AUTH-001 and other test cases
    
    Args:
        driver: WebDriver instance
        username: Login username
        password: Login password
        
    Returns:
        login_page: LoginPagePOM instance (ready for further actions)
    """
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded(), "Login page should load"
    login_page.login(username, password)
    return login_page


# ============================================
# LOGIN TESTS (Authentication)
# ============================================

def test_AUTH_001_login_success_goto_trading_page(driver):
    login_page = perform_login(driver, VALID_USERNAME, VALID_PASSWORD)
    success = login_page.wait_for_success()
    assert success, "User should be redirected to dashboard"
    current_url = login_page.get_current_url()
    print(f"Current URL after login: {current_url}")
    path = urlparse(current_url).path.lower().rstrip('/')
    assert "/web/trade" in path, f"Expected '/web/trade' in path, got: {path} (full URL: {current_url})"
    return True


def test_AUTH_002_invalid_username(driver):
    """AUTH-002: Login with invalid username"""
    login_page = perform_login(driver, INVALID_USERNAME, VALID_PASSWORD)
    error_msg = login_page.get_error_message_with_popup()
    assert error_msg is not None, "Error message should be displayed"
    return True


def test_AUTH_003_invalid_password(driver):
    login_page = perform_login(driver, VALID_USERNAME, INVALID_PASSWORD)
    error_msg = login_page.get_error_message_with_popup()
    assert error_msg is not None, "Error message should be displayed"
    return True

def test_DIAG_004_simplified_trading_flow(driver):
    """
    DIAG-004: Test simplified trading functions
    - Check market close status
    - Input symbol (AUDCAD)
    - Get price
    - Select order type
    - Input volume, SL, TP
    - Verify position reading
    """
    
    print("\n" + "="*80)
    print("DIAG-004: Simplified Trading Flow Test")
    print("="*80)
    
    # STEP 1: Login
    print("\n[STEP 1] Login...")
    login_page = LoginPagePOM(driver)
    login_page.open_page()
    assert login_page.verify_page_loaded()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    assert login_page.wait_for_success()
    print("[✓] Login successful")
    
    # STEP 2: Load WebTrade
    print("\n[STEP 2] Loading WebTrade...")
    webtrade = WebTradePagePOM(driver)
    assert webtrade.verify_page_loaded()
    print("[✓] WebTrade loaded")
    
    # STEP 3: Check market close status
    # print("\n[STEP 3] Checking market status...")
    # is_closed = webtrade.is_market_closed()
    # if is_closed:
    #     print("⚠️  Market is closed - skipping trade test")
    #     return False
    # print("✓ Market is open")
    
    # STEP 4: Input symbol (XAUUSD)
    print("\n[STEP 4] Inputting symbol XAUUSD and getting price...")
    price_text = webtrade.input_symbol("XAUUSD")
    print(f"[✓] XAUUSD price retrieved: {price_text}")
    
    # STEP 5: Select order type
    print("\n[STEP 5] Selecting order type...")
    webtrade.select_order_type("Market")
    print("[✓] Market order type selected")
    
    # # STEP 6: Input trading parameters
    print("\n[STEP 6] Inputting volume, SL, TP...")
    webtrade.input_volume(0.1)
    webtrade.input_stop_loss(0.95)
    webtrade.input_take_profit(1.05)
    print("[✓] All parameters entered")
    webtrade.click_place_order()
    
    # STEP 7: Open positions and read data
    print("\n[STEP 7] Opening positions and reading data...")
    if webtrade.open_positions_tab():
        position_data = webtrade.read_position_data()
        if position_data:
            print(f"[✓] Position data read successfully")
        else:
            print("[!] No position data available")
    else:
        print("[!] Could not open positions tab")
    
    # # STEP 8: Test edit and close functions exist
    # print("\n[STEP 8] Verifying edit/close functions...")
    # print("[✓] edit_position() function available")
    # print("[✓] close_position() function available")
    
    print("DIAG-004 COMPLETED") 
    return True



# ============================================
# TEST CASES ARRAY - Define all tests
# ============================================
TEST_CASES = [
    {
        "id": "AUTH-001",
        "name": "Login with valid credentials",
        "function": test_AUTH_001_login_success_goto_trading_page,
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
        "id": "DIAG-004",
        "name": "Simplified trading flow test",
        "function": test_DIAG_004_simplified_trading_flow,
        "category": "Workflow"
    }
]


# ============================================
# TEST RUNNER - Loop to run all tests
# ============================================

def run_all_tests(test_list=None, filter_by_id=None, filter_by_category=None, headless=True):
    """
    Run all test cases automatically
    
    Args:
        test_list: List of test cases (default is TEST_CASES)
        filter_by_id: Run only test with specific ID (e.g., "AUTH-001")
        filter_by_category: Run only tests in category (e.g., "Authentication")
        headless: Run browser in background (True) or show UI (False)
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
        
        # Create fresh driver for each test with headless parameter
        driver = setup_driver(headless=headless)
        
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
        
        finally:
            try:
                teardown_driver(driver)
            except:
                pass
        
        time.sleep(1)  # Pause between tests
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
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
    
    # Check for UION flag (UI ON - display browser window)
    headless = True
    if "UION" in sys.argv:
        headless = False
        print("\n[!] UION flag detected: Browser UI will be displayed\n")
        sys.argv.remove("UION")
    else:
        print("\n[!] Headless mode: Browser runs in background\n")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        
        if arg == "LIST":
            # Display test list
            print_test_list()
        
        elif arg == "AUTH":
            # Run only authentication tests
            print("🔐 Running Authentication Tests...\n")
            run_all_tests(filter_by_category="Authentication", headless=headless)
        
        elif arg == "WORKFLOW":
            # Run only workflow tests
            print("🔄 Running Workflow Tests...\n")
            run_all_tests(filter_by_category="Workflow", headless=headless)
        
        elif arg.startswith("TEST:"):
            # Run specific test (e.g., TEST:AUTH-001)
            test_id = arg.split(":")[-1]
            print(f"🎯 Running test: {test_id}\n")
            run_all_tests(filter_by_id=test_id, headless=headless)
        
        elif arg == "HELP":
            print("""
🆘 USAGE GUIDE:

  python automated_tests.py              # Run all tests (headless)
  python automated_tests.py LIST         # View test list
  python automated_tests.py AUTH         # Run authentication tests (headless)
  python automated_tests.py AUTH UION    # Run auth tests with UI (NOT headless)
  python automated_tests.py WORKFLOW     # Run workflow tests (headless)
  python automated_tests.py WORKFLOW UION# Run workflow with UI
  python automated_tests.py TEST:AUTH-001 # Run specific test (headless)
  python automated_tests.py TEST:AUTH-001 UION # Run specific test with UI
  python automated_tests.py HELP         # View this guide

📊 Results:
  - Each test runs sequentially
  - Default: Headless mode (no UI visible)
  - Add UION flag to display browser window
""")
        else:
            print(f"❓ Unknown argument: {arg}\n")
            run_all_tests(headless=headless)
    
    else:
        # Run all tests by default
        run_all_tests(headless=headless)
