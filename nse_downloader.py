import os
import sys
import time
import schedule
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import requests
from urllib.parse import urlencode

class NSEDownloader:
    def __init__(self, gui=None):
        # URLs for both websites
        self.urls = {
            'nifty500': "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%20500",
            'market_indices': "https://www.nseindia.com/market-data/live-market-indices"
        }
        
        # Download paths for each source
        self.download_paths = {
            'nifty500': os.path.join(os.path.expanduser("~"), "Downloads", "NSE_Data", "NIFTY500"),
            'market_indices': os.path.join(os.path.expanduser("~"), "Downloads", "NSE_Data", "Market_Indices")
        }
        
        self.scheduled_times = ["09:30"]  # Now supports multiple times
        self.is_running = False
        self.config_file = "config.json"
        self.gui = gui
        self.headless_mode = True  # Run browser hidden in background
        self.load_config()
        
        # Setup logging
        logging.basicConfig(
            filename='nse_downloader.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Load custom paths if available
                    if 'download_paths' in config:
                        self.download_paths.update(config.get('download_paths', {}))
                    # Support both old single time and new multiple times
                    if 'scheduled_times' in config:
                        self.scheduled_times = config.get('scheduled_times', self.scheduled_times)
                    elif 'scheduled_time' in config:
                        # Convert old single time to list
                        self.scheduled_times = [config.get('scheduled_time', "09:30")]
            except Exception as e:
                logging.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'download_paths': self.download_paths,
                'scheduled_times': self.scheduled_times
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
    
    def download_from_source(self, driver, source_name, url, download_path, progress_offset=0, extra_wait=0):
        """Download from a specific NSE source
        
        Args:
            driver: Selenium WebDriver instance
            source_name: Name of the source (e.g., 'NIFTY500', 'Market_Indices')
            url: URL to download from
            download_path: Path to save downloads
            progress_offset: Offset for progress bar (0 or 50)
            extra_wait: Extra seconds to wait after clicking download (for slow sites)
        """
        try:
            # CRITICAL: Set download path for this specific source via CDP
            abs_download_path = os.path.abspath(download_path)
            logging.info(f"Setting download path to: {abs_download_path}")
            
            # Update progress: Setting download path
            if self.gui:
                self.gui.update_progress(progress_offset + 15, f"Configuring download path for {source_name}...")
            
            driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": abs_download_path,
                "eventsEnabled": True
            })
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": abs_download_path
            })
            time.sleep(1)  # Brief wait for CDP command to take effect
            
            # Update progress: Navigating
            if self.gui:
                self.gui.update_progress(progress_offset + 20, f"Navigating to {source_name} page...")
            
            # Visit the target page
            logging.info(f"Navigating to {source_name} page...")
            driver.get(url)
            
            # Update progress: Page loading
            if self.gui:
                self.gui.update_progress(progress_offset + 25, f"Loading {source_name} page...")
            
            # Wait for page to load and dynamic content
            logging.info("Waiting for page to load...")
            time.sleep(10)
            
            # Update progress: Scrolling page
            if self.gui:
                self.gui.update_progress(progress_offset + 28, f"Scrolling page for {source_name}...")
            
            # Execute JavaScript to scroll if needed
            driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(2)
            
            # Update progress: Finding button
            if self.gui:
                self.gui.update_progress(progress_offset + 30, f"Searching for download button...")
            
            # Wait for and click the download button
            wait = WebDriverWait(driver, 30)
            
            # Prioritize the exact span element with text verification
            selectors = [
                (By.XPATH, "//span[@id='dwldcsv' and text()='Download (.csv)']"),  # Most specific
                (By.ID, "dwldcsv"),  # Exact button ID
                (By.XPATH, "//span[@id='dwldcsv']"),
                (By.XPATH, "//*[@id='dwldcsv']"),
            ]
            
            download_button = None
            for i, selector in enumerate(selectors):
                try:
                    by_method, selector_value = selector
                    logging.info(f"Trying selector {i+1}/{len(selectors)}: {by_method} = {selector_value}")
                    download_button = wait.until(
                        EC.element_to_be_clickable(selector)
                    )
                    element_html = download_button.get_attribute('outerHTML')
                    if element_html:
                        logging.info(f"✅ Found element for {source_name}: {element_html[:100]}")
                        print(f"✅ Found element for {source_name}")
                    
                    # Update progress: Button found
                    if self.gui:
                        self.gui.update_progress(progress_offset + 33, f"Download button found for {source_name}!")
                    break
                except Exception as e:
                    logging.debug(f"Selector failed: {selector} - {str(e)}")
                    continue
            
            # Update progress: Clicking button
            if self.gui:
                self.gui.update_progress(progress_offset + 35, f"Clicking download button...")
            
            if download_button:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                time.sleep(1)
                
                # Try multiple click methods
                click_methods = [
                    ("Normal click", lambda btn: btn.click()),
                    ("JavaScript click", lambda btn: driver.execute_script("arguments[0].click();", btn)),
                ]
                
                for method, click_func in click_methods:
                    try:
                        click_func(download_button)
                        logging.info(f"✅ Clicked download button for {source_name} using method: {method}")
                        print(f"Download button clicked for {source_name}!")
                        
                        # Update progress: Button clicked
                        if self.gui:
                            self.gui.update_progress(progress_offset + 37, f"Button clicked! Initiating download...")
                        
                        # Wait to let download start (extra wait for slow sites)
                        wait_time = 3 + extra_wait
                        logging.info(f"Waiting {wait_time} seconds for download to initiate...")
                        
                        # Update progress: Downloading
                        if self.gui:
                            self.gui.update_progress(progress_offset + 40, f"Downloading {source_name} file...")
                        
                        time.sleep(wait_time)
                        break
                    except Exception as e:
                        logging.warning(f"Click method '{method}' failed for {source_name}: {e}")
                        continue
                
                return True
            else:
                logging.error(f"Could not find download button for {source_name}")
                return False
                
        except Exception as e:
            logging.error(f"Error downloading from {source_name}: {str(e)}")
            print(f"Error downloading from {source_name}: {str(e)}")
            return False
    
    def download_data(self):
        """Download CSV files from both NSE sources"""
        driver = None
        try:
            # Update progress: Starting
            if self.gui:
                self.gui.update_progress(5, "Starting browser...")
            
            logging.info(f"Starting downloads at {datetime.now()}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting downloads...")
            
            driver = self.setup_driver()
            
            # Update progress: Browser started
            if self.gui:
                self.gui.update_progress(10, "Browser started! Connecting to NSE...")
            
            # First, visit NSE homepage to get cookies and establish session
            logging.info("Establishing session with NSE...")
            driver.get("https://www.nseindia.com")
            
            # Update progress: Session establishing
            if self.gui:
                self.gui.update_progress(12, "Establishing session with NSE India...")
            
            time.sleep(7)  # Increased wait for reliable session establishment
            
            # Download from NIFTY 500
            logging.info("=" * 50)
            logging.info("DOWNLOADING FROM NIFTY 500")
            logging.info("=" * 50)
            success_nifty500 = self.download_from_source(
                driver, 
                "NIFTY 500", 
                self.urls['nifty500'], 
                self.download_paths['nifty500'],
                progress_offset=0,
                extra_wait=0  # Standard wait for NIFTY 500
            )
            
            # Download from Market Indices
            logging.info("=" * 50)
            logging.info("DOWNLOADING FROM MARKET INDICES")
            logging.info("=" * 50)
            
            # Update progress: Preparing for second download
            if self.gui:
                self.gui.update_progress(50, "Preparing for Market Indices download...")
            
            # Re-establish session for second download (longer wait to avoid blocking)
            logging.info("Re-establishing session for Market Indices...")
            driver.get("https://www.nseindia.com")
            
            # Update progress: Re-establishing session
            if self.gui:
                self.gui.update_progress(52, "Re-establishing session for Market Indices...")
            
            time.sleep(8)  # Longer wait to avoid being blocked
            
            success_market = self.download_from_source(
                driver, 
                "Market Indices", 
                self.urls['market_indices'], 
                self.download_paths['market_indices'],
                progress_offset=50,
                extra_wait=5  # Extra 5 seconds wait for Market Indices (slower download)
            )
            
            # Update progress: Downloads initiated
            if self.gui:
                self.gui.update_progress(90, "Verifying downloaded files...")
            
            # Rename both downloaded files
            renamed_files = []
            
            if success_nifty500:
                # Update progress: Processing NIFTY 500 file
                if self.gui:
                    self.gui.update_progress(92, "Renaming NIFTY 500 file...")
                renamed = self.rename_downloaded_file('nifty500', self.download_paths['nifty500'])
                if renamed:
                    renamed_files.append(renamed)
            
            if success_market:
                # Update progress: Processing Market Indices file
                if self.gui:
                    self.gui.update_progress(95, "Renaming Market Indices file...")
                renamed = self.rename_downloaded_file('market_indices', self.download_paths['market_indices'])
                if renamed:
                    renamed_files.append(renamed)
            
            # Update progress: Finalizing
            if self.gui:
                self.gui.update_progress(98, "Finalizing downloads...")
            
            # Update progress: Complete
            if self.gui:
                files_msg = f"Complete! Downloaded {len(renamed_files)} file(s)" if renamed_files else "Process complete"
                self.gui.update_progress(100, files_msg)
            
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
    
    def rename_downloaded_file(self, source_name, download_path):
        """Rename the most recently downloaded CSV file with timestamp
        
        Args:
            source_name: Name of source ('nifty500' or 'market_indices')
            download_path: Path where file was downloaded
        
        Returns:
            str: New filename if successful, None if failed
        """
        try:
            logging.info(f"Searching for downloaded file from {source_name} in: {download_path}")
            
            # Wait for file to appear and download to complete
            max_wait = 60
            wait_count = 0
            latest_file = None
            
            # Check both configured path and default Downloads folder
            paths_to_check = [download_path]
            default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            if default_downloads != download_path and os.path.exists(default_downloads):
                paths_to_check.append(default_downloads)
            
            # Ensure download path exists
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            
            print(f"Checking paths for {source_name}: {paths_to_check}")
            
            while wait_count < max_wait:
                found_in_path = None
                # Look for ANY CSV file
                for check_path in paths_to_check:
                    if not os.path.exists(check_path):
                        continue
                        
                    all_files = os.listdir(check_path)
                    # Look for CSV files (case-insensitive) that aren't already renamed
                    csv_files = [f for f in all_files 
                                if f.lower().endswith('.csv') 
                                and not ('_' in f and '-' in f)]  # Skip already renamed files
                    downloading = [f for f in all_files if f.endswith('.crdownload') or f.endswith('.tmp')]
                    
                    if wait_count == 0 or wait_count % 10 == 0:
                        print(f"  {source_name} Wait {wait_count}s: Found {len(csv_files)} CSV, {len(downloading)} downloading...")
                    
                    if csv_files:
                        # Get the most recent file
                        files_with_path = [os.path.join(check_path, f) for f in csv_files]
                        potential_file = max(files_with_path, key=os.path.getctime)
                        found_in_path = check_path
                        
                        # Check if file size is stable (download completed)
                        if os.path.exists(potential_file):
                            size1 = os.path.getsize(potential_file)
                            time.sleep(2)
                            if os.path.exists(potential_file):
                                size2 = os.path.getsize(potential_file)
                                if size1 == size2 and size1 > 0:
                                    latest_file = potential_file
                                    print(f"  {source_name} file download complete! Size: {size1} bytes")
                                    break
                        break
                
                if latest_file:
                    break
                    
                time.sleep(2)
                wait_count += 2
            
            if not latest_file:
                logging.warning(f"No new CSV file found for {source_name} after {max_wait} seconds")
                print(f"  ⚠️ No file found for {source_name}")
                return None
            
            # Create new filename with timestamp (format: ddmmyy-hhmmmin)
            now = datetime.now()
            date_str = now.strftime('%d%m%y')  # e.g., 011025 for Oct 1, 2025
            time_str = now.strftime('%H%M')   # e.g., 1425 for 2:25 PM
            
            # Get original filename (without extension)
            original_name = os.path.basename(latest_file)
            original_base = os.path.splitext(original_name)[0]
            
            # Create new filename based on source (with "min" suffix)
            if source_name == 'nifty500':
                prefix = "NIFTY500"
            else:  # market_indices
                prefix = "MarketIndices"
            
            new_filename = f"{prefix}_{date_str}-{time_str}min.csv"
            new_filepath = os.path.join(download_path, new_filename)
            
            # If file with same name exists, add counter
            counter = 1
            while os.path.exists(new_filepath):
                new_filename = f"{prefix}_{date_str}-{time_str}min_{counter}.csv"
                new_filepath = os.path.join(download_path, new_filename)
                counter += 1
            
            # Move and rename the file
            if os.path.exists(latest_file):
                # If file is in different folder, move it
                if os.path.dirname(latest_file) != download_path:
                    import shutil
                    shutil.move(latest_file, new_filepath)
                else:
                    os.rename(latest_file, new_filepath)
                
                logging.info(f"File renamed from '{original_name}' to '{new_filename}'")
                print(f"  ✅ {source_name}: {new_filename}")
                return new_filename
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
        
        # Get current day (0=Monday, 6=Sunday)
        current_day = datetime.now().weekday()
        
        # Check if it's Saturday (5) or Sunday (6)
        if current_day == 5:  # Saturday
            message = "It's Saturday - Market is closed. Skipping scheduled download."
            logging.info(message)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
            if self.gui:
                self.gui.update_progress(0, "Weekend - Market closed")
            return
        elif current_day == 6:  # Sunday
            message = "It's Sunday - Market is closed. Skipping scheduled download."
            logging.info(message)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
            if self.gui:
                self.gui.update_progress(0, "Weekend - Market closed")
            return
        
        # Weekday - proceed with download
        logging.info("Weekday detected - Proceeding with scheduled download")
        self.download_data()
    
    def schedule_download(self):
        """Schedule the download job for multiple times"""
        schedule.clear()
        for time_str in self.scheduled_times:
            # Use wrapper function that checks for weekends
            schedule.every().day.at(time_str).do(self.scheduled_download_wrapper)
            logging.info(f"Download scheduled for {time_str} daily (Mon-Fri only)")
        
        times_display = ", ".join(self.scheduled_times)
        print(f"Download scheduled for {times_display} daily (Monday-Friday only)")
    
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
        self.root.geometry("650x460")  # Increased height for better spacing
        self.root.resizable(False, False)
        
        self.downloader = NSEDownloader(gui=self)
        self.scheduler_thread = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title - smaller and more compact
        title_label = tk.Label(
            self.root,
            text="NSE Data Downloader",
            font=("Arial", 14, "bold"),
            pady=5
        )
        title_label.pack()
        
        # Main frame - reduced padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Download Path Section - Show both download locations (compact)
        path_frame = ttk.LabelFrame(main_frame, text="Download Locations", padding="8")
        path_frame.pack(fill=tk.X, pady=5)
        
        # NIFTY 500 path - compact layout
        ttk.Label(path_frame, text="NIFTY 500:", width=12).grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)
        self.nifty_path_var = tk.StringVar(value=self.downloader.download_paths['nifty500'])
        nifty_entry = ttk.Entry(path_frame, textvariable=self.nifty_path_var, width=48)
        nifty_entry.grid(row=0, column=1, padx=3, pady=2)
        ttk.Button(path_frame, text="Browse", command=lambda: self.browse_folder('nifty500'), width=8).grid(row=0, column=2, padx=3, pady=2)
        
        # Market Indices path - compact layout
        ttk.Label(path_frame, text="Market Indices:", width=12).grid(row=1, column=0, padx=3, pady=2, sticky=tk.W)
        self.market_path_var = tk.StringVar(value=self.downloader.download_paths['market_indices'])
        market_entry = ttk.Entry(path_frame, textvariable=self.market_path_var, width=48)
        market_entry.grid(row=1, column=1, padx=3, pady=2)
        ttk.Button(path_frame, text="Browse", command=lambda: self.browse_folder('market_indices'), width=8).grid(row=1, column=2, padx=3, pady=2)
        
        # Time Schedule Section - compact
        time_frame = ttk.LabelFrame(main_frame, text="Schedule Times", padding="8")
        time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(time_frame, text="Times (HH:MM, 24-hour, comma separated):", font=("Arial", 8)).pack(anchor=tk.W, padx=3, pady=2)
        
        # Display current times
        self.time_var = tk.StringVar(value=", ".join(self.downloader.scheduled_times))
        time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=40)
        time_entry.pack(padx=3, pady=2, fill=tk.X)
        
        ttk.Label(time_frame, text="Example: 09:30, 12:00, 15:30", font=("Arial", 7), foreground="gray").pack(anchor=tk.W, padx=3)
        
        # Control Buttons - compact
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=8)
        
        self.start_btn = ttk.Button(
            button_frame,
            text="Start Scheduler",
            command=self.start_scheduler,
            width=18
        )
        self.start_btn.pack(side=tk.LEFT, padx=3)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop Scheduler",
            command=self.stop_scheduler,
            state=tk.DISABLED,
            width=18
        )
        self.stop_btn.pack(side=tk.LEFT, padx=3)
        
        # Manual Download Button
        manual_btn = ttk.Button(
            button_frame,
            text="Download Now",
            command=self.manual_download,
            width=18
        )
        manual_btn.pack(side=tk.LEFT, padx=3)
        
        # Progress Bar Section - compact
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="8")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=520
        )
        self.progress_bar.pack(pady=3)
        
        # Progress status label - black color instead of blue
        self.progress_label = ttk.Label(
            progress_frame, 
            text="Ready", 
            font=("Arial", 9, "bold"),
            foreground="#000000"  # Changed from blue to black
        )
        self.progress_label.pack(pady=3)
        
        # Info Label - shorter text to avoid cutoff
        info_label = ttk.Label(
            main_frame,
            text="Keep window open for scheduled downloads (Mon-Fri only)",
            font=("Arial", 8, "italic"),
            foreground="#555555"
        )
        info_label.pack(pady=2)
    
    def browse_folder(self, source_key):
        """Browse for download folder for a specific source"""
        folder = filedialog.askdirectory()
        if folder:
            if source_key == 'nifty500':
                self.nifty_path_var.set(folder)
            elif source_key == 'market_indices':
                self.market_path_var.set(folder)
    
    def update_progress(self, value, message=""):
        """Update progress bar and message"""
        self.progress_var.set(value)
        # Show percentage and message
        display_text = f"[{value}%] {message}" if message else f"{value}%"
        self.progress_label.config(text=display_text)
        self.root.update_idletasks()
    
    def validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.strip().split(":")
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour < 24 and 0 <= minute < 60
        except:
            return False
    
    def validate_times(self, times_str):
        """Validate multiple times separated by commas"""
        times = [t.strip() for t in times_str.split(",")]
        for time_str in times:
            if not self.validate_time(time_str):
                return False, time_str
        return True, times
    
    def start_scheduler(self):
        # Validate inputs
        valid, result = self.validate_times(self.time_var.get())
        if not valid:
            messagebox.showerror("Invalid Time", f"Invalid time format: '{result}'\nPlease enter times in HH:MM format (24-hour)\nSeparate multiple times with commas")
            return
        
        # Update downloader settings
        self.downloader.download_paths['nifty500'] = self.nifty_path_var.get()
        self.downloader.download_paths['market_indices'] = self.market_path_var.get()
        self.downloader.scheduled_times = result  # result contains the list of times
        self.downloader.save_config()
        
        # Create download directories if they don't exist
        for path in self.downloader.download_paths.values():
            if not os.path.exists(path):
                os.makedirs(path)
        
        # Setup and start scheduler
        self.downloader.schedule_download()
        
        # Check if today is weekend and show info
        from datetime import datetime
        current_day = datetime.now().weekday()
        day_name = datetime.now().strftime('%A')
        
        if current_day in [5, 6]:  # Saturday or Sunday
            messagebox.showinfo(
                "Weekend Detected", 
                f"Today is {day_name}.\n\nThe market is closed on weekends.\nScheduled downloads will run on weekdays (Monday-Friday) only.\n\nYou can still use 'Download Now' for manual downloads."
            )
        
        # Start scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.downloader.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
    
    def stop_scheduler(self):
        self.downloader.is_running = False
        schedule.clear()
        
        # Update UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def manual_download(self):
        # Update download paths
        self.downloader.download_paths['nifty500'] = self.nifty_path_var.get()
        self.downloader.download_paths['market_indices'] = self.market_path_var.get()
        
        # Run download in a separate thread to avoid freezing GUI
        download_thread = threading.Thread(target=self._run_manual_download, daemon=True)
        download_thread.start()
    
    def _run_manual_download(self):
        self.downloader.download_data()


def main():
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
