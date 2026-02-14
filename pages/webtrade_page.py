"""
WebTradePagePOM - Page Object Model for Trading Page
Handles all interactions with the trading chart and order placement
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class WebTradePagePOM(BasePage):
    """POM for WebTrade page - trading interface"""
    
    # Locators
    CHART_CONTAINER = (By.XPATH, "//div[contains(@class,'chart') or contains(@class,'chart-container')]")
    TRADE_SYMBOL_INPUT = (By.XPATH, "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'symbol')]")
    PRICE_DISPLAY = (By.XPATH, "//div[contains(@class,'price') or contains(@class,'current-price')]")
    SYMBOL_DROPDOWN_RESULT = (By.XPATH, "(//div[@class='sc-197e9882-0 kJjEOX']//div)[1]")
    SYMBOL_OVERVIEW_TITLE = (By.XPATH, "//div[@data-testid='symbol-overview-id']")
    
    VOLUME_INPUT = (By.XPATH, "//input[@name='lotSize']")
    STOP_LOSS_INPUT = (By.XPATH, "//input[@name='stopLoss']")
    TAKE_PROFIT_INPUT = (By.XPATH, "//input[@name='takeProfit']")
    
    ORDER_TYPE_DROPDOWN = (By.XPATH, "(//div[text()='Market']/following-sibling::div)[1]")
    MARKET_OPTION = (By.XPATH, "//div[normalize-space(text())='Market']")
    LIMIT_OPTION = (By.XPATH, "//div[normalize-space(text())='Limit']")
    STOP_OPTION = (By.XPATH, "//div[normalize-space(text())='Stop']")
    STOP_LIMIT_OPTION = (By.XPATH, "//div[normalize-space(text())='Stop Limit']")
    
    BUY_BUTTON = (By.XPATH, "//button[@data-testid='trade-button-order-buy']")
    SELL_BUTTON = (By.XPATH, "//button[@data-testid='trade-button-order-sell']")
    PLACE_ORDER_BTN = (By.XPATH, "//button[@data-testid='trade-button-order']")
    
    OPEN_POSITIONS_TAB = (By.XPATH, "//div[contains(., 'Open Positions')]")
    POSITION_CONTAINER = (By.XPATH, "//div[@class='sc-dvmDTH isBNLJ']")
    
    EDIT_POSITION_BTN = (By.XPATH, "//button[contains(text(), 'Edit')]")
    CLOSE_POSITION_BTN = (By.XPATH, "//button[contains(text(), 'Close')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://aqxtrader.aquariux.com/web/trade"
    
    def open_page(self):
        """Open WebTrade page"""
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self.CHART_CONTAINER))
        print(f"[✓] WebTrade loaded")
        return self
    
    def verify_page_loaded(self):
        """Verify page loaded successfully"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.CHART_CONTAINER))
            self.wait.until(EC.visibility_of_element_located(self.BUY_BUTTON))
            self.wait.until(EC.visibility_of_element_located(self.SELL_BUTTON))
            return True
        except:
            return False
    
    def is_market_closed(self):
        """Check if market is closed"""
        try:
            btn_text = self.driver.find_element(*self.PLACE_ORDER_BTN).text.upper()
            if 'CLOSED' in btn_text:
                print("⚠️ Market closed")
                return True
            return False
        except:
            return False
    
    def input_symbol(self, symbol):
        """Input symbol and verify"""
        symbol_input = self.driver.find_element(*self.TRADE_SYMBOL_INPUT)
        symbol_input.clear()
        time.sleep(0.2)
        symbol_input.click()
        time.sleep(0.2)
        
        for char in symbol:
            symbol_input.send_keys(char)
            time.sleep(0.1)
        time.sleep(0.5)
        print(f"[✓] Symbol: {symbol}")
        
        try:
            self.driver.find_element(*self.SYMBOL_DROPDOWN_RESULT).click()
            time.sleep(0.8)
            title = self.driver.find_element(*self.SYMBOL_OVERVIEW_TITLE).text.strip()
            print(f"[✓] Verified: {title}")
        except:
            pass
        
        return self.get_current_price()
    
    def get_current_price(self):
        """Get current price"""
        try:
            return self.driver.find_element(*self.PRICE_DISPLAY).text.strip()
        except:
            return None
    
    def select_order_type(self, order_type='Market'):
        """Select order type"""
        self.driver.find_element(*self.ORDER_TYPE_DROPDOWN).click()
        time.sleep(0.3)
        
        options = {
            'market': self.MARKET_OPTION,
            'limit': self.LIMIT_OPTION,
            'stop': self.STOP_OPTION,
            'stop limit': self.STOP_LIMIT_OPTION
        }
        
        option_loc = options.get(order_type.lower())
        if not option_loc:
            raise ValueError(f"Unknown order type: {order_type}")
        
        self.driver.find_element(*option_loc).click()
        print(f"[✓] Order: {order_type}")
        time.sleep(0.3)
        return self
    
    def input_volume(self, volume):
        """Input trading volume"""
        self.driver.find_element(*self.VOLUME_INPUT).clear()
        self.driver.find_element(*self.VOLUME_INPUT).send_keys(str(volume))
        print(f"[✓] Volume: {volume}")
        return self
    
    def input_stop_loss(self, price):
        """Input stop loss price"""
        self.driver.find_element(*self.STOP_LOSS_INPUT).clear()
        self.driver.find_element(*self.STOP_LOSS_INPUT).send_keys(f"{float(price):.2f}")
        print(f"[✓] SL: {price:.2f}")
        return self
    
    def input_take_profit(self, price):
        """Input take profit price"""
        self.driver.find_element(*self.TAKE_PROFIT_INPUT).clear()
        self.driver.find_element(*self.TAKE_PROFIT_INPUT).send_keys(f"{float(price):.2f}")
        print(f"[✓] TP: {price:.2f}")
        return self
    
    def place_buy_order(self):
        """Place BUY order"""
        btn = self.driver.find_element(*self.BUY_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", btn)
        time.sleep(0.2)
        btn.click()
        print("[✓] BUY")
        time.sleep(0.5)
        return True
    
    def place_sell_order(self):
        """Place SELL order"""
        btn = self.driver.find_element(*self.SELL_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView();", btn)
        time.sleep(0.2)
        btn.click()
        print("[✓] SELL")
        time.sleep(0.5)
        return True
    
    def click_place_order(self):
        """Confirm order placement"""
        self.driver.find_element(*self.PLACE_ORDER_BTN).click()
        print("[✓] Order confirmed")
        time.sleep(0.5)
        return True
    
    def open_positions_tab(self):
        """Open positions tab"""
        self.driver.find_element(*self.OPEN_POSITIONS_TAB).click()
        print("[✓] Positions tab")
        time.sleep(0.5)
        return True
    
    def read_position_data(self):
        """Read position data"""
        try:
            text = self.driver.find_element(*self.POSITION_CONTAINER).text.strip()
            if text:
                print(f"[✓] Position data retrieved")
                return text
        except:
            pass
        return None
    
    def edit_position(self):
        """Edit position"""
        self.driver.find_element(*self.EDIT_POSITION_BTN).click()
        print("[✓] Edit mode")
        time.sleep(0.5)
        return True
    
    def close_position(self):
        """Close position"""
        self.driver.find_element(*self.CLOSE_POSITION_BTN).click()
        print("[✓] Closed")
        time.sleep(0.5)
        return True
