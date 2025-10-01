# NSE Data Downloader

A powerful desktop application to automatically download NIFTY 500 data from NSE India website at scheduled times with automatic file naming and smart download detection.

## 📥 Quick Download (No Python Needed!)

**For Windows users**: Download the ready-to-use executable!

👉 **[Download NSE_DataDownloader.exe](releases/NSE_DataDownloader.exe)** (~40 MB)

- No Python installation required
- No dependencies to install
- Just download and run!
- See [releases/README.md](releases/README.md) for details

## 🎯 Features

### Core Features

- **Multiple Schedule Times**: Set multiple download times throughout the day (e.g., `09:30, 12:00, 15:30`)
- **Scheduled Downloads**: Automatic daily downloads at your configured times
- **Manual Download**: Download data instantly with a single click
- **Custom Download Location**: Choose where to save your CSV files

### Smart Features

- **Automatic File Naming**: Files saved as `NIFTY500_YYYYMMDD_HHMMmin.csv` (e.g., `NIFTY500_20251001_1015min.csv`)
- **Smart Download Detection**: Waits for download to complete (checks file size stability)
- **Duplicate Handling**: Auto-increments filename if downloading multiple times in same minute
- **Session Management**: Bypasses NSE security by establishing proper session

### User Experience

- **User-Friendly GUI**: Easy-to-use graphical interface
- **Comprehensive Logging**: All operations logged in `nse_downloader.log`
- **Background Operation**: Downloads run in headless mode (no visible browser)
- **Backward Compatible**: Old configurations automatically updated

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

   - **Download Location**: Click "Browse" to select save location
   - **Schedule Times**: Enter times in 24-hour format
     - Single time: `09:30`
     - Multiple times: `09:30, 12:00, 15:30`
     - Many times: `09:15, 10:00, 11:00, 12:00, 13:00, 14:00, 15:30`

3. **Start Scheduler**:

   - Click "Start Scheduler"
   - Keep window open for scheduled downloads
   - Downloads occur automatically at each configured time

4. **Manual Download**:

   - Click "Download Now" for immediate download

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

```
NIFTY500_YYYYMMDD_HHMMmin.csv
```

### Components

- **NIFTY500**: Data source identifier
- **YYYYMMDD**: Date (e.g., 20251001 for October 1, 2025)
- **HHMM**: Time in 24-hour format (e.g., 1015 for 10:15 AM)
- **min**: Suffix indicating minutes

### Examples

| Download Time | Filename                        |
| ------------- | ------------------------------- |
| 9:30 AM       | `NIFTY500_20251001_0930min.csv` |
| 10:15 AM      | `NIFTY500_20251001_1015min.csv` |
| 2:30 PM       | `NIFTY500_20251001_1430min.csv` |
| 11:45 PM      | `NIFTY500_20251001_2345min.csv` |

### Duplicate Handling

If downloading multiple times in the same minute:

- First: `NIFTY500_20251001_1015min.csv`
- Second: `NIFTY500_20251001_1015min_1.csv`
- Third: `NIFTY500_20251001_1015min_2.csv`

## ⚙️ Configuration

Settings are automatically saved in `config.json`:

```json
{
  "download_path": "path/to/download/folder",
  "scheduled_times": ["09:30", "12:00", "15:30"]
}
```

**Backward Compatibility**: Old configs with single `scheduled_time` are automatically converted to the new format.

## 📊 How It Works

### Download Process

1. Establishes session with NSE India homepage
2. Navigates to NIFTY 500 page
3. Waits for page to load (10 seconds)
4. Finds download button by ID `dwldcsv`
5. Clicks download button
6. Waits for file to appear (up to 30 seconds)
7. Verifies file size stability (download complete)
8. Renames file with timestamp
9. Logs success/failure

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
