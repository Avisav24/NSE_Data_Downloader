# NSE Downloader - Fix for DEPRECATED_ENDPOINT Error

## Problem

NSE India website was returning "DEPRECATED_ENDPOINT" error when trying to access the download functionality directly. This happens because NSE has implemented stricter security measures to detect and block automated scraping.

## Solutions Implemented

### 1. **Enhanced Browser Automation Detection Prevention**

- Added Chrome DevTools Protocol (CDP) commands to hide automation
- Set `navigator.webdriver` to undefined using JavaScript injection
- Added more stealth arguments to Chrome options

### 2. **Session Establishment**

- Now first visits NSE homepage (`https://www.nseindia.com`) to establish a proper session
- Gets necessary cookies before accessing the target page
- Waits 5 seconds for session establishment
- Then navigates to the NIFTY 500 page

### 3. **Proper Headers Setup**

- Added comprehensive browser headers including:
  - User-Agent
  - Accept headers
  - Accept-Language
  - Sec-Fetch-\* headers
  - Cache-Control

### 4. **Increased Wait Times**

- Extended page load wait time to 10 seconds
- Allows dynamic content to fully load before attempting to find the download button

### 5. **Additional Security Bypasses**

- Disabled web security checks
- Allowed running insecure content
- Added proper CDP commands for user agent override

## Technical Changes

### Files Modified:

1. **nse_downloader.py**

   - Added `requests` library import
   - Added `get_nse_headers()` method
   - Enhanced `setup_driver()` with CDP commands
   - Modified `download_data()` to visit homepage first

2. **requirements.txt**
   - Added `requests==2.31.0`

## How It Works Now

1. **Session Setup**: Opens NSE homepage to get cookies
2. **Navigation**: Visits the NIFTY 500 page with proper session
3. **Wait**: Gives time for dynamic content to load
4. **Detection**: Tries multiple XPath selectors to find download button
5. **Click**: Uses both normal and JavaScript click methods
6. **Download**: Waits for file to download completely

## Testing

To test the fix:

```powershell
python nse_downloader.py
```

Then click "Download Now" button in the GUI.

## Troubleshooting

If you still encounter issues:

1. **Check the log file** (`nse_downloader.log`) for detailed error messages
2. **Look for debug screenshot** in your download folder if button not found
3. **Verify Chrome browser** is up to date
4. **Try non-headless mode** temporarily by commenting out the `--headless` argument to see what's happening

## Alternative: Manual Browser Mode

If the automated approach still fails, you can temporarily disable headless mode to see the browser:

In `nse_downloader.py`, line ~75, comment out:

```python
# chrome_options.add_argument('--headless')  # Run in background
```

This will show the browser window and help debug the issue.

## Notes

- NSE India may update their website structure at any time
- If downloads stop working, check if the button text or HTML structure has changed
- The script includes debug screenshots that save when the button cannot be found
- Keep your Chrome browser and ChromeDriver updated
