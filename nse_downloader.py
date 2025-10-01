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
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import requests
from urllib.parse import urlencode

class NSEDownloader:
    def __init__(self):
        self.url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%20500"
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "NSE_Data")
        self.scheduled_time = "09:30"
        self.is_running = False
        self.config_file = "config.json"
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
                    self.scheduled_time = config.get('scheduled_time', self.scheduled_time)
            except Exception as e:
                logging.error(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'download_path': self.download_path,
                'scheduled_time': self.scheduled_time
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
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set download preferences
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        
        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute CDP commands to hide automation
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def download_data(self):
        """Download the CSV file from NSE website"""
        driver = None
        try:
            logging.info(f"Starting download at {datetime.now()}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting download...")
            
            driver = self.setup_driver()
            
            # First, visit NSE homepage to get cookies and establish session
            logging.info("Establishing session with NSE...")
            driver.get("https://www.nseindia.com")
            time.sleep(5)
            
            # Now visit the target page
            logging.info("Navigating to NIFTY 500 page...")
            driver.get(self.url)
            
            # Wait for page to load and dynamic content
            logging.info("Waiting for page to load...")
            time.sleep(10)
            
            # Execute JavaScript to scroll if needed
            driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(2)
            
            # Wait for and click the download button
            wait = WebDriverWait(driver, 30)
            
            # Try to find the button using the exact ID first, then fallback to other selectors
            selectors = [
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
                    logging.info(f"Found download button using selector: {by_method} = {selector_value}")
                    break
                except Exception as e:
                    logging.debug(f"Selector failed: {selector} - {str(e)}")
                    continue
            
            if download_button:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                time.sleep(1)
                
                # Try to click
                try:
                    download_button.click()
                except:
                    # Try JavaScript click as fallback
                    driver.execute_script("arguments[0].click();", download_button)
                
                logging.info("Download button clicked successfully")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Download completed successfully!")
                
                # Wait for download to complete
                time.sleep(10)
                
                # Rename the downloaded file with timestamp
                self.rename_downloaded_file()
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
            # Get the most recently downloaded file in the download directory
            files = [f for f in os.listdir(self.download_path) if f.endswith('.csv')]
            
            if not files:
                logging.warning("No CSV file found to rename")
                return
            
            # Get the most recent file
            files_with_path = [os.path.join(self.download_path, f) for f in files]
            latest_file = max(files_with_path, key=os.path.getctime)
            
            # Create new filename with timestamp (format: HHMMmin)
            now = datetime.now()
            timestamp = now.strftime('%H%M')  # e.g., 1015 for 10:15 AM
            date_str = now.strftime('%Y%m%d')  # e.g., 20251001
            
            # Get the original file extension
            original_name = os.path.basename(latest_file)
            
            # Create new filename: NIFTY500_YYYYMMDD_HHMMmin.csv
            new_filename = f"NIFTY500_{date_str}_{timestamp}min.csv"
            new_filepath = os.path.join(self.download_path, new_filename)
            
            # Rename the file
            if os.path.exists(latest_file):
                os.rename(latest_file, new_filepath)
                logging.info(f"File renamed from '{original_name}' to '{new_filename}'")
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] File saved as: {new_filename}")
            
        except Exception as e:
            logging.error(f"Error renaming file: {str(e)}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Warning: Could not rename file - {str(e)}")
    
    def schedule_download(self):
        """Schedule the download job"""
        schedule.clear()
        schedule.every().day.at(self.scheduled_time).do(self.download_data)
        logging.info(f"Download scheduled for {self.scheduled_time} daily")
        print(f"Download scheduled for {self.scheduled_time} daily")
    
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
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.downloader = NSEDownloader()
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
        time_frame = ttk.LabelFrame(main_frame, text="Schedule Time", padding="10")
        time_frame.pack(fill=tk.X, pady=10)
        
        time_label = ttk.Label(time_frame, text="Download Time (HH:MM):")
        time_label.pack(side=tk.LEFT, padx=5)
        
        self.time_var = tk.StringVar(value=self.downloader.scheduled_time)
        time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=10)
        time_entry.pack(side=tk.LEFT, padx=5)
        
        time_info = ttk.Label(time_frame, text="(24-hour format)", font=("Arial", 8))
        time_info.pack(side=tk.LEFT)
        
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
    
    def update_status(self, message=None):
        if message:
            self.status_text.config(state=tk.NORMAL)
            self.status_text.insert(tk.END, f"{message}\n")
            self.status_text.see(tk.END)
            self.status_text.config(state=tk.DISABLED)
    
    def validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour < 24 and 0 <= minute < 60
        except:
            return False
    
    def start_scheduler(self):
        # Validate inputs
        if not self.validate_time(self.time_var.get()):
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format (24-hour)")
            return
        
        # Update downloader settings
        self.downloader.download_path = self.path_var.get()
        self.downloader.scheduled_time = self.time_var.get()
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
        
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler started. Download scheduled for {self.downloader.scheduled_time} daily."
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
