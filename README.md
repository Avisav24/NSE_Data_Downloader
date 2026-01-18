<div align="center">

# 📈 NSE Data Downloader

### _Automated NIFTY 500, FnO, & Market Indices Data Downloader_

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/Avisav24/NSE_Data_Downloader)
[![Downloads](https://img.shields.io/github/downloads/Avisav24/NSE_Data_Downloader/total.svg)](https://github.com/Avisav24/NSE_Data_Downloader/releases)

A powerful desktop application to automatically download **NIFTY 500**, **Market Indices**, and **14+ Critical NSE Reports** including **Bhavcopies, FnO Stats, and Bulk/Block Deals**. Features scheduled automation, smart file management, and **weekend-aware scheduling**.

---

## 📥 Quick Download (No Python Needed!)

### 🎯 **Ready-to-Use Windows Executable**

**Latest Version: v3.5** | **Size: ~24 MB** | **Platform: Windows 10/11**

<p>
  <a href="https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/nse_downloader.exe">
    <img src="https://img.shields.io/badge/⬇️%20Download-nse__downloader.exe-success?style=for-the-badge&logo=windows&logoColor=white" alt="Download EXE" height="50"/>
  </a>
</p>

**Direct Download URL:**

```text
https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/nse_downloader.exe
```

_Or browse the [releases folder](releases/) for all versions_

---

</div>

---

## ✨ What's New

<div align="center">

### v3.5 Highlights

- **Short Sell Download Fix**: Resolved a casing issue (`Short_sell` vs `Short_Sell`) that caused failures in some environments.
- **Config Migration**: Added automatic migration logic for older configuration files.
- **Improved Executable**: Rebuilt with the latest dependencies and fixes.
- Rebuilt Windows EXE (v3.5)

<table>
<tr>
<td width="50%" align="center">

### 📊 **Expanded Data Suite**

**NEW!** Now supports 14+ new reports!

✅ **FnO:** OI Spurts, Participant Vol/OI, FII Stats  
✅ **Equities:** Bulk/Block Deals, 52 Wk High/Low  
✅ **Archives:** Daily Bhavcopies (CM & FO)

</td>
<td width="50%" align="center">

### 🤖 **Enhanced Auto Mode**

**UPDATED!** Set it and forget it!

✅ **Multiple Schedule Times** (comma-separated)
✅ Auto-start scheduler (8 AM - 8 PM)  
✅ Handles multiple download sources  
✅ State persists across restarts  
✅ Perfect for Windows startup

</td>
</tr>
</table>

</div>

### 🎯 Core Features

<table>
<tr>
<td width="50%">

**📈 Comprehensive Data Downloads**

- **Derivatives:** Combined OI, Participant OI/Vol, FII Stats
- **Capital Market:** NIFTY 500, PE Details, Bulk/Block Deals
- **Bhavcopies:** Full CM & FO Bhavcopies (ZIP/CSV)

**🗓️ Weekend Detection**

- Auto-skips Saturday & Sunday
- Market-aware scheduling
- Manual override available

**🏷️ Enhanced File Naming**

- Format: `{ReportName}_ddmmyy-hhmmmin.csv`
- Duplicate auto-increment protection

</td>
<td width="50%">

- Redesigned interface for multiple sources
- Wide path fields
- Professional design

**⚡ Smart Features**

- **Hidden browser mode** (Headless)
- ChromeDriver auto-update
- Session management for Archives
- Error recovery

</td>
</tr>
</table>

---

## 📋 Supported Data Reports

The application now fetches the following reports automatically:

| Category              | Report Type                                                                                                                    |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Derivatives (FnO)** | • OI Spurts (By Underlying)<br>• Combined OI (Archive)<br>• Participant Volume & OI<br>• FII Statistics<br>• FO Bhavcopy (ZIP) |
| **Capital Market**    | • NIFTY 500 Data<br>• Bulk Deals & Block Deals<br>• 52 Week High/Low<br>• Security Bhavdata (Full)<br>• CM Bhavcopy (ZIP)      |
| **Indices/Others**    | • Indices Close All<br>• PE Details                                                                                            |

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

| Feature                         | Description                                              |
| ------------------------------- | -------------------------------------------------------- |
| 📥 **Multi-Source Downloads**   | Download from 14+ NSE endpoints simultaneously           |
| 📅 **Weekend-Aware Scheduling** | Auto-skips Saturday & Sunday (market closed)             |
| 📂 **Smart Organization**       | Files are sorted into relevant folders automatically     |
| 🔇 **Hidden Browser Mode**      | Completely background operation - no visible window      |
| 📊 **Real-time Progress**       | Feedback on which report is currently downloading        |
| ⏰ **Multiple Schedule Times**  | Set unlimited times (e.g., `09:30, 15:30`)               |
| 🎯 **Manual Download**          | Instant downloads with a single click (works any day)    |
| 🤖 **Auto Mode**                | Auto-start scheduler during business hours (8 AM - 8 PM) |
| Feature                         | Description                                              |
| ---------                       | -------------                                            |
| 📥 **Multi-Source Downloads**   | Download from 14+ NSE endpoints simultaneously           |
| 📅 **Weekend-Aware Scheduling** | Auto-skips Saturday & Sunday (market closed)             |
| 📂 **Smart Organization**       | Files are sorted into relevant folders automatically     |
| 🔇 **Hidden Browser Mode**      | Completely background operation - no visible window      |
| 📊 **Real-time Progress**       | Feedback on which report is currently downloading        |
| ⏰ **Multiple Schedule Times**  | Set unlimited times (e.g., `09:30, 15:30`)               |
| 🎯 **Manual Download**          | Instant downloads with a single click (works any day)    |
| 🤖 **Auto Mode**                | Auto-start scheduler during business hours (8 AM - 8 PM) |

<div align="center">

### 🧠 Smart Features

</div>

```
File Naming Format: {ReportType}_ddmmyy-hhmmmin.ext

Examples:
✓ OI_Spurts_101025-1425min.csv
✓ FII_Stats_101025-1530min.xls
✓ BhavCopy_CM_101025-1600min.zip
```

- ✅ **Smart Download Detection** - Waits for completion (file size stability check)
- ✅ **Archive Handling** - Automatically handles ZIP and CSV formats
- ✅ **Duplicate Handling** - Auto-increments filename (`_1`, `_2`, etc.)
- ✅ **Session Management** - Bypasses NSE security for archives and API
- ✅ **Error Recovery** - Robust ChromeDriver handling with auto-fallback

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

> > > > > > > a512c1f (Update downloader GUI, fix OI Spurts csv, rebuild exe)

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

## 💻 Usage

### Quick Start

1. **Run the Application**:

   ```bash
   python nse_downloader.py
   ```

2. **Configure Settings**:

   - **Download Locations**: Click "Browse" to select save locations.
   - **Auto Mode**: Check "Auto Mode" to enable automatic scheduler activation on startup.
   - **Schedule Times**: Enter times in 24-hour format (e.g., `15:35, 17:00`).
   - **Note**: Scheduled downloads only run Monday-Friday.

3. **Start Scheduler**:

   - Click "Start Scheduler"
   - Downloads occur automatically at configured times.

4. **Manual Download**:
   - Click "Download Now" for immediate download of **ALL** configured reports.

## ⚙️ Configuration

Settings are automatically saved in `config.json`. The downloader now manages multiple endpoints dynamically.

## 📊 How It Works

### Download Process (Multi-Source)

1. **Session Initialization**: Establishes a valid session with NSE India homepage to get cookies.
2. **Sequential Downloading**: Iterates through the list of 14+ configured URLs (Spurts, PE, Vol, Bhavcopies, etc.).
3. **Smart Navigation**: Uses specific API endpoints or Archive URLs based on the report type.
4. **File Processing**:
   - Verifies download completion.
   - Renames files with timestamp and source prefix.
   - Moves files to their specific folders (e.g., `NSE_Data/FnO`, `NSE_Data/Bhavcopy`).

### Weekend Detection

- Checks current day before scheduled downloads.
- Logs: "It's Saturday - Market is closed. Skipping."

## 📝 Logging

All activities are logged in `nse_downloader.log`:

- Download start/completion times for each report type.
- File rename operations.
- Errors (e.g., if a specific report is not yet generated by NSE for the day).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect NSE India's terms of service and use responsibly. Do not use this tool for commercial purposes or excessive automated requests.

---

**Repository**: https://github.com/Avisav24/NSE_Data_Downloader  
**Last Updated**: December 11, 2025
