"""
WebTradePagePOM - Page Object Model for Trading Page
Handles all interactions with the trading chart and order placement
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time
import re


class WebTradePagePOM(BasePage):
    """POM for WebTrade page - trading interface"""
    
    # Locators
    CHART_CONTAINER = (By.XPATH, "//div[contains(@class,'chart') or contains(@class,'chart-container')]")
    TRADE_SYMBOL_INPUT = (By.XPATH, "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'symbol')]")
    PRICE_DISPLAY = (By.XPATH, "//div[@class='sc-bca4f92-0 kkrurn']//div)[2]]")
    CURRENT_TIME_DISPLAY = (By.XPATH, "//div[@class='sc-5d3a04eb-0 fsRkWV']/following-sibling::div[1]")


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

    EXPIRY_TYPE_DROPDOWN = (By.XPATH, "(//div[text()='Good Till Day']/following-sibling::div")
    GOOD_TILL_CANCELED_OPTION = (By.XPATH, "//div[normalize-space(text())='Good Till Canceled']")
    GOOD_TILL_DAY_OPTION = (By.XPATH, "(//div[normalize-space(text())='Good Till Day']")
    SPECIFIED_DATE_AND_TIME_OPTION = (By.XPATH, "//div[normalize-space(text())='Specified Date and Time']")
    SPECIFIED_DATE_OPTION = (By.XPATH, "//div[normalize-space(text())='Specified Date']")
    EXPIRY_DATE_INPUT = (By.XPATH, "(//div[@data-testid='trade-input-expiry-date']//div)[1]")
    EXPIRY_TIME_INPUT = (By.XPATH, "(//div[@data-testid='trade-input-expiry-time']//div)[1]")
    
    BUY_BUTTON = (By.XPATH, "//button[@data-testid='trade-button-order-buy']")
    SELL_BUTTON = (By.XPATH, "//button[@data-testid='trade-button-order-sell']")
    PLACE_ORDER_BTN = (By.XPATH, "//button[@data-testid='trade-button-order']")
    
    OPEN_POSITIONS_TAB = (By.XPATH, "//div[contains(., 'Open Positions')]")
    PENDING_ORDERS_TAB = (By.XPATH, "//div[contains(., 'Pending Orders')]")
    POSITIONS_HISTORY_TAB = (By.XPATH, "//div[contains(., 'Positions History')]")
    POSITION_CONTAINER = (By.XPATH, "//div[@class='sc-dvmDTH isBNLJ']")
    
    EDIT_POSITION_BTN = (By.XPATH, "//button[@data-testid='asset-open-button-edit']")
    CLOSE_POSITION_BTN = (By.XPATH, "//button[@data-testid='asset-open-button-close']")
    BULK_CLOSE_BTN = (By.XPATH, "//div[@data-testid='bulk-close']")

    NOTIFICATION_SELECTOR = (By.XPATH, "//div[@data-testid='notification-selector']")
    NOTIFICATION_LIST_RESULT_ITEM = (By.XPATH, "//div[@data-testid='notification-list-result-item']")
    NOTIFICATION_TITLES = (By.XPATH, "//div[@data-testid='notification-list-result-item-title']")
    
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
        
    def click_buy(self):
        """Click the buy button"""
        try:
            self.driver.find_element(*self.BUY_BUTTON).click()
            print(f"[✓] Clicked Buy button")
            return True
        except:
            return False
        
    def click_sell(self):
        """Click the sell button"""
        try:
            self.driver.find_element(*self.SELL_BUTTON).click()
            print(f"[✓] Clicked Sell button")
            return True
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
        
    def get_current_day(self):
        """Get current day"""
        try:
            return self.driver.find_element(*self.CURRENT_TIME_DISPLAY).text.strip()
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
    
    def select_order_expiry(self, expiry_type='Good Till Day'):
        """Select order expiry type"""
        self.driver.find_element(*self.EXPIRY_TYPE_DROPDOWN).click()
        time.sleep(0.3)
        
        options = {
            'Good Till Canceled': self.GOOD_TILL_CANCELED_OPTION,
            'Good Till Day': self.GOOD_TILL_DAY_OPTION,
            'Specified Date and Time': self.SPECIFIED_DATE_AND_TIME_OPTION,
            'Specified Date': self.SPECIFIED_DATE_OPTION
        }
        
        option_loc = options.get(expiry_type)
        if not option_loc:
            raise ValueError(f"Unknown expiry type: {expiry_type}")
        
        self.driver.find_element(*option_loc).click()
        print(f"[✓] Expiry: {expiry_type}")
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

    def input_expiry_date(self, date_str: str):
        """Input expiry date string into expiry date field."""
        try:
            self._click_when_clickable(self.EXPIRY_DATE_INPUT)
            time.sleep(0.2)
            el = self.driver.switch_to.active_element
            try:
                el.clear()
            except Exception:
                pass
            el.send_keys(date_str)
            el.send_keys(Keys.ENTER)
            print(f"[✓] Expiry date set: {date_str}")
        except Exception as e:
            print(f"[!] input_expiry_date failed: {e}")
            raise
        return self

    def input_expiry_time(self, time_str: str):
        """Input expiry time string into expiry time field."""
        try:
            self._click_when_clickable(self.EXPIRY_TIME_INPUT)
            time.sleep(0.2)
            el = self.driver.switch_to.active_element
            try:
                el.clear()
            except Exception:
                pass
            el.send_keys(time_str)
            el.send_keys(Keys.ENTER)
            print(f"[✓] Expiry time set: {time_str}")
        except Exception as e:
            print(f"[!] input_expiry_time failed: {e}")
            raise
        return self

    def set_expiry_next_day_noon(self):
        """Set expiry to next day at 12:00."""
        return self.set_expiry_plus_days(1, "12:00")
    
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

    def open_pending_order_tab(self):
        """Open pending order tab"""
        self.driver.find_element(*self.PENDING_ORDERS_TAB).click()
        print("[✓] Pending order tab")
        time.sleep(0.5)
        return True

    def open_history_tab(self):
        """Open history tab"""
        self.driver.find_element(*self.POSITIONS_HISTORY_TAB).click()
        print("[✓] History tab")
        time.sleep(0.5)
        return True
    
    def read_position_data(self):
        """Read position data from positions table"""
        try:
            text = self.driver.find_element(*self.POSITION_CONTAINER).text.strip()
            if text:
                data = self._parse_position_table(text)
                titles = self._get_notification_titles(open_panel=True)
                data['title'] = titles[0] if titles else None
                print(f"[✓] Position data retrieved")
                return data
        except Exception as e:
            print(f"[!] read_position_data failed: {e}")
        return None

    def read_information(self):
        """Read notification information from notification panel."""
        try:
            self.driver.find_element(*self.NOTIFICATION_SELECTOR).click()
            time.sleep(2.0)
            
            scroller = self.driver.find_element(By.XPATH, "//div[@data-testid='virtuoso-scroller']")
            height = self.driver.execute_script("return arguments[0].scrollHeight;", scroller)
            
            for i in range(10):
                self.driver.execute_script(f"arguments[0].scrollTop = {int(height * i / 10)};", scroller)
                time.sleep(0.5)
            
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroller)
            time.sleep(1.5)
            
            results = self._collect_notification_entries()
            print(f"[✓] {len(results)} notifications")
            return results
        except Exception as e:
            print(f"[!] read_information failed: {e}")
            return []
    
    def _collect_notification_entries(self):
        """Collect and parse notification entries from scroller."""
        items = self.driver.find_elements(*self.NOTIFICATION_LIST_RESULT_ITEM)
        
        if not items:
            return []
        
        titles = self._get_notification_titles()
        results = []
        
        for idx, item in enumerate(items):
            text = item.text.strip()
            if text:
                data = self._parse_notification_text(text)
                data['title'] = titles[idx] if idx < len(titles) else None
                results.append(data)
        
        return results

    def _get_notification_titles(self, open_panel=False):
        """Get notification titles."""
        if open_panel:
            self.driver.find_element(*self.NOTIFICATION_SELECTOR).click()
            time.sleep(0.3)
        
        elements = self.driver.find_elements(*self.NOTIFICATION_TITLES)
        print(f"[DEBUG] Found {len(elements)} notification titles")
        return [el.text.strip() for el in elements if el.text.strip()]

    def _parse_notification_text(self, text):
        """Parse notification text to structured data."""
        data = {'date': None, 'order_id': None, 'symbol': None, 
                'type': None, 'volume': None, 'profit': None}
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        seen_at = False
        
        for line in lines:
            if line.lower() == 'at':
                seen_at = True
            elif re.match(r'\d{4}-\d{2}-\d{2}', line):
                data['date'] = line.split()[0]
            elif 'Order No.' in line:
                if match := re.search(r'Order No\.\s*(\d+)', line):
                    data['order_id'] = match.group(1)
                if match := re.search(r'\b([A-Z]{6})\b', line):
                    data['symbol'] = match.group(1)
            elif line in ['BUY', 'SELL']:
                data['type'] = line
            elif 'volume' in line.lower():
                if match := re.search(r'(\d+\.\d+)', line):
                    data['volume'] = match.group(1)
            elif re.match(r'^[+-]?\d+\.\d+$', line) and not seen_at and not data['profit']:
                data['profit'] = line
        return data


    def edit_position(self, order_id=None, volume=None, stop_loss=None, take_profit=None):
        """
        Edit an open position
        
        Args:
            order_id: Optional order ID to edit specific position
            volume: Optional new volume to set
            stop_loss: Optional new stop loss price
            take_profit: Optional new take profit price
        
        Returns:
            self: For method chaining
        """
        try:
            if order_id:
                scoped_locator = (By.XPATH, f"//div[contains(., '{order_id}')]//button[@data-testid='asset-open-button-edit']")
                try:
                    self._click_when_clickable(scoped_locator, timeout=3)
                    print(f"[✓] Edit button clicked for Order {order_id}")
                except (TimeoutException, NoSuchElementException):
                    self._click_when_clickable(self.EDIT_POSITION_BTN)
                    print(f"[✓] Edit button clicked for Order {order_id} (fallback)")
            else:
                self._click_when_clickable(self.EDIT_POSITION_BTN)
                print(f"[✓] Edit button clicked")

            time.sleep(0.5)

            if volume is not None:
                try:
                    vol_input = (By.XPATH, "//input[@name='lotSize' or @data-testid='edit-volume-input']")
                    el = self.driver.find_element(*vol_input)
                    el.clear()
                    el.send_keys(str(volume))
                    print(f"[✓] Updated volume: {volume}")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"[!] Volume update failed: {e}")

            if stop_loss is not None:
                try:
                    sl_input = (By.XPATH, "//input[@name='stopLoss' or @data-testid='edit-sl-input']")
                    el = self.driver.find_element(*sl_input)
                    el.clear()
                    el.send_keys(f"{float(stop_loss):.2f}")
                    print(f"[✓] Updated SL: {stop_loss:.2f}")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"[!] SL update failed: {e}")

            if take_profit is not None:
                try:
                    tp_input = (By.XPATH, "//input[@name='takeProfit' or @data-testid='edit-tp-input']")
                    el = self.driver.find_element(*tp_input)
                    el.clear()
                    el.send_keys(f"{float(take_profit):.2f}")
                    print(f"[✓] Updated TP: {take_profit:.2f}")
                    time.sleep(0.2)
                except Exception as e:
                    print(f"[!] TP update failed: {e}")

            if any([volume is not None, stop_loss is not None, take_profit is not None]):
                try:
                    confirm_btn = (By.XPATH, "//button[contains(text(), 'Update') or contains(text(), 'Save') or contains(text(), 'Confirm')]")
                    self._click_when_clickable(confirm_btn, timeout=3)
                    print("[✓] Edit confirmed")
                    time.sleep(0.5)
                except TimeoutException:
                    print("[!] No confirm button found or edit completed")

            return self
        except Exception as e:
            print(f"[!] Edit position failed: {e}")
            raise
    
    def close_position(self, order_id=None, confirm=True):
        """
        Close an open position
        
        Args:
            order_id: Optional order ID to close specific position (if multiple positions exist)
            confirm: Whether to confirm close dialog (default True)
        
        Returns:
            self: For method chaining
        """
        try:
            if order_id:
                scoped_locator = (By.XPATH, f"//div[contains(., '{order_id}')]//button[@data-testid='asset-open-button-close']")
                try:
                    self._click_when_clickable(scoped_locator, timeout=3)
                    print(f"[✓] Close button clicked for Order {order_id}")
                except (TimeoutException, NoSuchElementException):
                    self._click_when_clickable(self.CLOSE_POSITION_BTN)
                    print(f"[✓] Close button clicked for Order {order_id} (fallback)")
            else:
                self._click_when_clickable(self.CLOSE_POSITION_BTN)
                print(f"[✓] Close button clicked")

            time.sleep(0.5)

            if confirm:
                confirm_xpath = "//button[contains(text(), 'Close') or contains(text(), 'Confirm') or contains(text(), 'OK')]"
                try:
                    self._click_when_clickable((By.XPATH, confirm_xpath), timeout=3)
                    print("[✓] Close confirmed")
                    time.sleep(1.0)
                except TimeoutException:
                    print("[✓] Position closed (no confirmation dialog found)")

            return self
        except Exception as e:
            print(f"[!] Close position failed: {e}")
            raise
    
    def bulk_close_positions(self, confirm=True):
        """
        Close all open positions at once using bulk close feature
        
        Args:
            confirm: Whether to confirm bulk close dialog (default True)
        
        Returns:
            self: For method chaining
        """
        try:
            self._click_when_clickable(self.BULK_CLOSE_BTN)
            print("[✓] Bulk close button clicked")
            time.sleep(0.5)

            if confirm:
                confirm_xpath = "//button[contains(text(), 'Close All') or contains(text(), 'Confirm') or contains(text(), 'OK')]"
                try:
                    self._click_when_clickable((By.XPATH, confirm_xpath), timeout=4)
                    print("[✓] Bulk close confirmed - all positions closed")
                    time.sleep(1.0)
                except TimeoutException:
                    print("[*] No confirmation dialog for bulk close")

            return self
        except Exception as e:
            print(f"[!] Bulk close failed: {e}")
            raise
    def _parse_position_table(self, text):
        """Parse position data from table format."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        headers = ['Open Date', 'Order No.', 'Symbol', 'Type', 'Profit/Loss', 'Volume', 
                   'Units', 'Entry Price', 'Current Price', 'Take Profit', 'Stop Loss', 
                   'Swap', 'Comment', 'Track', 'Edit', 'Close']
        
        header_end = -1
        for i, header in enumerate(headers):
            if header in lines:
                header_end = max(header_end, lines.index(header))
        
        if header_end == -1:
            return self._parse_notification_text(text)
        
        data_values = lines[header_end + 1:]
        
        result = {
            'raw': text,
            'date': None,
            'order_id': None,
            'symbol': None,
            'type': None,
            'volume': None,
            'profit': None,
        }
        try:
            if len(data_values) > 0 and re.match(r'\d{4}-\d{2}-\d{2}', data_values[0]):
                result['date'] = data_values[0]
            if len(data_values) > 1 and data_values[1].isdigit():
                result['order_id'] = data_values[1]
            if len(data_values) > 2:
                result['symbol'] = data_values[2]
            if len(data_values) > 3 and data_values[3] in ['BUY', 'SELL', 'Buy', 'Sell']:
                result['type'] = data_values[3]
            if len(data_values) > 4:
                result['profit'] = data_values[4]
            if len(data_values) > 5:
                result['volume'] = data_values[5]
        except Exception as e:
            print(f"[!] Position table parsing error: {e}")
        
        return result

    def _click_when_clickable(self, locator, timeout=5):
        el = self.wait.until(EC.element_to_be_clickable(locator), message=f"{locator} not clickable")
        el.click()
        return el
    