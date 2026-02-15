# AQX Trader - Automated Testing Framework

## 📋 Overview

This is a comprehensive **automated testing framework** built with **Python** and **Selenium WebDriver** for testing the AQX Trader web trading platform. The framework implements the **Page Object Model (POM)** design pattern to ensure maintainable, scalable, and reusable test automation code.

## ✨ Features

- **56 Automated Test Cases** covering all major trading functionalities
- **Page Object Model (POM)** architecture for better code organization
- **Comprehensive Order Type Coverage**:
  - Market Orders (BUY/SELL)
  - Limit Orders (BUY/SELL)
  - Stop Orders (BUY/SELL)
  - Stop Limit Orders (BUY/SELL)
- **Dynamic Wait Strategies** for reliable test execution
- **Detailed Logging** and console output
- **Bulk Operations** testing (bulk close, multiple positions)
- **Position Management** (create, edit, close orders)

## 🏗️ Project Structure


Fintech_Automation/
├── FintechAutomation/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py          # Base page with common methods
│   │   ├── login_page.py         # Login page POM
│   │   ├── webtrade_page.py      # Trading page POM
│   ├── tests/
│   │   ├── automated_tests.py    # Main test suite (56 tests)
│   │   ├── conftest.py           # Pytest configuration
│   │   └── extra_test.py         # Additional test scenarios
│   └── requirements.txt          # Python dependencies
└── .venv/                        # Virtual environment

## 🔧 Prerequisites
Before running the automated tests, ensure you have the following installed:
- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **Google Chrome Browser** (latest version)
- **pip** (Python package installer)
- **Git** (optional, for version control)

## 📦 Installation

### Step 1: Clone or Download the Project
git clone https://github.com/dinhtoan2110/FintechAutomation.git

### Step 2: Create Virtual Environment
# Create virtual environment
python -m venv .venv

### Step 3: Install Dependencies
pip install -r requirements.txt

## 🚀 Running Tests
### Run All Tests (Headless Mode)
cd ~/tests
python automated_tests.py

**Output:**
================================================================================
🚀 STARTING TEST SUITE - 56 Tests
================================================================================
[1/56] Running AUTH-001: Login with valid credentials
✅ PASSED: AUTH-001


### Run All Tests (With UI - Browser Visible)

```bash
python automated_tests.py UION
```

> **Note:** `UION` = UI ON, displays the browser window during test execution

### Run Specific Test Case

```bash
# Run single test by ID
python automated_tests.py TEST:AUTH-001

# Run with UI visible
python automated_tests.py TEST:AUTH-001 UION
```
**Available Categories:**
- Authentication
- Market Buy / Market Sell
- Limit Buy / Limit Sell
- Stop Buy / Stop Sell
- Stop Limit Buy / Stop Limit Sell
- History

## 📊 Test Cases Overview

### Total: 56 Test Cases

| Category | Count | Test IDs | Description |
|----------|-------|----------|-------------|
| **Authentication** | 3 | AUTH-001 to AUTH-003 | Login validation tests |
| **Market Buy** | 5 | MO-BUY-001 to MO-BUY-005 | Market order buy tests |
| **Limit Buy** | 7 | LO-BUY-001 to LO-BUY-007 | Limit order buy tests |
| **Stop Buy** | 7 | SO-BUY-001 to SO-BUY-007 | Stop order buy tests |
| **Stop Limit Buy** | 7 | SLO-BUY-001 to SLO-BUY-007 | Stop limit buy tests |
| **Market Sell** | 5 | MO-SELL-001 to MO-SELL-005 | Market order sell tests |
| **Limit Sell** | 7 | LO-SELL-001 to LO-SELL-007 | Limit order sell tests |
| **Stop Sell** | 7 | SO-SELL-001 to SO-SELL-007 | Stop order sell tests |
| **Stop Limit Sell** | 7 | SLO-SELL-001 to SLO-SELL-007 | Stop limit sell tests |
| **History** | 1 | HIS-001 | Order history verification |

### Example Test Cases

#### AUTH-001: Login with Valid Credentials
```python
def test_AUTH_001_login_success_goto_trading_page(driver):
    """Verify successful login redirects to trading page"""
    # Test implementation...
```

#### MO-BUY-001: Market Buy - Standard Entry
```python
def test_MO_BUY_001_market_buy_standard_entry(driver):
    """Create market buy order with SL/TP and verify"""
    # Test implementation...
```

## 📝 Test Execution Flow
### Standard Test Flow

```
1. Setup Driver
   ↓
2. Navigate to Login Page
   ↓
3. Enter Credentials
   ↓
4. Verify Login Success
   ↓
5. Navigate to Trading Page
   ↓
6. Execute Trading Actions
   ↓
7. Verify Results
   ↓
8. Cleanup/Close Positions
   ↓
9. Teardown Driver
```

### Buy Order Test Flow Example

```python
1. Login to platform
2. Click BUY button
3. Input symbol (e.g., XAUUSD)
4. Select order type (Market/Limit/Stop/Stop Limit)
5. Input volume
6. Set Stop Loss (last_price * 0.99)
7. Set Take Profit (last_price * 1.03)
8. Place order
9. Verify position created
10. Close position
11. Verify position closed
```

**Created with** LE DINH TOAN **using Python & Selenium**

**Last Updated:** 15 February 2026
