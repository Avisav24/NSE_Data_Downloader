# NSE Data Downloader

A powerful desktop application to automatically download **NIFTY 500** and **Market Indices** data from NSE India website at scheduled times with automatic file naming, smart download detection, **hidden browser mode** for background operation, and **weekend-aware scheduling**.

## 📥 Quick Download (No Python Needed!)

**For Windows users**: Download the ready-to-use executable with all latest features!

### 🚀 Direct Download Link

👉 **[Download NSE_DataDownloader.exe](https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_DataDownloader.exe)** (~54 MB)

🔗 **Direct URL**: `https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_DataDownloader.exe`

**Alternative**: Browse to [releases folder](releases/) and download from there.

### ✨ What's New in v3.0 (Latest)

- 📊 **Dual-Source Downloads**: Download from both NIFTY 500 and Market Indices simultaneously!
- 🗓️ **Weekend Detection**: Automatically skips downloads on Saturday & Sunday (market closed)
- � **Separate Folders**: Each data source saves to its own folder
- 🏷️ **Enhanced File Naming**: New format `NIFTY500_ddmmyy-hhmmmin.csv` (e.g., `NIFTY500_031025-1425min.csv`)
- 🎨 **Compact GUI**: Redesigned interface (680×450px) with wider path fields
- � **28 Progress Stages**: Detailed progress from "Configuring" to "Downloading" with percentages
- �️ **Startup Ready**: Perfect for Windows startup apps with smart weekend handling
- ⚡ **Faster Downloads**: CDP download path control for each source

### ✨ Why Use the Executable?

- ✅ No Python installation required
- ✅ No dependencies to install
- ✅ Just download and double-click to run!
- ✅ Download from TWO NSE sources automatically
- ✅ Weekend-aware scheduling (Mon-Fri only)
- ✅ Auto-updates ChromeDriver
- ✅ Browser runs hidden in background
- ✅ Perfect for Windows startup apps

📖 See [releases/README.md](releases/README.md) for detailed usage instructions.

---

## 🚀 Multiple Installation Options

Not on Windows? Want to customize? We've got you covered!

| Installation Method                                                                                                        | Best For                    | Platform | Setup Time |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------- | -------- | ---------- |
| **[Windows EXE](https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_DataDownloader.exe)** ⭐ Recommended | End users, Startup apps     | Windows  | 1 min      |
| **[Python Script](#option-2-install-from-source)**                                                                         | Developers, Mac/Linux users | All      | 5 min      |

---

## 🎯 Features

### Core Features

- **Dual-Source Downloads**: Simultaneously download from NIFTY 500 AND Market Indices pages!
- **Weekend-Aware Scheduling**: Automatically skips Saturday & Sunday (market closed days)
- **Separate Download Folders**: Each source saves to its own directory
  - `NSE_Data/NIFTY500/` for NIFTY 500 data
  - `NSE_Data/Market_Indices/` for Market Indices data
- **Hidden Browser Mode**: Browser runs completely in background - no visible window!
- **28-Stage Progress Bar**: Detailed real-time feedback from "Configuring" to "Complete!"
- **Multiple Schedule Times**: Set multiple download times throughout the day (e.g., `09:30, 12:00, 15:30`)
- **Scheduled Downloads**: Automatic daily downloads at your configured times (Monday-Friday only)
- **Manual Download**: Download data instantly any day with a single click
- **Custom Download Locations**: Choose separate paths for each data source

### Smart Features

- **Enhanced File Naming**: New format `{source}_ddmmyy-hhmmmin.csv`
  - Example: `NIFTY500_031025-1425min.csv` (Oct 3, 2025 at 2:25 PM)
  - Example: `MarketIndices_031025-1425min.csv`
- **Smart Download Detection**: Waits for download to complete (checks file size stability)
- **Multi-Location Search**: Automatically checks both configured and default Downloads folders
- **Duplicate Handling**: Auto-increments filename if downloading multiple times in same minute
- **Session Management**: Bypasses NSE security by establishing proper session for each source
- **Error Recovery**: Robust ChromeDriver handling with automatic fallback
- **CDP Download Control**: Dynamically sets download path for each source

### User Experience

- **Compact GUI (680×450px)**: Efficient use of screen space
- **Wide Path Fields**: View full file paths (48 characters)
- **Progress Percentage Display**: Shows `[37%] Button clicked! Initiating download...`
- **Comprehensive Logging**: All operations logged in `nse_downloader.log`
- **Background Operation**: Downloads run in headless mode (no visible browser)
- **Startup App Ready**: Perfect for Windows startup with weekend auto-skip
- **User-Friendly Interface**: Easy-to-use graphical interface with clear labels

## 📋 Requirements

### For Executable (Windows)

- Windows 10 or 11 (64-bit)
- Google Chrome browser installed
- Internet connection

### For Python Version

- Python 3.8 or higher
- Google Chrome browser installed
- Internet connection
- Windows/Linux/Mac OS

## 🚀 Installation

### Option 1: Download Executable (Recommended for Windows)

1. Download [NSE_DataDownloader.exe](releases/NSE_DataDownloader.exe)
2. Double-click to run
3. That's it! No installation needed.

### Option 2: Run from Source (All Platforms)

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Avisav24/NSE_Data_Downloader.git
   cd NSE_Data_Downloader
   ```

2. **Install Python Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **ChromeDriver** (automatic):
   The application will automatically use the appropriate ChromeDriver for your Chrome version.

## 💻 Usage

### Quick Start

1. **Run the Application**:

   ```bash
   python nse_downloader.py
   ```

2. **Configure Settings**:

   - **Download Locations**: Click "Browse" for each source to select save locations
     - NIFTY 500 folder (e.g., `C:\Users\YourName\Downloads\NSE_Data\NIFTY500`)
     - Market Indices folder (e.g., `C:\Users\YourName\Downloads\NSE_Data\Market_Indices`)
   - **Schedule Times**: Enter times in 24-hour format
     - Single time: `09:30`
     - Multiple times: `09:30, 12:00, 15:30`
     - Many times: `09:15, 10:00, 11:00, 12:00, 13:00, 14:00, 15:30`
     - **Note**: Scheduled downloads only run Monday-Friday (weekends auto-skipped)

3. **Start Scheduler**:

   - Click "Start Scheduler"
   - Keep window open for scheduled downloads
   - Downloads occur automatically at each configured time (Monday-Friday only)
   - If started on weekend, you'll see a notification that market is closed
   - Weekend downloads are automatically skipped

4. **Manual Download**:

   - Click "Download Now" for immediate download from BOTH sources
   - Works any day (including weekends)
   - Downloads NIFTY 500 and Market Indices simultaneously

5. **Stop Scheduler**:
   - Click "Stop Scheduler" to stop automatic downloads

### Multiple Schedule Times Examples

**Market Hours Coverage**:

```
09:30, 12:00, 15:30
```

- 9:30 AM: Market open
- 12:00 PM: Midday
- 3:30 PM: Market close

**Hourly Monitoring**:

```
09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00
```

**Single Daily Download**:

```
15:35
```

## 📁 File Naming Convention

### Format

```text
{SOURCE}_ddmmyy-hhmmmin.csv
```

### Components

- **{SOURCE}**: Data source identifier
  - `NIFTY500` for NIFTY 500 data
  - `MarketIndices` for Market Indices data
- **ddmmyy**: Date (e.g., 031025 for October 3, 2025)
- **hhmm**: Time in 24-hour format (e.g., 1425 for 2:25 PM)
- **min**: Suffix indicating minutes

### Examples

| Download Time | NIFTY 500 Filename              | Market Indices Filename              |
| ------------- | ------------------------------- | ------------------------------------ |
| 9:30 AM       | `NIFTY500_031025-0930min.csv`   | `MarketIndices_031025-0930min.csv`   |
| 10:15 AM      | `NIFTY500_031025-1015min.csv`   | `MarketIndices_031025-1015min.csv`   |
| 2:30 PM       | `NIFTY500_031025-1430min.csv`   | `MarketIndices_031025-1430min.csv`   |
| 11:45 PM      | `NIFTY500_031025-2345min.csv`   | `MarketIndices_031025-2345min.csv`   |

### Duplicate Handling

If downloading multiple times in the same minute:

- First: `NIFTY500_031025-1015min.csv`
- Second: `NIFTY500_031025-1015min_1.csv`
- Third: `NIFTY500_031025-1015min_2.csv`

## ⚙️ Configuration

Settings are automatically saved in `config.json`:

```json
{
  "download_paths": {
    "nifty500": "C:\\Users\\YourName\\Downloads\\NSE_Data\\NIFTY500",
    "market_indices": "C:\\Users\\YourName\\Downloads\\NSE_Data\\Market_Indices"
  },
  "scheduled_times": ["09:30", "12:00", "15:30"]
}
```

**Key Features**:
- Separate paths for each data source
- Multiple schedule times supported
- Scheduled downloads: Monday-Friday only
- Manual downloads: Any day

## 📊 How It Works

### Download Process (Dual-Source)

**For NIFTY 500**:
1. Configures download path for NIFTY 500 folder
2. Establishes session with NSE India homepage
3. Navigates to NIFTY 500 page
4. Waits for page to load (10 seconds)
5. Finds download button by ID `dwldcsv`
6. Clicks download button
7. Waits 3 seconds for download to initiate

**For Market Indices**:
8. Re-establishes session (8-second wait to avoid blocking)
9. Configures download path for Market Indices folder
10. Navigates to Market Indices page
11. Waits for page to load (10 seconds)
12. Finds download button by ID `dwldcsv`
13. Clicks download button
14. Waits 8 seconds for download to complete (slower download)

**File Processing**:
15. Verifies both files downloaded successfully
16. Checks file size stability (download complete)
17. Renames files with timestamp and source prefix
18. Logs success/failure for each source

### Weekend Detection

- Checks current day before scheduled downloads
- Saturday (day 5) and Sunday (day 6) are skipped
- Logs: "It's Saturday - Market is closed. Skipping."
- Manual downloads work any day

### Smart Renaming

- Monitors download folder for new CSV files
- Waits for file size to stabilize (2-second check)
- Ignores already-renamed files (starting with "NIFTY500\_")
- Auto-increments if duplicate exists

## 📝 Logging

All activities are logged in `nse_downloader.log`:

- Download start/completion times
- Button detection status
- File rename operations
- Errors and warnings

Example log:

```
2025-10-01 09:30:05 - INFO - Starting download at 2025-10-01 09:30:05
2025-10-01 09:30:10 - INFO - Establishing session with NSE...
2025-10-01 09:30:15 - INFO - Navigating to NIFTY 500 page...
2025-10-01 09:30:25 - INFO - Found download button using selector: By.ID = dwldcsv
2025-10-01 09:30:26 - INFO - Download button clicked successfully
2025-10-01 09:30:35 - INFO - File renamed to 'NIFTY500_20251001_0930min.csv'
```

## 🔧 Troubleshooting

### Download Button Not Found

- **Issue**: Website structure may have changed
- **Solution**: Check `nse_downloader.log` for details
- **Debug**: Screenshot saved in download folder

### ChromeDriver Not Compatible

- **Issue**: Chrome browser version mismatch
- **Solution**: Update Chrome to latest version
- **Alternative**: Reinstall dependencies

### Downloads Not Happening at Scheduled Time

- **Issue**: Scheduler not running
- **Solution**:
  - Keep application window open
  - Ensure computer is not in sleep mode
  - Check status panel for confirmation

### DEPRECATED_ENDPOINT Error

- **Issue**: NSE security detection
- **Solution**: Already handled by session establishment
- **Technical**: Script visits homepage first to get cookies

### File Not Renaming

- **Issue**: Download not completing or permissions
- **Solution**:
  - Verify download folder permissions
  - Check log for errors
  - Ensure file size > 0

## 🛡️ Technical Details

### Anti-Detection Features

- Chrome DevTools Protocol (CDP) commands
- Proper user agent headers
- Session cookie establishment
- Disabled automation flags
- JavaScript injection to hide webdriver

### Button Detection

Primary selector: `By.ID = "dwldcsv"`

Fallback selectors:

- `//span[@id='dwldcsv']`
- `//*[@id='dwldcsv']`
- `//span[@id='dwldcsv']/parent::*`
- Text-based selectors

## 📦 Project Structure

```
NSE_Data_Downloader/
├── nse_downloader.py          # Main application
├── requirements.txt           # Python dependencies
├── config.json               # User configuration (auto-created)
├── nse_downloader.log        # Activity logs (auto-created)
├── README.md                 # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect NSE India's terms of service and use responsibly. Do not use this tool for commercial purposes or excessive automated requests.

## 🙏 Acknowledgments

- NSE India for providing market data
- Selenium WebDriver for browser automation
- Schedule library for task scheduling

## 📧 Support

For issues or questions:

- Check `nse_downloader.log` for error details
- Review troubleshooting section above
- Open an issue on GitHub

---

**Repository**: https://github.com/Avisav24/NSE_Data_Downloader  
**Version**: 2.0  
**Last Updated**: October 1, 2025

For issues or questions, please check the `nse_downloader.log` file for error details.
