import os
import sys
import time
import customtkinter as ctk
import schedule
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import requests
from urllib.parse import urlencode, urlparse

class NSEDownloader:
    def __init__(self, gui=None):
        # URLs for both websites
        self.urls = {
            'nifty50': "https://www.nseindia.com/api/equity-stock-indices?csv=true&index=NIFTY%2050&selectValFormat=crores",
            'nifty500': " https://www.nseindia.com/api/equity-stock-indices?csv=true&index=NIFTY%20500&selectValFormat=crores",
           
            'market_indices': "https://www.nseindia.com/api/allIndices?csv=true",
            'option_chain': "https://www.nseindia.com/option-chain"
        }

        # Direct download URLs with placeholders
        # Formats: {ddmmyyyy}, {ddmmyy}, {yyyymmdd}, {dd-Mon-yyyy}
        self.direct_urls = {
            'oi_spurts': "https://www.nseindia.com/api/live-analysis-oi-spurts-underlyings?type=underlying&csv=true&partialFileName=By-Underlying",
            'combine_oi': "https://nsearchives.nseindia.com/archives/nsccl/mwpl/combineoi_{ddmmyyyy}.zip",
            'pe_detail': "https://nsearchives.nseindia.com/content/equities/peDetail/PE_{ddmmyy}.csv",
            'cm_high_low': "https://nsearchives.nseindia.com/content/CM_52_wk_High_low_{ddmmyyyy}.csv",
            'sec_bhavdata': "https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{ddmmyyyy}.csv",
            'block_deals': "https://nsearchives.nseindia.com/content/equities/block.csv",
            'bulk_deals': "https://nsearchives.nseindia.com/content/equities/bulk.csv",
            'bhavcopy_cm': "https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{yyyymmdd}_F_0000.csv.zip",
            'ind_close': "https://nsearchives.nseindia.com/content/indices/ind_close_all_{ddmmyyyy}.csv",
            'fao_participant_vol': "https://nsearchives.nseindia.com/content/nsccl/fao_participant_vol_{ddmmyyyy}.csv",
            'fao_participant_oi': "https://nsearchives.nseindia.com/content/nsccl/fao_participant_oi_{ddmmyyyy}.csv",
            'fii_stats': "https://nsearchives.nseindia.com/content/fo/fii_stats_{dd-Mon-yyyy}.xls",
            'bhavcopy_fo': "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip",
            'Short_Sell': "https://nsearchives.nseindia.com/archives/equities/shortSelling/shortselling_{ddmmyyyy}.csv",
            'corporates_pit': "https://www.nseindia.com/api/corporates-pit?index=equities&csv=true",
            'bse_cash_bhavcopy': "https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{yyyymmdd}_F_0000.CSV"
            
        }

        # Optional downloads share the same EOD root by default.
        self.eod_source_keys = list(self.direct_urls.keys())
        
        self.target_date = datetime.now() # Default to today
        
        # Download paths for each source
        nse_base_path = os.path.join(os.path.expanduser("~"), "Downloads", "NSE_Data")
        eod_base_path = os.path.join(os.path.expanduser("~"), "Downloads", "EOD_Data")
        
        self.download_paths = {
            'nifty50': os.path.join(nse_base_path, "NIFTY50"),
            'nifty500': os.path.join(nse_base_path, "NIFTY500"),
            'market_indices': os.path.join(nse_base_path, "Market_Indices"),
            'option_chain': os.path.join(nse_base_path, "Option_Chain"),
            'oi_spurts': eod_base_path,
            'combine_oi': eod_base_path,
            'pe_detail': eod_base_path,
            'cm_high_low': eod_base_path,
            'sec_bhavdata': eod_base_path,
            'block_deals': eod_base_path,
            'bulk_deals': eod_base_path,
            'bhavcopy_cm': eod_base_path,
            'ind_close': eod_base_path,
            'fao_participant_vol': eod_base_path,
            'fao_participant_oi': eod_base_path,
            'fii_stats': eod_base_path,
            'bhavcopy_fo': eod_base_path,
            'Short_Sell': eod_base_path,
            'corporates_pit': eod_base_path,
            'bse_cash_bhavcopy': eod_base_path
        }
        
        self.scheduled_times = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", 
                              "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", 
                              "15:00", "15:30", "16:00"]
        self.optional_download_time = "21:00"  # Optional files run at 9 PM daily
        self.is_running = False
        self.auto_mode = False  # Auto mode: scheduler runs 8 AM - 8 PM
        self.weekend_downloads_enabled = False  # Allow downloads on weekends
        self.last_weekend_notification = None  # Track last weekend notification date
        self.enabled_downloads = list(self.direct_urls.keys()) # List of enabled optional downloads
        # Use a writable directory for config and logs
        app_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "NSE_Data_Downloader")
        if not os.path.exists(app_data_dir):
            try:
                os.makedirs(app_data_dir)
            except Exception:
                # Fallback to user home directory if AppData fails
                app_data_dir = os.path.expanduser("~")
        
        self.app_dir = app_data_dir
            
        self.config_file = os.path.join(self.app_dir, "config.json")
        self.gui = gui
        self.headless_mode = True  # Run browser hidden in background
        self.load_config()
        
        # Setup logging
        log_file = os.path.join(self.app_dir, 'nse_downloader.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            migrated = False
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Load custom paths if available
                    if 'download_paths' in config:
                        self.download_paths.update(config.get('download_paths', {}))

                        # Ensure legacy NSE_Data paths for optional files move to EOD_Data
                        eod_base_path = os.path.join(os.path.expanduser("~"), "Downloads", "EOD_Data")

                        for key in self.eod_source_keys:
                            current_path = self.download_paths.get(key)
                            if not current_path:
                                continue

                            normalized = os.path.normpath(current_path).lower()
                            normalized_base = os.path.normpath(eod_base_path).lower()

                            # If path is not the base path, but is inside EOD_Data or NSE_Data (legacy)
                            # We flatten it to the root EOD_Data folder
                            if normalized != normalized_base and ("eod_data" in normalized or "nse_data" in normalized):
                                self.download_paths[key] = eod_base_path
                                migrated = True
                                logging.info(f"Migrated path for {key} to EOD_Data root: {eod_base_path}")

                    # Support both old single time and new multiple times
                    if 'scheduled_times' in config:
                        self.scheduled_times = config.get('scheduled_times', self.scheduled_times)
                    elif 'scheduled_time' in config:
                        # Convert old single time to list
                        self.scheduled_times = [config.get('scheduled_time', "09:30")]
                    # Optional downloads time
                    if 'optional_download_time' in config:
                        self.optional_download_time = config.get('optional_download_time', self.optional_download_time)
                    # Load auto mode state
                    self.auto_mode = config.get('auto_mode', False)
                    # Load weekend downloads setting
                    self.weekend_downloads_enabled = config.get('weekend_downloads_enabled', False)
                    # Load enabled downloads
                    self.enabled_downloads = config.get('enabled_downloads', [])
                    
                    # Migrate old naming for Short Sell if present
                    if 'Short_sell' in self.enabled_downloads:
                        self.enabled_downloads = ['Short_Sell' if d == 'Short_sell' else d for d in self.enabled_downloads]
                        migrated = True
                    
                    if 'Short_sell' in self.download_paths:
                        self.download_paths['Short_Sell'] = self.download_paths.pop('Short_sell')
                        migrated = True

                if migrated:
                    self.save_config()
            except Exception as e:
                logging.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'download_paths': self.download_paths,
                'scheduled_times': self.scheduled_times,
                'optional_download_time': self.optional_download_time,
                'auto_mode': self.auto_mode,
                'weekend_downloads_enabled': self.weekend_downloads_enabled,
                'enabled_downloads': self.enabled_downloads
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def get_nse_headers(self):
        """Get proper headers for NSE India website"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        
        # Add headless mode configuration
        if hasattr(self, 'headless_mode') and self.headless_mode:
            chrome_options.add_argument('--headless=new')  # New headless mode with download support
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            print("Running in headless mode (browser hidden)")
        else:
            print("Running in visible mode (browser shown)")
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Set download preferences - CRITICAL for headless mode
        # Create all download folders and ensure absolute paths
        for key in self.download_paths:
            self.download_paths[key] = os.path.abspath(self.download_paths[key])
            if not os.path.exists(self.download_paths[key]):
                os.makedirs(self.download_paths[key])
        
        # Use a temporary default download directory (will be updated via CDP for each download)
        temp_download = self.download_paths['nifty500']
        
        prefs = {
            "download.default_directory": temp_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_setting_values.automatic_downloads": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Use webdriver-manager to handle ChromeDriver automatically with fallback
        try:
            print("Installing/updating ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("ChromeDriver loaded successfully")
        except Exception as e:
            # Fallback: try system Chrome driver
            logging.error(f"ChromeDriver manager failed: {e}")
            print(f"ChromeDriver error: {e}")
            print("Trying system ChromeDriver...")
            try:
                driver = webdriver.Chrome(options=chrome_options)
                print("Using system ChromeDriver")
            except Exception as e2:
                logging.error(f"System ChromeDriver also failed: {e2}")
                print(f"System ChromeDriver error: {e2}")
                raise Exception("Could not initialize ChromeDriver. Please ensure Chrome browser is installed.")
        
        # CRITICAL: Enable downloads in headless mode using CDP
        # Use both Browser and Page CDP commands for maximum compatibility
        # Set initial download path (will be updated for each source during download)
        driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": temp_download,
            "eventsEnabled": True
        })
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": temp_download
        })
        
        # Minimal automation hiding (keeping CDP commands that work)
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {  # DISABLED
        #     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        # })
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # DISABLED
        
        logging.info(f"Download paths configured: {self.download_paths}")
        print(f"Download paths: {self.download_paths}")
        
        return driver
    
    def get_formatted_url(self, url, date_obj):
        """Format URL with date placeholders"""
        if not date_obj:
            date_obj = datetime.now()
            
        formatted_url = url
        
        # Replace {ddmmyyyy} -> 09122025
        if "{ddmmyyyy}" in formatted_url:
            formatted_url = formatted_url.replace("{ddmmyyyy}", date_obj.strftime("%d%m%Y"))
            
        # Replace {ddmmyy} -> 091225
        if "{ddmmyy}" in formatted_url:
            formatted_url = formatted_url.replace("{ddmmyy}", date_obj.strftime("%d%m%y"))
            
        # Replace {yyyymmdd} -> 20251209
        if "{yyyymmdd}" in formatted_url:
            formatted_url = formatted_url.replace("{yyyymmdd}", date_obj.strftime("%Y%m%d"))
            
        # Replace {dd-Mon-yyyy} -> 09-Dec-2025
        if "{dd-Mon-yyyy}" in formatted_url:
            formatted_url = formatted_url.replace("{dd-Mon-yyyy}", date_obj.strftime("%d-%b-%Y"))
            
        return formatted_url

    def download_direct_file(self, driver, source_name, url, download_path, progress_offset=0, progress_bar="optional"):
        """Download a file directly from a URL using HTTP requests

        Args:
            driver: Selenium WebDriver instance
            source_name: Name of the source
            url: URL to download from
            download_path: Path to save downloads
            progress_offset: Offset for progress bar
        """
        abs_download_path = os.path.abspath(download_path)
        try:
            if not os.path.exists(abs_download_path):
                os.makedirs(abs_download_path)

            logging.info(f"Direct download for {source_name} to: {abs_download_path}")

            if self.gui:
                self.gui.update_progress(progress_offset, f"Downloading {source_name}...", bar=progress_bar)

            session = requests.Session()

            # Attempt to share cookies from Selenium session to maintain NSE authentication
            if driver:
                try:
                    for cookie in driver.get_cookies():
                        session.cookies.set(cookie.get("name"), cookie.get("value"))
                except Exception as cookie_err:
                    logging.debug(f"Cookie transfer skipped for {source_name}: {cookie_err}")

            headers = self.get_nse_headers()
            
            # Use specific referers for API endpoints to avoid blocking
            referer = "https://www.nseindia.com/"
            if source_name == 'nifty500':
                referer = "https://www.nseindia.com/market-data/live-equity-market"
            elif source_name == 'market_indices':
                referer = "https://www.nseindia.com/market-data/live-index-watch"
            elif source_name == 'oi_spurts':
                referer = "https://www.nseindia.com/live-market/live-analysis/oi-spurts"
            elif source_name == 'corporates_pit':
                referer = "https://www.nseindia.com/companies-listing/corporate-filings-insider-trading"
            elif source_name == 'bse_cash_bhavcopy':
                referer = "https://www.bseindia.com/"

            headers.update({
                "Referer": referer,
                "Accept": "*/*",
                # Restrict to gzip/deflate so we avoid Brotli-encoded CSV corruption
                "Accept-Encoding": "gzip, deflate",
            })

            response = session.get(url, headers=headers, timeout=60, allow_redirects=True)

            # NSE may intermittently return 401/403 for API calls even with valid cookies.
            # Refresh browser session cookies once and retry before failing.
            if response.status_code in (401, 403) and driver:
                logging.warning(f"Received HTTP {response.status_code} for {source_name}; retrying after cookie refresh")
                try:
                    driver.get(referer)
                    time.sleep(1)
                    session.cookies.clear()
                    for cookie in driver.get_cookies():
                        session.cookies.set(cookie.get("name"), cookie.get("value"))
                    response = session.get(url, headers=headers, timeout=60, allow_redirects=True)
                except Exception as retry_err:
                    logging.warning(f"Retry cookie refresh failed for {source_name}: {retry_err}")
            
            # If requests fails, try using the driver directly (fallback)
            if response.status_code != 200:
                logging.warning(f"Direct download via requests failed for {source_name} (HTTP {response.status_code}). Trying Selenium fallback...")
                
                if driver:
                    try:
                        # Update download behavior for this specific path
                        driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                            "behavior": "allow",
                            "downloadPath": abs_download_path,
                            "eventsEnabled": True
                        })
                        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                            "behavior": "allow",
                            "downloadPath": abs_download_path
                        })
                        
                        # Navigate to the URL to trigger download
                        driver.get(url)
                        time.sleep(5) # Wait for download to start/complete
                        
                        # Check if any new file appeared in the path
                        files_after = os.listdir(abs_download_path)
                        if any(f.endswith('.csv') or f.endswith('.zip') for f in files_after):
                            logging.info(f"Selenium fallback successful for {source_name}")
                            return True
                    except Exception as fallback_err:
                        logging.error(f"Selenium fallback also failed for {source_name}: {fallback_err}")
                
                return False

            filename = None
            content_disp = response.headers.get("Content-Disposition")
            if content_disp and "filename=" in content_disp:
                filename = content_disp.split("filename=")[-1].split(";")[0].strip('"')

            if not filename:
                parsed = urlparse(url)
                ext = os.path.splitext(parsed.path)[1] or ".csv"
                filename = f"{source_name}{ext}"

            target_file = os.path.join(abs_download_path, filename)
            with open(target_file, "wb") as fp:
                fp.write(response.content)

            logging.info(f"Saved {source_name} as {target_file}")
            return target_file
        except Exception as e:
            logging.error(f"Error downloading {source_name}: {str(e)}")
            print(f"Error downloading {source_name}: {str(e)}")
            return False

    def download_browser_click_file(self, driver, source_name, page_url, download_path, click_selector, progress_offset=0, progress_bar="optional"):
        """Download a file by opening a page in the browser and clicking a download element."""
        abs_download_path = os.path.abspath(download_path)
        try:
            if not os.path.exists(abs_download_path):
                os.makedirs(abs_download_path)

            logging.info(f"Browser-click download for {source_name} to: {abs_download_path}")

            if self.gui:
                self.gui.update_progress(progress_offset, f"Opening {source_name} page...", bar=progress_bar)

            if not driver:
                return False

            driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": abs_download_path,
                "eventsEnabled": True
            })
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": abs_download_path
            })

            start_time = time.time()
            default_downloads = os.path.expanduser("~/Downloads")
            directories_to_check = [abs_download_path]
            if os.path.exists(default_downloads) and default_downloads != abs_download_path:
                directories_to_check.append(default_downloads)
                
            for path in getattr(self, 'download_paths', {}).values():
                if os.path.exists(path) and path not in directories_to_check:
                    directories_to_check.append(path)

            before_files = {}
            for d in directories_to_check:
                try:
                    before_files[d] = set(os.listdir(d))
                except OSError:
                    before_files[d] = set()

            driver.get(page_url)

            if source_name == 'option_chain':
                self.prepare_option_chain_page(driver)

            wait = WebDriverWait(driver, 30)
            download_button = wait.until(EC.element_to_be_clickable((By.ID, click_selector)))
            driver.execute_script("arguments[0].click();", download_button)

            if self.gui:
                self.gui.update_progress(progress_offset + 5, f"Downloading {source_name}...", bar=progress_bar)

            timeout = 60
            poll_interval = 0.5
            elapsed = 0.0

            if source_name == 'option_chain':
                # Option chain is a data-URI download; keep the browser flow but hint a filename.
                driver.execute_script("arguments[0].setAttribute('download', arguments[1]);", download_button, f"Option_Chain_{datetime.now().strftime('%d%m%y')}.csv")

            while elapsed < timeout:
                candidate_files = []
                for d in directories_to_check:
                    try:
                        current_files = os.listdir(d)
                    except OSError:
                        continue
                    for filename in current_files:
                        full_path = os.path.join(d, filename)
                        if not os.path.isfile(full_path):
                            continue
                        lower_name = filename.lower()
                        if lower_name.endswith(('.crdownload', '.tmp', '.part')):
                            continue
                        if filename in before_files[d]:
                            continue
                        try:
                            if os.path.getmtime(full_path) >= start_time - 5:
                                candidate_files.append(full_path)
                        except OSError:
                            continue

                if candidate_files:
                    latest_file = max(candidate_files, key=os.path.getmtime)
                    size1 = os.path.getsize(latest_file)
                    time.sleep(poll_interval)
                    if os.path.exists(latest_file):
                        size2 = os.path.getsize(latest_file)
                        if size1 > 0 and size1 == size2:
                            logging.info(f"Browser-click download successful for {source_name}: {latest_file}")
                            return latest_file

                time.sleep(poll_interval)
                elapsed += poll_interval

            logging.warning(f"Browser-click download timed out for {source_name}")
            return False
        except Exception as e:
            logging.error(f"Error browser-downloading {source_name}: {str(e)}")
            print(f"Error browser-downloading {source_name}: {str(e)}")
            return False

    def prepare_option_chain_page(self, driver, symbol="NIFTY"):
        """Set a stable option-chain selection before downloading the CSV."""
        try:
            wait = WebDriverWait(driver, 30)

            # Keep the main contract view on NIFTY, then choose the symbol and earliest available expiry.
            view_select = wait.until(lambda d: self.find_view_contract_select(d))
            if view_select:
                Select(view_select).select_by_visible_text(symbol)

            symbol_select = wait.until(lambda d: self.find_symbol_select(d, symbol))
            if symbol_select:
                Select(symbol_select).select_by_visible_text(symbol)

            def expiry_ready(driver):
                expiry_select = self.find_expiry_select(driver)
                if not expiry_select:
                    return False
                options = [opt.text.strip() for opt in Select(expiry_select).options if opt.text.strip() and opt.text.strip().lower() != 'select']
                return expiry_select if options else False

            expiry_select = wait.until(expiry_ready)
            expiry_options = [opt.text.strip() for opt in Select(expiry_select).options if opt.text.strip() and opt.text.strip().lower() != 'select']
            if expiry_options:
                Select(expiry_select).select_by_visible_text(expiry_options[0])

            # ── Spot price: poll #equity_underlyingVal inside the browser's JS engine ──
            # execute_async_script runs the polling loop inside Chrome's own event loop,
            # so it fires correctly when Angular/NSE pushes the live value into the DOM.
            current_spot = getattr(self, 'current_spot_price', '0')
            if current_spot == '0':
                try:
                    # First check: what does the element currently contain (for debug)?
                    dbg = driver.execute_script(
                        "var e=document.getElementById('equity_underlyingVal');"
                        "return e ? (e.innerText||e.textContent||'[empty]').trim() : '[not found]';"
                    )
                    print(f"  🔍 equity_underlyingVal current content: '{dbg}'")
    
                    driver.set_script_timeout(30)   # allow up to 30s for the async script
                    spot_js = """
    var callback = arguments[0];
    var maxWait  = 25000;   // 25 seconds total
    var interval = 400;     // poll every 400 ms
    var elapsed  = 0;
    
    var timer = setInterval(function () {
        var el = document.getElementById('equity_underlyingVal');
        if (el) {
            // innerText works on visible elements; textContent works even if hidden
            var txt = (el.innerText || el.textContent || '').replace(/,/g, '').trim();
            if (txt) {
                var tokens = txt.split(/\\s+/);
                for (var i = tokens.length - 1; i >= 0; i--) {
                    var v = parseFloat(tokens[i]);
                    if (!isNaN(v) && v > 1000) {
                        clearInterval(timer);
                        callback(String(Math.round(v)));
                        return;
                    }
                }
            }
        }
        elapsed += interval;
        if (elapsed >= maxWait) {
            clearInterval(timer);
            callback('0');
        }
    }, interval);
    """
                    spot_val = driver.execute_async_script(spot_js)
                    self.current_spot_price = spot_val if spot_val and spot_val != '0' else '0'
                    if self.current_spot_price != '0':
                        print(f"  📊 Nifty spot from browser: {self.current_spot_price}")
                        logging.info(f"Spot price read from #equity_underlyingVal: {self.current_spot_price}")
                    else:
                        print("  ⚠️ equity_underlyingVal still empty after 25s — filename will use spot_0")
                        logging.warning("equity_underlyingVal empty/not found after 25s polling")
                except Exception as spot_err:
                    logging.warning(f"Spot price script error: {spot_err}")
                    print(f"  ⚠️ Spot price error: {spot_err}")
            else:
                print(f"  ✅ Using existing Nifty spot price: {current_spot}")

            return True
        except Exception as e:
            logging.warning(f"Could not preselect option chain values: {e}")
            return False

    def find_view_contract_select(self, driver):
        """Find the top-level contract select, which has a small fixed set of index choices."""
        for element in driver.find_elements(By.TAG_NAME, "select"):
            try:
                option_texts = {opt.text.strip() for opt in Select(element).options if opt.text.strip()}
                if {'NIFTY', 'NIFTYNXT50', 'FINNIFTY', 'BANKNIFTY', 'MIDCPNIFTY'}.issubset(option_texts):
                    return element
            except Exception:
                continue
        return None

    def find_symbol_select(self, driver, symbol):
        """Find the symbol select, which has a long list of equities and a placeholder option."""
        for element in driver.find_elements(By.TAG_NAME, "select"):
            try:
                select_widget = Select(element)
                option_texts = [opt.text.strip() for opt in select_widget.options if opt.text.strip()]
                if len(option_texts) > 20 and option_texts[0].lower() == 'select' and symbol in option_texts:
                    return element
            except Exception:
                continue
        return None

    def find_expiry_select(self, driver):
        """Find the expiry select by looking for a select with date-like options."""
        for element in driver.find_elements(By.TAG_NAME, "select"):
            try:
                options = [opt.text.strip() for opt in Select(element).options if opt.text.strip() and opt.text.strip().lower() != 'select']
                if options and any('-' in option for option in options):
                    return element
            except Exception:
                continue
        return None

    def download_data(self, mode='all'):
        """
        Download CSV files from NSE sources
        mode: 'all', 'defaults' (NIFTY500/Indices), 'optionals' (Selected files)
        """
        driver = None
        # Record download start time to pass to rename function
        import time as time_module
        download_start_time = time_module.time()
        
        try:
            # Determine which progress bar to use for general updates
            target_bar = "optional" if mode == 'optionals' else "main"
            
            # Update progress: Starting
            if self.gui:
                self.gui.update_progress(5, f"Starting browser ({mode} mode)...", bar=target_bar)
            
            logging.info(f"Starting downloads at {datetime.now()} (Mode: {mode})")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting downloads ({mode})...")
            
            driver = self.setup_driver()
            
            # Update progress: Browser started
            if self.gui:
                self.gui.update_progress(10, "Browser started! Connecting to NSE...", bar=target_bar)
            
            # First, visit NSE homepage to get cookies and establish session
            logging.info("Establishing session with NSE...")
            driver.get("https://www.nseindia.com")
            
            # Update progress: Session establishing
            if self.gui:
                self.gui.update_progress(12, "Establishing session with NSE India...", bar=target_bar)
            
            time.sleep(5)
            
            # Visit dynamic data pages to ensure all cookies are set (crucial for API)
            driver.get("https://www.nseindia.com/market-data/live-equity-market")
            time.sleep(3)
            driver.get("https://www.nseindia.com/market-data/live-index-watch")
            time.sleep(3)

            # ── Read Nifty spot price from live-index-watch page ──────────────────
            # This page shows all indices including NIFTY 50 live value.
            # We poll inside the browser's JS engine so Angular data binding is caught.
            self.current_spot_price = '0'
            try:
                driver.set_script_timeout(20)
                nifty_spot_js = """
var callback = arguments[0];
var maxWait  = 15000;
var interval = 400;
var elapsed  = 0;

function extractNifty() {
    // Strategy A: look for any element whose text contains 'NIFTY 50' or 'Nifty 50'
    // and grab the nearby number, OR find a table row with NIFTY and read the LTP cell.
    var rows = document.querySelectorAll('tr');
    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].querySelectorAll('td');
        for (var j = 0; j < cells.length; j++) {
            var txt = (cells[j].innerText || cells[j].textContent || '').trim();
            if (/^NIFTY 50$/i.test(txt) || /^NIFTY50$/i.test(txt)) {
                // Next cell or nearby cells likely have the LTP value
                for (var k = j + 1; k < cells.length && k <= j + 3; k++) {
                    var val = parseFloat((cells[k].innerText || cells[k].textContent || '').replace(/,/g,''));
                    if (!isNaN(val) && val > 1000) {
                        return String(Math.round(val));
                    }
                }
            }
        }
    }
    // Strategy B: scan all visible text nodes for a number > 10000 near "NIFTY"
    var allEls = document.querySelectorAll('td, span, div');
    var prev = '';
    for (var i = 0; i < allEls.length; i++) {
        var t = (allEls[i].innerText || allEls[i].textContent || '').trim();
        if (/nifty 50/i.test(prev + ' ' + t)) {
            var v = parseFloat(t.replace(/,/g,''));
            if (!isNaN(v) && v > 10000) return String(Math.round(v));
        }
        if (t) prev = t;
    }
    return null;
}

var timer = setInterval(function() {
    var result = extractNifty();
    if (result) {
        clearInterval(timer);
        callback(result);
        return;
    }
    elapsed += interval;
    if (elapsed >= maxWait) {
        clearInterval(timer);
        callback('0');
    }
}, interval);
"""
                spot_val = driver.execute_async_script(nifty_spot_js)
                if spot_val and spot_val != '0':
                    self.current_spot_price = spot_val
                    print(f"  📊 Nifty 50 spot (from live-index-watch): {self.current_spot_price}")
                    logging.info(f"Nifty spot price captured: {self.current_spot_price}")
                else:
                    print("  ⚠️ Could not read Nifty spot from live-index-watch — will try on option-chain page")
            except Exception as spot_err:
                logging.warning(f"Live-index-watch spot read error: {spot_err}")
                print(f"  ⚠️ Spot read error: {spot_err}")
            
            success_nifty50 = False
            if mode in ['all', 'defaults']:
                logging.info("=" * 50)
                logging.info("DIRECT DOWNLOAD: NIFTY 50")
                logging.info("=" * 50)

                if self.gui:
                    self.gui.update_progress(20, "Preparing NIFTY 50 download...", bar="main")

                nifty50_url = self.urls['nifty50']
                print(f"Downloading NIFTY 50 from: {nifty50_url}")
                success_nifty50 = self.download_direct_file(
                    driver,
                    'nifty50',
                    nifty50_url,
                    self.download_paths['nifty50'],
                    progress_offset=25,
                    progress_bar='main'
                )

            success_nifty500 = False
            if mode in ['all', 'defaults']:
                logging.info("=" * 50)
                logging.info("DIRECT DOWNLOAD: NIFTY 500")
                logging.info("=" * 50)

                if self.gui:
                    self.gui.update_progress(30, "Preparing NIFTY 500 download...", bar="main")

                nifty_url = self.urls['nifty500']
                print(f"Downloading NIFTY 500 from: {nifty_url}")
                success_nifty500 = self.download_direct_file(
                    driver,
                    'nifty500',
                    nifty_url,
                    self.download_paths['nifty500'],
                    progress_offset=35,
                    progress_bar='main'
                )

            success_market = False
            if mode in ['all', 'defaults']:
                logging.info("=" * 50)
                logging.info("DIRECT DOWNLOAD: MARKET INDICES")
                logging.info("=" * 50)

                if self.gui:
                    self.gui.update_progress(60, "Preparing Market Indices download...", bar="main")

                market_url = self.urls['market_indices']
                print(f"Downloading Market Indices from: {market_url}")
                success_market = self.download_direct_file(
                    driver,
                    'market_indices',
                    market_url,
                    self.download_paths['market_indices'],
                    progress_offset=75,
                    progress_bar='main'
                )

            # ── Read Nifty 50 spot from the already-downloaded MarketIndices CSV ──
            # MarketIndices CSV row format: "NIFTY 50","24,182.10",...
            # Column 1 (index 1) = CURRENT value — always reliable, no DOM scraping needed.
            if success_market:
                try:
                    import glob, csv
                    abs_market_path = os.path.abspath(self.download_paths['market_indices'])
                    market_files = sorted(
                        glob.glob(os.path.join(abs_market_path, 'MarketIndices_*.csv')),
                        key=os.path.getmtime, reverse=True
                    )
                    if market_files:
                        with open(market_files[0], newline='', encoding='utf-8-sig') as mf:
                            reader = csv.reader(mf)
                            for row in reader:
                                if row and row[0].strip().strip('"') == 'NIFTY 50':
                                    raw_val = row[1].strip().strip('"').replace(',', '') if len(row) > 1 else ''
                                    try:
                                        val = int(float(raw_val))
                                        if val > 1000:
                                            self.current_spot_price = str(val)
                                            print(f"  📊 Nifty 50 spot (from MarketIndices CSV): {self.current_spot_price}")
                                            logging.info(f"Nifty spot from CSV: {self.current_spot_price}")
                                            break
                                    except (ValueError, TypeError):
                                        pass
                except Exception as csv_err:
                    logging.warning(f"Could not read Nifty spot from MarketIndices CSV: {csv_err}")
                    print(f"  ⚠️ Spot CSV read error: {csv_err}")

            if success_market and self.current_spot_price == '0':
                print("  ⚠️ NIFTY 50 row not found in MarketIndices CSV — spot will be 0")

            success_option_chain = False
            if mode in ['all', 'defaults']:
                logging.info("=" * 50)
                logging.info("DIRECT DOWNLOAD: OPTION CHAIN")
                logging.info("=" * 50)

                if self.gui:
                    self.gui.update_progress(75, "Preparing Option Chain download...", bar="main")

                option_chain_url = self.urls['option_chain']
                print(f"Downloading Option Chain from: {option_chain_url}")
                success_option_chain = self.download_browser_click_file(
                    driver,
                    'option_chain',
                    option_chain_url,
                    self.download_paths['option_chain'],
                    'download_csv',
                    progress_offset=80,
                    progress_bar='main'
                )
            
            # Process direct downloads
            direct_download_results = {}
            if mode in ['all', 'optionals'] and hasattr(self, 'direct_urls'):
                # Filter only enabled downloads
                enabled_keys = [k for k in self.direct_urls.keys() if k in self.enabled_downloads]
                total_direct = len(enabled_keys)
                
                if total_direct > 0:
                    for i, key in enumerate(enabled_keys):
                        url = self.direct_urls[key]
                        logging.info("=" * 50)
                        logging.info(f"DOWNLOADING {key.upper()}")
                        logging.info("=" * 50)
                        
                        # Calculate progress (0 to 75 for optional bar)
                        progress = int((i / total_direct) * 75)
                        
                        # Format URL with target date
                        formatted_url = self.get_formatted_url(url, self.target_date)
                        print(f"Downloading {key} from: {formatted_url}")
                        success = self.download_direct_file(
                            driver,
                            key,
                            formatted_url,
                            self.download_paths[key],
                            progress_offset=progress,
                            progress_bar='optional'
                        )
                        direct_download_results[key] = success
                        time.sleep(0.5)  # Smaller delay between downloads
            
            # Update progress: Downloads initiated
            if self.gui:
                if mode in ['all', 'defaults']:
                    self.gui.update_progress(90, "Verifying downloaded files...", bar="main")
                if mode in ['all', 'optionals']:
                    self.gui.update_progress(95, "Verifying optional files...", bar="optional")
            
            # Rename both downloaded files
            renamed_files = []
            failed_downloads = []
            
            if mode in ['all', 'defaults']:
                success_msg = []
                if success_nifty50:
                    success_msg.append("NIFTY 50")
                if success_nifty500:
                    success_msg.append("NIFTY 500")
                if success_market:
                    success_msg.append("Market Indices")
                if success_option_chain:
                    success_msg.append("Option Chain")
                    
                if success_msg:
                    msg = f"Successfully downloaded: {', '.join(success_msg)}"
                    logging.info(msg)
                    if self.gui:
                        self.gui.update_progress(100, "Defaults completed!", bar="main")
                else:
                    if self.gui:
                        self.gui.update_progress(100, "Defaults completed (with errors)", bar="main")

                if success_nifty50:
                    preferred_file = success_nifty50 if isinstance(success_nifty50, str) else None
                    renamed = self.rename_downloaded_file('nifty50', self.download_paths['nifty50'], skip_stability_check=True, progress_start=76, progress_end=84, progress_bar="main", download_start_time=download_start_time, preferred_file=preferred_file)
                    if renamed:
                        renamed_files.append(renamed)
                    else:
                        failed_downloads.append("NIFTY 50")
                
                if success_nifty500:
                    # Update progress: Processing NIFTY 500 file
                    preferred_file = success_nifty500 if isinstance(success_nifty500, str) else None
                    renamed = self.rename_downloaded_file('nifty500', self.download_paths['nifty500'], skip_stability_check=True, progress_start=84, progress_end=92, progress_bar="main", download_start_time=download_start_time, preferred_file=preferred_file)
                    if renamed:
                        renamed_files.append(renamed)
                    else:
                        failed_downloads.append("NIFTY 500")
                else:
                    failed_downloads.append("NIFTY 500")
            
                if success_market:
                    # Update progress: Processing Market Indices file
                    preferred_file = success_market if isinstance(success_market, str) else None
                    renamed = self.rename_downloaded_file('market_indices', self.download_paths['market_indices'], skip_stability_check=True, progress_start=88, progress_end=100, progress_bar="main", download_start_time=download_start_time, preferred_file=preferred_file)
                    if renamed:
                        renamed_files.append(renamed)
                    else:
                        failed_downloads.append("Market Indices")
                else:
                    failed_downloads.append("Market Indices")

                if success_option_chain:
                    # Update progress: Processing Option Chain file
                    preferred_file = success_option_chain if isinstance(success_option_chain, str) else None
                    renamed = self.rename_downloaded_file('option_chain', self.download_paths['option_chain'], skip_stability_check=True, progress_start=92, progress_end=100, progress_bar="main", download_start_time=download_start_time, preferred_file=preferred_file)
                    if renamed:
                        renamed_files.append(renamed)
                    else:
                        failed_downloads.append("Option Chain")
                else:
                    failed_downloads.append("Option Chain")
            
            # Rename optional downloads
            if hasattr(self, 'direct_urls') and mode in ['all', 'optionals']:
                # Check which ones were supposed to be downloaded
                enabled_keys = [k for k in self.direct_urls.keys() if k in self.enabled_downloads]
                total_enabled = len(enabled_keys)
                
                for idx, key in enumerate(enabled_keys):
                    success = direct_download_results.get(key, False)
                    if success:
                        # Calculate dynamic progress for each file (76% to 100%)
                        slice_size = 24.0 / max(total_enabled, 1)
                        start_p = 76 + int(idx * slice_size)
                        end_p = 76 + int((idx + 1) * slice_size)
                        end_p = min(end_p, 100)
                        
                        # Determine extension based on URL
                        ext = '.csv'
                        if '.zip' in self.direct_urls[key].lower():
                            ext = '.zip'
                        elif '.xls' in self.direct_urls[key].lower():
                            ext = '.xls'
                            
                        preferred_file = success if isinstance(success, str) else None
                        renamed = self.rename_downloaded_file(key, self.download_paths[key], extension=ext, skip_stability_check=True, progress_start=start_p, progress_end=end_p, progress_bar="optional", download_start_time=download_start_time, preferred_file=preferred_file)
                        if renamed:
                            renamed_files.append(renamed)
                        else:
                            failed_downloads.append(key)
                    else:
                        failed_downloads.append(key)

            # Show notification for failed downloads
            if failed_downloads and self.gui:
                failed_str = "\n".join([f"- {name}" for name in failed_downloads])
                def show_alert():
                    messagebox.showwarning(
                        "Download Incomplete", 
                        f"The following files could not be downloaded (possibly not available for this date):\n\n{failed_str}"
                    )
                self.gui.root.after(0, show_alert)
            
            # Update progress: Finalizing
            if self.gui:
                if mode in ['all', 'defaults']:
                    self.gui.update_progress(98, "Finalizing downloads...", bar="main")
                if mode in ['all', 'optionals']:
                    self.gui.update_progress(100, "Complete!", bar="optional")
            
            # Update progress: Complete
            if self.gui:
                files_msg = f"Complete! Downloaded {len(renamed_files)} file(s)" if renamed_files else "Process complete"
                self.gui.update_progress(100, files_msg, bar=target_bar)
                # Reset progress bar after 3 seconds
                threading.Timer(3.0, self.gui.reset_progress).start()
            
            if renamed_files:
                print(f"✅ Successfully downloaded {len(renamed_files)} file(s)")
                for file in renamed_files:
                    print(f"   - {file}")
            else:
                print(f"⚠️ Download may have failed - check the folders manually")
            
            # Keep browser open for a moment
            time.sleep(3)
            
        except Exception as e:
            logging.error(f"Error during download: {str(e)}")
            print(f"Error: {str(e)}")
        finally:
            if driver:
                driver.quit()
    
    def rename_downloaded_file(self, source_name, download_path, extension='.csv', skip_stability_check=True, progress_start=98, progress_end=100, progress_bar="optional", download_start_time=None, preferred_file=None):
        """Rename the most recently downloaded file with timestamp
        
        Args:
            source_name: Name of source
            download_path: Path where file was downloaded
            extension: File extension to look for (default: .csv)
            skip_stability_check: Skip file size stability check (True for direct downloads)
            progress_start: Starting progress percentage for this rename operation
            progress_end: Ending progress percentage for this rename operation
            progress_bar: Which progress bar to update ("main" or "optional")
            download_start_time: Timestamp when downloads started (only files modified after this will be renamed)
        
        Returns:
            str: New filename if successful, None if failed
        """
        try:
            # Always work with an absolute, normalised path so all comparisons are consistent
            abs_download_path = os.path.abspath(download_path)

            # Force delete any incomplete and unwanted download files for nifty500
            if source_name == 'nifty500':
                try:
                    # Delete incomplete download file
                    incomplete_file = os.path.join(abs_download_path, 'downloads.htm.crdownload')
                    if os.path.exists(incomplete_file):
                        os.remove(incomplete_file)
                        logging.info(f"Deleted incomplete download file: {incomplete_file}")
                        print(f"  🗑️ Deleted incomplete download: downloads.htm.crdownload")
                    
                    # Delete completed downloads.htm if it exists (unwanted HTML file)
                    html_file = os.path.join(abs_download_path, 'downloads.htm')
                    if os.path.exists(html_file):
                        os.remove(html_file)
                        logging.info(f"Deleted unwanted HTML file: {html_file}")
                        print(f"  🗑️ Deleted unwanted file: downloads.htm")
                except Exception as e:
                    logging.warning(f"Could not delete download files: {str(e)}")
            
            logging.info(f"Searching for downloaded file from {source_name} in: {abs_download_path}")
            
            # Wait for file to appear and download to complete
            max_wait = 10 if skip_stability_check else 30  # Even faster for direct downloads
            wait_count = 0
            latest_file = None

            # If download function already returned an exact file path, prefer it.
            if preferred_file and os.path.exists(preferred_file):
                latest_file = preferred_file
            
            # Check both configured path and default Downloads folder
            # Use abspath for all entries so comparisons are always consistent
            paths_to_check = [abs_download_path]
            default_downloads = os.path.abspath(os.path.join(os.path.expanduser("~"), "Downloads"))
            if default_downloads != abs_download_path and os.path.exists(default_downloads):
                paths_to_check.append(default_downloads)
                
            for path in getattr(self, 'download_paths', {}).values():
                norm_path = os.path.abspath(path)
                if os.path.exists(norm_path) and norm_path not in paths_to_check:
                    paths_to_check.append(norm_path)
            
            # Ensure download path exists
            if not os.path.exists(abs_download_path):
                os.makedirs(abs_download_path)
            
            print(f"Checking paths for {source_name}: {paths_to_check}")
            
            # Build filename pattern to match based on source_name
            # This ensures we grab the correct file when multiple files of same type exist
            # Support both the NSE original filename AND the fallback source_name
            filename_patterns = {
                'nifty500': ['nifty-500', 'nifty500', 'MW-NIFTY'],
                'market_indices': ['allIndices', 'market_indices', 'index-watch', 'indexall', 'all-indices'],
                'combine_oi': ['combineoi', 'combine_oi'],
                'bhavcopy_fo': ['BhavCopy_NSE_FO', 'bhavcopy_fo'],
                'bhavcopy_cm': ['BhavCopy_NSE_CM', 'bhavcopy_cm'],
                'fii_stats': ['fii_stats'],
                'pe_detail': ['PE_', 'pe_detail'],
                'cm_high_low': ['cm_52_wk_High_low', 'cm_high_low'],
                'sec_bhavdata': ['sec_bhavdata_full', 'sec_bhavdata'],
                'ind_close': ['ind_close_all', 'ind_close'],
                'fao_participant_vol': ['fao_participant_vol'],
                'fao_participant_oi': ['fao_participant_oi'],
                'block_deals': ['block', 'block_deals'],
                'bulk_deals': ['bulk', 'bulk_deals'],
                'oi_spurts': ['By-Underlying', 'oi_spurts'],
                'option_chain': ['option-chain', 'option_chain', 'optionchain', 'download_csv'],
                'Short_Sell': ['shortselling', 'short_sell'],
                'corporates_pit': ['corporates-pit', 'corporates_pit'],
                'bse_cash_bhavcopy': ['BhavCopy_BSE_CM', 'bse_cash_bhavcopy']
            }
            expected_patterns = filename_patterns.get(source_name, [source_name])
            
            # Use provided download start time, or fall back to current time minus 2 minutes
            import time as time_module
            if download_start_time is None:
                download_start_time = time_module.time() - 120  # Fallback: last 2 minutes
            
            while (latest_file is None) and wait_count < max_wait:
                # Update progress dynamically based on elapsed time
                if self.gui:
                    progress_pct = progress_start + int((wait_count / max_wait) * (progress_end - progress_start))
                    self.gui.update_progress(progress_pct, f"Searching for {source_name} file...", bar=progress_bar)
                
                found_in_path = None
                # Look for files matching the extension AND expected filename pattern
                for check_path in paths_to_check:
                    if not os.path.exists(check_path):
                        continue
                        
                    all_files = os.listdir(check_path)
                    # Look for files (case-insensitive) that aren't already renamed
                    # AND match the expected filename pattern for this source
                    # Also check modification time to ensure we only rename files downloaded in this session
                    target_files = []
                    for f in all_files:
                        if (f.lower().endswith(extension.lower()) 
                            and not ('_' in f and '-' in f and len(f) > 20)  # Skip already renamed files
                            and (not expected_patterns or any(pattern.lower() in f.lower() for pattern in expected_patterns))):  # Match any pattern
                            # Check if file was modified after download started
                            file_path = os.path.join(check_path, f)
                            try:
                                file_mtime = os.path.getmtime(file_path)
                                # Only include files modified AFTER downloads started
                                # Added 300s buffer to account for server-side generation delays
                                if file_mtime >= (download_start_time - 300):
                                    target_files.append(f)
                            except:
                                pass
                    downloading = [f for f in all_files if f.endswith('.crdownload') or f.endswith('.tmp')]
                    
                    if wait_count == 0 or wait_count % 10 == 0:
                        print(f"  {source_name} Wait {wait_count}s: Found {len(target_files)} {extension} files, {len(downloading)} downloading...")
                    
                    if target_files:
                        # Get the most recent file
                        files_with_path = [os.path.join(check_path, f) for f in target_files]
                        potential_file = max(files_with_path, key=os.path.getctime)
                        found_in_path = check_path
                        
                        # Check if file size is stable (download completed)
                        if os.path.exists(potential_file):
                            if skip_stability_check:
                                # Direct downloads are complete when saved - no need to check stability
                                size1 = os.path.getsize(potential_file)
                                if size1 > 0:
                                    latest_file = potential_file
                                    print(f"  {source_name} file found! Size: {size1} bytes")
                                    break
                            else:
                                # Browser downloads need stability check
                                size1 = os.path.getsize(potential_file)
                                time.sleep(0.5)
                                if os.path.exists(potential_file):
                                    size2 = os.path.getsize(potential_file)
                                    if size1 == size2 and size1 > 0:
                                        latest_file = potential_file
                                        print(f"  {source_name} file download complete! Size: {size1} bytes")
                                        break
                        break
                
                if latest_file:
                    break
                    
                time.sleep(0.1)  # Check every 0.1s for ultra fast detection
                wait_count += 0.1
            
            if not latest_file:
                logging.warning(f"No new {extension} file found for {source_name} after {max_wait} seconds")
                print(f"  ⚠️ No file found for {source_name}")
                return None
            
            # Create new filename with timestamp (format: ddmmyy-hhmmmin)
            now = datetime.now()
            
            # Determine date to use in filename
            # For NIFTY 500 and Market Indices, always use current date (live data)
            # For others, use the selected target date
            if source_name in ['nifty500', 'market_indices']:
                file_date = now
            else:
                file_date = self.target_date if hasattr(self, 'target_date') and self.target_date else now
                
            date_str = file_date.strftime('%d%m%y')  # e.g., 011025
            time_str = now.strftime('%H%M') + 'min'  # e.g., 1425min for 2:25 PM
            
            # Get original filename (without extension)
            original_name = os.path.basename(latest_file)
            original_base = os.path.splitext(original_name)[0]
            
            # Create new filename based on source
            if source_name == 'nifty500':
                prefix = "NIFTY500"
            elif source_name == 'market_indices':
                prefix = "MarketIndices"
            elif source_name == 'cm_high_low':
                prefix = "CM_52wk_HighLow"
            elif source_name == 'oi_spurts':
                prefix = "OI_Spurts"
            elif source_name == 'option_chain':
                prefix = "Option_Chain"
            elif source_name == 'combine_oi':
                prefix = "CombineOI"
            elif source_name == 'pe_detail':
                prefix = "PE_Detail"
            elif source_name == 'sec_bhavdata':
                prefix = "Sec_Bhavdata"
            elif source_name == 'block_deals':
                prefix = "Block_Deals"
            elif source_name == 'bulk_deals':
                prefix = "Bulk_Deals"
            elif source_name == 'bhavcopy_cm':
                prefix = "BhavCopy_CM"
            elif source_name == 'ind_close':
                prefix = "Ind_Close"
            elif source_name == 'fao_participant_vol':
                prefix = "FAO_Participant_Vol"
            elif source_name == 'fao_participant_oi':
                prefix = "FAO_Participant_OI"
            elif source_name == 'fii_stats':
                prefix = "FII_Stats"
            elif source_name == 'bhavcopy_fo':
                prefix = "BhavCopy_FO"
            elif  source_name== 'Short_Sell':
                prefix="Short_sell"
            elif source_name == 'corporates_pit':
                prefix = "Corporates_PIT"
            elif source_name == 'bse_cash_bhavcopy':
                prefix = "BSE_BhavCopy_CM"
            else:
                prefix = source_name
            
            # Format: prefix_ddmmyy for optional files (no time suffix for optional downloads)
            if source_name in ['nifty50', 'nifty500', 'market_indices']:
                # Main files get time stamp
                new_filename = f"{prefix}_{date_str}-{time_str}{extension}"
            elif source_name == 'option_chain':
                spot_val = getattr(self, 'current_spot_price', '0')
                new_filename = f"{original_base}_spot_{spot_val}_at_{now.strftime('%H%M')}m{extension}"
            else:
                # Optional files get only date
                new_filename = f"{prefix}_{date_str}{extension}"
            new_filepath = os.path.join(abs_download_path, new_filename)
            
            # If file with same name exists, add counter
            counter = 1
            while os.path.exists(new_filepath):
                if source_name in ['nifty50', 'nifty500', 'market_indices']:
                    new_filename = f"{prefix}_{date_str}-{time_str}_{counter}{extension}"
                elif source_name == 'option_chain':
                    spot_val = getattr(self, 'current_spot_price', '0')
                    new_filename = f"{original_base}_spot_{spot_val}_at_{now.strftime('%H%M')}m_{counter}{extension}"
                else:
                    new_filename = f"{prefix}_{date_str}_{counter}{extension}"
                new_filepath = os.path.join(abs_download_path, new_filename)
                counter += 1
            
            # Move and rename the file
            if os.path.exists(latest_file):
                # Compare normalised absolute paths to decide move vs rename
                src_dir = os.path.abspath(os.path.dirname(latest_file))
                if src_dir != abs_download_path:
                    import shutil
                    shutil.move(latest_file, new_filepath)
                    logging.info(f"Moved '{original_name}' from '{src_dir}' to '{abs_download_path}'")
                else:
                    os.rename(latest_file, new_filepath)
                
                logging.info(f"File renamed from '{original_name}' to '{new_filename}'")
                print(f"  ✅ {source_name}: {new_filename}")
                return new_filepath  # Return full absolute path for consistency
            else:
                logging.error(f"File disappeared before rename: {latest_file}")
                return None
            
        except Exception as e:
            logging.error(f"Error renaming file for {source_name}: {str(e)}")
            print(f"  ❌ Error renaming {source_name}: {str(e)}")
            return None
    
    def scheduled_download_wrapper(self):
        """Wrapper for scheduled downloads - checks if it's weekend"""
        from datetime import datetime
        from tkinter import messagebox
        
        # Get current day (0=Monday, 6=Sunday)
        current_day = datetime.now().weekday()
        today_date = datetime.now().date()
        
        # Check if it's Saturday (5) or Sunday (6)
        if current_day == 5 or current_day == 6:  # Weekend
            day_name = "Saturday" if current_day == 5 else "Sunday"
            
            if not self.weekend_downloads_enabled:
                # Weekend downloads disabled - show notification
                message = f"It's {day_name} - Weekend downloads are disabled."
                logging.info(message)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
                if self.gui:
                    self.gui.update_progress(0, "Weekend - Downloads disabled")
                    
                    # Show notification only once per day
                    if self.last_weekend_notification != today_date:
                        self.last_weekend_notification = today_date
                        messagebox.showinfo(
                            "Weekend Downloads Disabled",
                            f"It's {day_name} - Market is typically closed.\n\n"
                            f"Weekend downloads are currently disabled.\n"
                            f"Enable the 'Enable Weekend Downloads' checkbox\n"
                            f"in the scheduler section to download on weekends."
                        )
                return
            else:
                # Weekend downloads enabled - proceed
                logging.info(f"Weekend detected ({day_name}) but weekend downloads enabled - Proceeding")
        else:
            # Weekday - proceed with download
            logging.info("Weekday detected - Proceeding with scheduled download")
        
        # Ensure scheduled downloads always use current date
        self.target_date = datetime.now()
        # Scheduler only downloads defaults (NIFTY 500 & Indices)
        self.download_data(mode='defaults')
    
    def scheduled_optionals_wrapper(self):
        """Run optional download set each evening"""
        from datetime import datetime
        
        # Check for weekend
        current_day = datetime.now().weekday()
        if current_day in [5, 6] and not self.weekend_downloads_enabled:
            day_name = "Saturday" if current_day == 5 else "Sunday"
            logging.info(f"It's {day_name} - Skipping optional downloads (weekend downloads disabled)")
            return
        
        if not self.enabled_downloads:
            logging.info("No optional downloads enabled; skipping optional schedule run")
            return

        logging.info("Starting scheduled optional downloads")
        self.target_date = datetime.now()
        self.download_data(mode='optionals')

    def schedule_download(self):
        """Schedule the download job for multiple times"""
        schedule.clear()
        for time_str in self.scheduled_times:
            # Use wrapper function that checks for weekends
            schedule.every().day.at(time_str).do(self.scheduled_download_wrapper)
            logging.info(f"Download scheduled for {time_str} daily (Mon-Fri only)")
        
        times_display = ", ".join(self.scheduled_times)
        print(f"Download scheduled for {times_display} daily (Monday-Friday only)")

        # Schedule optional downloads for daily 9 PM run
        schedule.every().day.at(self.optional_download_time).do(self.scheduled_optionals_wrapper)
        logging.info(f"Optional downloads scheduled for {self.optional_download_time} daily")
        print(f"Optional downloads scheduled for {self.optional_download_time} daily")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)


class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NSE Data Downloader")
        self.root.geometry("750x580")
        self.root.minsize(500, 400)
        
        # Configure CTk appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.downloader = NSEDownloader(gui=self)
        self.scheduler_thread = None
        
        # Initialize selection variables
        self.selected_downloads = {}
        self.weekend_downloads_var = tk.BooleanVar(value=self.downloader.weekend_downloads_enabled)
        
        self.create_widgets()
        
        # Auto-start scheduler if auto mode is enabled and time is between 8 AM and 8 PM
        if self.downloader.auto_mode:
            self.check_and_start_auto_mode()
            
    def create_widgets(self):
        # Title - Apple tight headline
        title_label = ctk.CTkLabel(
            self.root,
            text="NSE Data Downloader",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=5)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        # Create Notebook (Tabs)
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Tabs
        self.dashboard_tab = self.notebook.add("Dashboard")
        self.settings_tab = self.notebook.add("Settings")
        
        # --- DASHBOARD TAB ---
        self.scrollable_dashboard = ctk.CTkScrollableFrame(self.dashboard_tab, fg_color="transparent")
        self.scrollable_dashboard.pack(fill=tk.BOTH, expand=True)
        
        # Date Selection Section
        date_frame = ctk.CTkFrame(self.scrollable_dashboard)
        date_frame.pack(fill=tk.X, pady=2, padx=2)
        ctk.CTkLabel(date_frame, text="Select Date", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(2,0))
        
        # Date Picker (Day, Month, Year)
        date_inner_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_inner_frame.pack(fill=tk.X, padx=10, pady=2)
        
        ctk.CTkLabel(date_inner_frame, text="Date:").pack(side=tk.LEFT, padx=(0,5))
        
        # Day
        self.day_var = tk.StringVar(value=datetime.now().strftime("%d"))
        days = [f"{i:02d}" for i in range(1, 32)]
        self.day_cb = ctk.CTkComboBox(date_inner_frame, variable=self.day_var, values=days, width=70)
        self.day_cb.pack(side=tk.LEFT, padx=5)
        
        # Month
        self.month_var = tk.StringVar(value=datetime.now().strftime("%B"))
        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        self.month_cb = ctk.CTkComboBox(date_inner_frame, variable=self.month_var, values=months, width=120)
        self.month_cb.pack(side=tk.LEFT, padx=5)
        
        # Year
        current_year = int(datetime.now().strftime("%Y"))
        self.year_var = tk.StringVar(value=str(current_year))
        years = [str(y) for y in range(current_year - 5, 2100)]
        self.year_cb = ctk.CTkComboBox(date_inner_frame, variable=self.year_var, values=years, width=80)
        self.year_cb.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(date_inner_frame, text="Set Today", command=self.set_today, width=100, corner_radius=50).pack(side=tk.LEFT, padx=20)

        # Download Selection Section
        select_frame = ctk.CTkFrame(self.scrollable_dashboard)
        select_frame.pack(fill=tk.X, pady=2, padx=2)
        
        ctk.CTkLabel(select_frame, text="Select Downloads", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(2,0))
        
        # Default downloads (Always selected)
        default_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        default_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        ctk.CTkLabel(default_frame, text="Default (Always Downloaded):", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        ctk.CTkLabel(select_frame, text="• NIFTY 50, NIFTY 500, Market Indices, Option Chain", font=("Helvetica", 12)).pack(anchor=tk.W, padx=10, pady=2)
        
        # Optional downloads
        opt_header_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        opt_header_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkLabel(opt_header_frame, text="Optional Downloads:", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT)
        
        # Helper buttons
        ctk.CTkButton(opt_header_frame, text="Clear All", command=self.deselect_all, width=100, corner_radius=50, fg_color="transparent", border_width=1, text_color=("black", "white")).pack(side=tk.RIGHT)
        ctk.CTkButton(opt_header_frame, text="Select All", command=self.select_all, width=100, corner_radius=50, fg_color="transparent", border_width=1, text_color=("black", "white")).pack(side=tk.RIGHT, padx=5)
        ctk.CTkButton(opt_header_frame, text="Download Selected", command=self.download_optionals, width=150, corner_radius=50).pack(side=tk.RIGHT, padx=5)
        
        # Frame for checkboxes
        checkbox_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        checkbox_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.source_names = {}
        for k in self.downloader.direct_urls.keys():
            if k == 'cm_high_low':
                self.source_names[k] = 'CM 52wk HighLow'
            elif k == 'corporates_pit':
                self.source_names[k] = 'Corporates PIT'
            elif k == 'bse_cash_bhavcopy':
                self.source_names[k] = 'BSE Cash Bhavcopy'
            else:
                self.source_names[k] = k.replace('_', ' ').title()
        
        row = 0
        col = 0
        self.checkbox_widgets = {}
        for key, name in self.source_names.items():
            is_checked = key in self.downloader.enabled_downloads
            var = tk.BooleanVar(value=is_checked)
            self.selected_downloads[key] = var
            cb = ctk.CTkCheckBox(
                checkbox_frame, 
                text=name, 
                variable=var, 
                command=lambda k=key: self.on_checkbox_toggle(k)
            )
            cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            self.checkbox_widgets[key] = cb
            
            col += 1
            if col > 4: # 5 columns
                col = 0
                row += 1



        # Time Schedule Section
        time_frame = ctk.CTkFrame(self.scrollable_dashboard)
        time_frame.pack(fill=tk.X, pady=2, padx=2)
        
        ctk.CTkLabel(time_frame, text="Schedule Times", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(2,0))
        
        time_inner_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        time_inner_frame.pack(fill=tk.X, padx=10, pady=2)
        
        # Auto Mode Checkbox
        self.auto_mode_var = tk.BooleanVar(value=self.downloader.auto_mode)
        self.auto_mode_check = ctk.CTkCheckBox(
            time_inner_frame,
            text="Auto Mode (8 AM - 8 PM, auto-start scheduler)",
            variable=self.auto_mode_var,
            command=self.toggle_auto_mode
        )
        self.auto_mode_check.pack(anchor=tk.W, pady=5)
        
        # Weekend Downloads Checkbox
        self.weekend_check = ctk.CTkCheckBox(
            time_inner_frame,
            text="Enable Weekend Downloads (Saturday & Sunday)",
            variable=self.weekend_downloads_var,
            command=self.toggle_weekend_downloads
        )
        self.weekend_check.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(time_inner_frame, text="Times (HH:MM, 24-hour, comma separated):", font=("Helvetica", 12)).pack(anchor=tk.W, pady=(10,0))
        
        self.time_var = tk.StringVar(value=", ".join(self.downloader.scheduled_times))
        time_entry = ctk.CTkEntry(time_inner_frame, textvariable=self.time_var, width=400)
        time_entry.pack(anchor=tk.W, pady=5)
        
        ctk.CTkLabel(time_inner_frame, text="Example: 09:30, 12:00, 15:30", font=("Helvetica", 11), text_color="gray").pack(anchor=tk.W)

        # Control Buttons
        button_frame = ctk.CTkFrame(self.scrollable_dashboard, fg_color="transparent")
        button_frame.pack(pady=5)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Scheduler",
            command=self.start_scheduler,
            width=120, height=30, corner_radius=50,
            font=("Helvetica", 12, "bold")
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop Scheduler",
            command=self.stop_scheduler,
            state="disabled",
            width=120, height=30, corner_radius=50,
            font=("Helvetica", 12, "bold")
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.manual_btn = ctk.CTkButton(
            button_frame,
            text="Download Now",
            command=self.manual_download,
            width=140, height=30, corner_radius=50,
            font=("Helvetica", 12, "bold")
        )
        self.manual_btn.pack(side=tk.LEFT, padx=10)
        
        # Progress Bar Section
        progress_frame = ctk.CTkFrame(self.scrollable_dashboard)
        progress_frame.pack(fill=tk.X, pady=2, padx=2)
        
        ctk.CTkLabel(progress_frame, text="Downloads Progress", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(2,0))
        
        prog_inner = ctk.CTkFrame(progress_frame, fg_color="transparent")
        prog_inner.pack(fill=tk.X, padx=10, pady=5)
        
        # Default Progress
        ctk.CTkLabel(prog_inner, text="Default (NIFTY 50, 500, Indices & Option Chain):", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
        self.progress_bar = ctk.CTkProgressBar(
            prog_inner,
            height=12,
            corner_radius=50,
            progress_color="#28a745" # Green
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=2, fill=tk.X)
        
        self.progress_label = ctk.CTkLabel(
            prog_inner, 
            text="Ready", 
            font=("Helvetica", 11)
        )
        self.progress_label.pack(anchor=tk.W)

        # Optional Progress
        ctk.CTkLabel(prog_inner, text=f"Optionals (Runs daily at {self.downloader.optional_download_time}):", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(5,0))
        self.opt_progress_bar = ctk.CTkProgressBar(
            prog_inner,
            height=12,
            corner_radius=50,
            progress_color="#28a745" # Green
        )
        self.opt_progress_bar.set(0)
        self.opt_progress_bar.pack(pady=2, fill=tk.X)
        
        self.opt_progress_label = ctk.CTkLabel(
            prog_inner, 
            text="Ready", 
            font=("Helvetica", 11)
        )
        self.opt_progress_label.pack(anchor=tk.W)
        
        # --- SETTINGS TAB ---
        self.create_settings_widgets()

    def create_settings_widgets(self):
        settings_container = ctk.CTkFrame(self.settings_tab, fg_color="transparent")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        path_frame = ctk.CTkFrame(settings_container)
        path_frame.pack(fill=tk.X, pady=5)
        ctk.CTkLabel(path_frame, text="Download Locations", font=("Helvetica", 14, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        
        # Source Selection
        path_inner_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(path_inner_frame, text="Source:", width=60).pack(side=tk.LEFT, padx=(0,10))
        
        # Get all source keys
        all_source_keys = ['nifty50', 'nifty500', 'market_indices', 'option_chain', 'eod_all'] + list(self.downloader.direct_urls.keys())
        all_source_names = {k: k.replace('_', ' ').title() for k in all_source_keys}
        all_source_names['nifty50'] = "NIFTY 50"
        all_source_names['nifty500'] = "NIFTY 500"
        all_source_names['market_indices'] = "Market Indices"
        all_source_names['eod_all'] = "EOD Data (All Optional Files)"
        all_source_names['cm_high_low'] = "CM 52wk HighLow"
        all_source_names['corporates_pit'] = "Corporates PIT"
        
        self.name_to_key = {v: k for k, v in all_source_names.items()}
        
        self.source_var = tk.StringVar(value=all_source_names['nifty500'])
        self.source_cb = ctk.CTkComboBox(path_inner_frame, variable=self.source_var, 
                                     values=list(all_source_names.values()), width=350, command=self.on_source_change)
        self.source_cb.pack(side=tk.LEFT, padx=5)
        
        # Path Entry
        path_entry_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ctk.CTkLabel(path_entry_frame, text="Path:", width=60).pack(side=tk.LEFT, padx=(0,10))
        self.download_path_var = tk.StringVar(value=self.downloader.download_paths.get('nifty500', ''))
        self.path_entry = ctk.CTkEntry(path_entry_frame, textvariable=self.download_path_var, width=400)
        self.path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ctk.CTkButton(path_entry_frame, text="Browse", command=self.browse_current_folder, width=100, corner_radius=50).pack(side=tk.LEFT, padx=10)

    def set_today(self):
        now = datetime.now()
        self.day_var.set(now.strftime("%d"))
        self.month_var.set(now.strftime("%B"))
        self.year_var.set(now.strftime("%Y"))
        
    def on_checkbox_toggle(self, changed_key=None):
        enabled = []
        for key, var in self.selected_downloads.items():
            if var.get():
                enabled.append(key)
        self.downloader.enabled_downloads = enabled
        self.downloader.save_config()
        
    def select_all(self):
        for key, var in self.selected_downloads.items():
            var.set(True)
        self.on_checkbox_toggle()
        
    def deselect_all(self):
        for key, var in self.selected_downloads.items():
            var.set(False)
        self.on_checkbox_toggle()
        
    def on_source_change(self, event=None):
        source = self.source_var.get()
        source_key = self.name_to_key.get(source)
        if source_key:
            self.download_path_var.set(self.downloader.download_paths.get(source_key, ""))
            
    def browse_current_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path_var.set(folder)
            source = self.source_var.get()
            source_key = self.name_to_key.get(source)
            if source_key:
                self.downloader.download_paths[source_key] = folder
                self.downloader.save_config()
                
    def get_selected_date(self):
        try:
            date_str = f"{self.day_var.get()} {self.month_var.get()} {self.year_var.get()}"
            return datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date selected")
            return None
            
    def manual_download(self):
        date = self.get_selected_date()
        if not date:
            return
            
        self.downloader.target_date = date
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.manual_btn.configure(state="disabled")
        
        threading.Thread(target=self.run_download_thread, args=('defaults',), daemon=True).start()
        
    def download_optionals(self):
        date = self.get_selected_date()
        if not date:
            return
            
        self.downloader.target_date = date
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.manual_btn.configure(state="disabled")
        
        threading.Thread(target=self.run_download_thread, args=('optionals',), daemon=True).start()
        
    def update_progress(self, value, message="", bar="main"):
        display_text = f"[{value}%] {message}" if message else f"{value}%"
        
        if bar == "main":
            self.progress_bar.set(value / 100.0)
            self.progress_label.configure(text=display_text)
        elif bar == "optional":
            self.opt_progress_bar.set(value / 100.0)
            self.opt_progress_label.configure(text=display_text)
            
        self.root.update_idletasks()
        
    def reset_progress(self):
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready")
        self.opt_progress_bar.set(0)
        self.opt_progress_label.configure(text="Ready")
        
        if not getattr(self, 'is_running', False):
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            if not getattr(self.downloader, 'auto_mode', False):
                self.manual_btn.configure(state="normal")
        else:
            self.stop_btn.configure(state="normal")
            self.start_btn.configure(state="disabled")
            if not getattr(self.downloader, 'auto_mode', False):
                self.manual_btn.configure(state="normal")
            
    def validate_time(self, time_str):
        try:
            datetime.strptime(time_str.strip(), "%H:%M")
            return True
        except ValueError:
            return False
            
    def validate_times(self, times_str):
        times = [t.strip() for t in times_str.split(",")]
        return all(self.validate_time(t) for t in times)
        
    def start_scheduler(self):
        times_str = self.time_var.get()
        if not self.validate_times(times_str):
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM (24-hour)")
            return
            
        self.downloader.scheduled_times = [t.strip() for t in times_str.split(",")]
        self.downloader.save_config()
        self.downloader.schedule_download()
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self.downloader.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.update_progress(0, f"Scheduler running — waiting for next download (Next: {schedule.next_run()})")
        
    def stop_scheduler(self):
        self.downloader.is_running = False
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        schedule.clear()
        self.update_progress(0, "Scheduler stopped")
        
    def run_download_thread(self, mode='all'):
        try:
            self.downloader.download_data(mode)
        except Exception as e:
            logging.error(f"Error during download: {str(e)}")
            self.update_progress(100, f"Error: {str(e)}", bar="main" if mode != 'optionals' else "optional")
        finally:
            self.root.after(0, self.reset_progress)
            
    def toggle_auto_mode(self):
        self.downloader.auto_mode = self.auto_mode_var.get()
        self.downloader.save_config()
        if self.downloader.auto_mode:
            self.check_and_start_auto_mode()
        else:
            if getattr(self, 'is_running', False):
                self.stop_scheduler()

    def toggle_weekend_downloads(self):
        self.downloader.weekend_downloads_enabled = self.weekend_downloads_var.get()
        self.downloader.save_config()

    def check_and_start_auto_mode(self):
        now = datetime.now()
        current_time = now.time()
        start_time = datetime.strptime("08:00", "%H:%M").time()
        end_time = datetime.strptime("20:00", "%H:%M").time()

        if start_time <= current_time <= end_time:
            if not self.downloader.is_running:
                self.start_scheduler()
                self.update_progress(0, "[Auto Mode] Scheduler started — waiting for next download")
        else:
            self.update_progress(0, "[Auto Mode] Outside active hours (8 AM - 8 PM)")


def main():
    # Use CTk instead of Tk
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = DownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
