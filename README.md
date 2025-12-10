<div align="center">

# 📈 NSE Data Downloader

### *Automated NIFTY 500 & Market Indices Data Downloader*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/Avisav24/NSE_Data_Downloader)
[![Downloads](https://img.shields.io/github/downloads/Avisav24/NSE_Data_Downloader/total.svg)](https://github.com/Avisav24/NSE_Data_Downloader/releases)

A powerful desktop application to automatically download **NIFTY 500** and **Market Indices** data from NSE India with scheduled automation, smart file management, and **weekend-aware scheduling**.

---

## 📥 Quick Download (No Python Needed!)

### 🎯 **Ready-to-Use Windows Executable**

**Latest Version: v3.1** | **Size: ~82 MB** | **Platform: Windows 10/11**

<p>
  <a href="https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_Data_Downloader.exe">
    <img src="https://img.shields.io/badge/⬇️%20Download-NSE__Data_Downloader.exe-success?style=for-the-badge&logo=windows&logoColor=white" alt="Download EXE" height="50"/>
  </a>
</p>

**Direct Download URL:**
```text
https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_Data_Downloader.exe
```

*Or browse the [releases folder](releases/) for all versions*

---

</div>

---

</div>

## ✨ What's New in v3.1

<div align="center">

<table>
<tr>
<td width="50%" align="center">

### 🤖 **Auto Mode**
**NEW!** Set it and forget it!

✅ Auto-start scheduler (8 AM - 8 PM)  
✅ No manual button clicks needed  
✅ State persists across restarts  
✅ Perfect for Windows startup  

</td>
<td width="50%" align="center">

### 🔄 **Progress Reset**
**NEW!** Clean interface!

✅ Auto-resets after download  
✅ 3-second completion display  
✅ Shows "Ready" status  
✅ Professional UX  

</td>
</tr>
</table>

</div>

### 🎯 Core Features (v3.1)

<table>
<tr>
<td width="50%">

**📊 Dual-Source Downloads**
- NIFTY 500 + Market Indices simultaneously
- Separate folders for each source
- CDP download path control

**🗓️ Weekend Detection**
- Auto-skips Saturday & Sunday
- Market-aware scheduling
- Manual override available

**🏷️ Enhanced File Naming**
- Format: `NIFTY500_ddmmyy-hhmmmin.csv`
- Example: `NIFTY500_031025-1425min.csv`
- Duplicate auto-increment

</td>
<td width="50%">

**🎨 Compact GUI**
- 650×485px redesigned interface
- Wide path fields (48 chars)
- Professional design

**📈 28 Progress Stages**
- Real-time feedback
- Percentage display
- Detailed status messages

**⚡ Smart Features**
- Hidden browser mode
- ChromeDriver auto-update
- Session management
- Error recovery

</td>
</tr>
</table>

### ✨ Why Use the Executable?

<div align="center">

| Feature | Benefit |
|:-------:|:-------:|
| ✅ **No Python Installation** | Just download & run |
| ✅ **No Dependencies** | Everything included |
| ✅ **Auto Mode** | Hands-free operation |
| ✅ **Weekend-Aware** | Smart scheduling (Mon-Fri) |
| ✅ **Dual Downloads** | Two sources simultaneously |
| ✅ **Background Mode** | Hidden browser |
| ✅ **Startup Ready** | Perfect for automation |

**Perfect for traders, analysts, and data enthusiasts!** 📊

</div>

---

## 🚀 Installation Options

<div align="center">

<table>
<tr>
<th>Method</th>
<th>Best For</th>
<th>Platform</th>
<th>Setup Time</th>
</tr>
<tr>
<td><b><a href="https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_Data_Downloader.exe">Windows EXE</a></b> ⭐</td>
<td>End users, Startup apps</td>
<td>Windows 10/11</td>
<td>1 min</td>
</tr>
<tr>
<td><b><a href="#-python-installation">Python Script</a></b></td>
<td>Developers, Mac/Linux</td>
<td>All platforms</td>
<td>5 min</td>
</tr>
</table>

</div>

---

## 🎯 All Features

<div align="center">

### 📦 Core Capabilities

</div>

| Feature | Description |
|---------|-------------|
| 📥 **Dual-Source Downloads** | Download from NIFTY 500 AND Market Indices simultaneously |
| 📅 **Weekend-Aware Scheduling** | Auto-skips Saturday & Sunday (market closed) |
| 📂 **Separate Folders** | `NSE_Data/NIFTY500/` & `NSE_Data/Market_Indices/` |
| 🔇 **Hidden Browser Mode** | Completely background operation - no visible window |
| 📊 **28-Stage Progress** | Real-time feedback from "Configuring" to "Complete!" |
| ⏰ **Multiple Schedule Times** | Set unlimited times (e.g., `09:30, 12:00, 15:30`) |
| 🎯 **Manual Download** | Instant downloads with a single click (works any day) |
| 📁 **Custom Locations** | Choose separate paths for each data source |
| 🤖 **Auto Mode (v3.1)** | Auto-start scheduler during business hours (8 AM - 8 PM) |

<div align="center">

### 🧠 Smart Features

</div>

```
File Naming Format: {source}_ddmmyy-hhmmmin.csv

Examples:
✓ NIFTY500_101025-1425min.csv       (Oct 10, 2025 at 2:25 PM)
✓ MarketIndices_101025-0930min.csv  (Oct 10, 2025 at 9:30 AM)
```

- ✅ **Smart Download Detection** - Waits for completion (file size stability check)
- ✅ **Multi-Location Search** - Checks configured AND default Downloads folder
- ✅ **Duplicate Handling** - Auto-increments filename (`_1`, `_2`, etc.)
- ✅ **Session Management** - Bypasses NSE security for each source
- ✅ **Error Recovery** - Robust ChromeDriver handling with auto-fallback
- ✅ **CDP Download Control** - Dynamic path setting per source
- ✅ **Progress Bar Reset (v3.1)** - Auto-resets after download completes

---

## 💻 Python Installation

<div align="center">

**For developers and advanced users who want to customize the code**

</div>

### 📋 Requirements
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

1. Download [NSE_Data_Downloader.exe](releases/NSE_Data_Downloader.exe)
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
   - **Auto Mode** (NEW in v3.1):
     - Check "Auto Mode (8 AM - 8 PM, auto-start scheduler)" to enable automatic scheduler activation
     - When enabled, scheduler starts automatically when you open the app (if time is between 8 AM - 8 PM)
     - State is saved - your preference persists across app restarts
     - Perfect for adding to Windows startup - app will auto-start scheduler during business hours!
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

| Download Time | NIFTY 500 Filename            | Market Indices Filename            |
| ------------- | ----------------------------- | ---------------------------------- |
| 9:30 AM       | `NIFTY500_031025-0930min.csv` | `MarketIndices_031025-0930min.csv` |
| 10:15 AM      | `NIFTY500_031025-1015min.csv` | `MarketIndices_031025-1015min.csv` |
| 2:30 PM       | `NIFTY500_031025-1430min.csv` | `MarketIndices_031025-1430min.csv` |
| 11:45 PM      | `NIFTY500_031025-2345min.csv` | `MarketIndices_031025-2345min.csv` |

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

**For Market Indices**: 8. Re-establishes session (8-second wait to avoid blocking) 9. Configures download path for Market Indices folder 10. Navigates to Market Indices page 11. Waits for page to load (10 seconds) 12. Finds download button by ID `dwldcsv` 13. Clicks download button 14. Waits 8 seconds for download to complete (slower download)

**File Processing**: 15. Verifies both files downloaded successfully 16. Checks file size stability (download complete) 17. Renames files with timestamp and source prefix 18. Logs success/failure for each source

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
