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
        self.url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%20500"
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "NSE_Data")
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
                    self.download_path = config.get('download_path', self.download_path)
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
                'download_path': self.download_path,
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
        # chrome_options.add_argument('--disable-web-security')  # DISABLED
        # chrome_options.add_argument('--allow-running-insecure-content')  # DISABLED
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # DISABLED
        # chrome_options.add_experimental_option('useAutomationExtension', False)  # DISABLED
        
        # Set download preferences - CRITICAL for headless mode
        # Ensure absolute path
        self.download_path = os.path.abspath(self.download_path)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        
        prefs = {
            "download.default_directory": self.download_path,
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
        driver.execute_cdp_cmd("Browser.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": self.download_path,
            "eventsEnabled": True
        })
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": self.download_path
        })
        
        # Minimal automation hiding (keeping CDP commands that work)
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {  # DISABLED
        #     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        # })
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # DISABLED
        
        logging.info(f"Download path set to: {self.download_path}")
        print(f"Download path: {self.download_path}")
        
        return driver
    
    def download_data(self):
        """Download the CSV file from NSE website"""
        driver = None
        try:
            # Update progress: Starting
            if self.gui:
                self.gui.update_progress(10, "Starting browser...")
            
            logging.info(f"Starting download at {datetime.now()}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting download...")
            
            driver = self.setup_driver()
            
            # Update progress: Browser started
            if self.gui:
                self.gui.update_progress(20, "Establishing session...")
            
            # First, visit NSE homepage to get cookies and establish session
            logging.info("Establishing session with NSE...")
            driver.get("https://www.nseindia.com")
            time.sleep(7)  # Increased wait for reliable session establishment
            
            # Update progress: Session established
            if self.gui:
                self.gui.update_progress(40, "Navigating to NIFTY 500...")
            
            # Now visit the target page
            logging.info("Navigating to NIFTY 500 page...")
            driver.get(self.url)
            
            # Wait for page to load and dynamic content
            logging.info("Waiting for page to load...")
            time.sleep(10)
            
            # Update progress: Page loaded
            if self.gui:
                self.gui.update_progress(60, "Finding download button...")
            
            # Execute JavaScript to scroll if needed
            driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(2)
            
            # Wait for and click the download button
            wait = WebDriverWait(driver, 30)
            
            # Prioritize the exact span element with text verification
            selectors = [
                (By.XPATH, "//span[@id='dwldcsv' and text()='Download (.csv)']"),  # Most specific
                (By.ID, "dwldcsv"),  # Exact button ID
                (By.XPATH, "//span[@id='dwldcsv']"),
                (By.XPATH, "//*[@id='dwldcsv']"),
                (By.XPATH, "//a[contains(@id, 'dwldcsv')]"),
                (By.XPATH, "//button[contains(@id, 'dwldcsv')]"),
                (By.XPATH, "//span[@id='dwldcsv']/parent::*"),
                (By.XPATH, "//a[contains(text(), 'Download (.csv)')]"),
                (By.XPATH, "//a[contains(text(), 'Download') and contains(text(), 'csv')]"),
                (By.XPATH, "//button[contains(text(), 'Download (.csv)')]")
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
                        logging.info(f"✅ Found element: {element_html[:100]}")
                        print(f"✅ Found element: {element_html[:100]}")
                    logging.info(f"Found download button using selector: {by_method} = {selector_value}")
                    break
                except Exception as e:
                    logging.debug(f"Selector failed: {selector} - {str(e)}")
                    continue
            
            # Update progress: Button found
            if self.gui:
                self.gui.update_progress(70, "Clicking download button...")
            
            if download_button:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                time.sleep(1)
                
                # Try multiple click methods with detailed logging
                click_methods = [
                    ("Normal click", lambda btn: btn.click()),
                    ("JavaScript click", lambda btn: driver.execute_script("arguments[0].click();", btn)),
                    ("Navigate href", lambda btn: driver.get(btn.get_attribute('href')) if btn.get_attribute('href') else None),
                    ("JavaScript trigger", lambda btn: driver.execute_script("""
                        var event = new MouseEvent('click', {
                            view: window,
                            bubbles: true,
                            cancelable: true
                        });
                        arguments[0].dispatchEvent(event);
                    """, btn))
                ]
                
                for method, click_func in click_methods:
                    try:
                        click_func(download_button)
                        logging.info(f"✅ Clicked download button using method: {method}")
                        print(f"Download button clicked! Waiting for file...")
                        
                        # Update progress: Download initiated
                        if self.gui:
                            self.gui.update_progress(80, "Waiting for download...")
                        
                        # Brief wait to let download start
                        time.sleep(2)
                        break
                    except Exception as e:
                        logging.warning(f"Click method '{method}' failed: {e}")
                        continue
                
                # Rename the downloaded file with timestamp (will wait for download to complete)
                success = self.rename_downloaded_file()
                
                if success:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Download completed successfully!")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Download may have failed - check the folder manually")
                
                # Keep browser open for a moment so you can see what happened
                time.sleep(3)
            else:
                # Take screenshot for debugging
                screenshot_path = os.path.join(self.download_path, f"debug_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                driver.save_screenshot(screenshot_path)
                logging.error(f"Could not find download button. Screenshot saved to: {screenshot_path}")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: Could not find download button. Check log for details.")
            
        except Exception as e:
            logging.error(f"Error during download: {str(e)}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {str(e)}")
        finally:
            if driver:
                driver.quit()
    
    def rename_downloaded_file(self):
        """Rename the most recently downloaded CSV file with timestamp"""
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Looking for downloaded file in: {self.download_path}")
            logging.info(f"Searching for downloaded file in: {self.download_path}")
            
            # Wait for file to appear and download to complete
            max_wait = 60  # Increased to 60 seconds
            wait_count = 0
            latest_file = None
            
            # Check both configured path and default Downloads folder
            paths_to_check = [self.download_path]
            default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            if default_downloads != self.download_path and os.path.exists(default_downloads):
                paths_to_check.append(default_downloads)
            
            print(f"Checking paths: {paths_to_check}")
            
            while wait_count < max_wait:
                found_in_path = None
                # Look for ANY CSV file (including .crdownload for Chrome partial downloads)
                for check_path in paths_to_check:
                    if not os.path.exists(check_path):
                        continue
                        
                    all_files = os.listdir(check_path)
                    # Look for CSV files (case-insensitive) that aren't already renamed
                    csv_files = [f for f in all_files 
                                if f.lower().endswith('.csv') 
                                and not f.startswith('NIFTY500_')]
                    downloading = [f for f in all_files if f.endswith('.crdownload') or f.endswith('.tmp')]
                    
                    if wait_count == 0 or wait_count % 10 == 0:  # Log every 10 seconds
                        print(f"Wait {wait_count}s: Path '{os.path.basename(check_path)}' - Found {len(csv_files)} CSV, {len(downloading)} downloading...")
                    
                    if downloading:
                        print(f"Download in progress: {downloading[0]}")
                    
                    if csv_files:
                        # Get the most recent file
                        files_with_path = [os.path.join(check_path, f) for f in csv_files]
                        potential_file = max(files_with_path, key=os.path.getctime)
                        found_in_path = check_path
                        
                        print(f"Found CSV: {os.path.basename(potential_file)} in {os.path.basename(check_path)}")
                        
                        # Check if file size is stable (download completed)
                        if os.path.exists(potential_file):
                            size1 = os.path.getsize(potential_file)
                            time.sleep(2)
                            if os.path.exists(potential_file):
                                size2 = os.path.getsize(potential_file)
                                if size1 == size2 and size1 > 0:
                                    latest_file = potential_file
                                    print(f"File download complete! Size: {size1} bytes")
                                    
                                    # If found in default Downloads, move to configured path
                                    if found_in_path != self.download_path:
                                        print(f"Moving file from {os.path.basename(found_in_path)} to {os.path.basename(self.download_path)}")
                                    break
                        break
                
                if latest_file:
                    break
                    
                time.sleep(2)  # Check every 2 seconds
                wait_count += 2
            
            if not latest_file:
                error_msg = f"No new CSV file found after {max_wait} seconds in any location"
                logging.warning(error_msg)
                print(f"{error_msg}")
                
                # Update progress: Failed
                if self.gui:
                    self.gui.update_progress(100, "Download failed - no file found")
                
                return False
            
            # Create new filename with timestamp (format: HHMMmin)
            now = datetime.now()
            timestamp = now.strftime('%H%M')  # e.g., 1015 for 10:15 AM
            date_str = now.strftime('%Y%m%d')  # e.g., 20251001
            
            # Get the original file name
            original_name = os.path.basename(latest_file)
            
            # Create new filename: NIFTY500_YYYYMMDD_HHMMmin.csv
            new_filename = f"NIFTY500_{date_str}_{timestamp}min.csv"
            new_filepath = os.path.join(self.download_path, new_filename)
            
            # If file with same name exists, add a counter
            counter = 1
            while os.path.exists(new_filepath):
                new_filename = f"NIFTY500_{date_str}_{timestamp}min_{counter}.csv"
                new_filepath = os.path.join(self.download_path, new_filename)
                counter += 1
            
            # Rename the file
            if os.path.exists(latest_file):
                os.rename(latest_file, new_filepath)
                logging.info(f"File renamed from '{original_name}' to '{new_filename}'")
                print(f"✅ File saved as: {new_filename}")
                
                # Update progress: Complete
                if self.gui:
                    self.gui.update_progress(100, "Download complete!")
                
                return True
            else:
                logging.error(f"File disappeared before rename: {latest_file}")
                print(f"Error: File disappeared before rename")
                
                # Update progress: Failed
                if self.gui:
                    self.gui.update_progress(100, "Download failed - file disappeared")
                
                return False
            
        except Exception as e:
            logging.error(f"Error renaming file: {str(e)}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error: Could not rename file - {str(e)}")
            return False
    
    def schedule_download(self):
        """Schedule the download job for multiple times"""
        schedule.clear()
        for time_str in self.scheduled_times:
            schedule.every().day.at(time_str).do(self.download_data)
            logging.info(f"Download scheduled for {time_str} daily")
        
        times_display = ", ".join(self.scheduled_times)
        print(f"Download scheduled for {times_display} daily")
    
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
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        self.downloader = NSEDownloader(gui=self)
        self.scheduler_thread = None
        
        self.create_widgets()
        self.update_status()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="NSE NIFTY 500 Data Downloader",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Download Path Section
        path_frame = ttk.LabelFrame(main_frame, text="Download Location", padding="10")
        path_frame.pack(fill=tk.X, pady=10)
        
        self.path_var = tk.StringVar(value=self.downloader.download_path)
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT)
        
        # Time Schedule Section
        time_frame = ttk.LabelFrame(main_frame, text="Schedule Times", padding="10")
        time_frame.pack(fill=tk.X, pady=10)
        
        time_label = ttk.Label(time_frame, text="Download Times:")
        time_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        time_info = ttk.Label(time_frame, text="(HH:MM, 24-hour format, separate multiple times with commas)", font=("Arial", 8))
        time_info.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Display current times
        self.time_var = tk.StringVar(value=", ".join(self.downloader.scheduled_times))
        time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=40)
        time_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        
        example_label = ttk.Label(time_frame, text="Example: 09:30, 12:00, 15:30", font=("Arial", 8), foreground="gray")
        example_label.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky=tk.W)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(
            button_frame,
            text="Start Scheduler",
            command=self.start_scheduler,
            width=20
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop Scheduler",
            command=self.stop_scheduler,
            state=tk.DISABLED,
            width=20
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Manual Download Button
        manual_btn = ttk.Button(
            main_frame,
            text="Download Now",
            command=self.manual_download,
            width=20
        )
        manual_btn.pack(pady=10)
        
        # Progress Bar Section
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready", font=("Arial", 9))
        self.progress_label.pack(pady=2)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=8, width=60, state=tk.DISABLED)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Info Label
        info_label = ttk.Label(
            main_frame,
            text="Note: Keep this window open for scheduled downloads to work.",
            font=("Arial", 9, "italic"),
            foreground="blue"
        )
        info_label.pack()
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)
    
    def update_progress(self, value, message=""):
        """Update progress bar and message"""
        self.progress_var.set(value)
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def update_status(self, message=None):
        if message:
            self.status_text.config(state=tk.NORMAL)
            self.status_text.insert(tk.END, f"{message}\n")
            self.status_text.see(tk.END)
            self.status_text.config(state=tk.DISABLED)
    
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
        self.downloader.download_path = self.path_var.get()
        self.downloader.scheduled_times = result  # result contains the list of times
        self.downloader.save_config()
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.downloader.download_path):
            os.makedirs(self.downloader.download_path)
        
        # Setup and start scheduler
        self.downloader.schedule_download()
        
        # Start scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.downloader.run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        times_display = ", ".join(self.downloader.scheduled_times)
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler started. Downloads scheduled for: {times_display}"
        self.update_status(message)
    
    def stop_scheduler(self):
        self.downloader.is_running = False
        schedule.clear()
        
        # Update UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler stopped."
        self.update_status(message)
    
    def manual_download(self):
        # Update download path
        self.downloader.download_path = self.path_var.get()
        
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting manual download..."
        self.update_status(message)
        
        # Run download in a separate thread to avoid freezing GUI
        download_thread = threading.Thread(target=self._run_manual_download, daemon=True)
        download_thread.start()
    
    def _run_manual_download(self):
        self.downloader.download_data()
        self.update_status(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Manual download completed.")


def main():
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
