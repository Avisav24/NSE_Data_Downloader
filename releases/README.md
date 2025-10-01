# NSE Data Downloader - Windows Executable

## Download

**Latest Version**: v2.0  
**File**: `NSE_DataDownloader.exe`  
**Size**: ~40 MB  
**Platform**: Windows 10/11 (64-bit)

## Quick Start

1. **Download** the `NSE_DataDownloader.exe` file
2. **Double-click** to run (no installation needed!)
3. **Configure** your download times and location
4. **Start** the scheduler or download manually

## No Python Required!

This is a standalone executable. You don't need Python or any dependencies installed.

## Requirements

- Windows 10 or 11 (64-bit)
- Google Chrome browser installed
- Internet connection

## First-Time Setup

1. Download `NSE_DataDownloader.exe`
2. Right-click → Properties → Check "Unblock" if present
3. Double-click to run

### Windows Defender Warning

If Windows Defender shows a warning:

1. Click "More info"
2. Click "Run anyway"

This is normal for unsigned executables. The software is safe.

## What It Does

- Downloads NIFTY 500 data from NSE India
- Automatic downloads at scheduled times
- Files saved with timestamps: `NIFTY500_20251001_1015min.csv`
- Multiple schedule times support
- Smart download detection and file renaming

## Files Created

On first run, the app creates:

- `config.json` - Your settings
- `nse_downloader.log` - Activity log
- `NSE_Data/` - Default download folder (customizable)

## Usage

1. **Set Download Location**: Click "Browse" to choose folder
2. **Set Times**: Enter one or more times (e.g., `09:30, 12:00, 15:30`)
3. **Start Scheduler**: Click "Start Scheduler" for automatic downloads
4. **Manual Download**: Click "Download Now" for immediate download

## Features

✅ Multiple daily download times  
✅ Automatic timestamp naming  
✅ Smart download completion detection  
✅ Duplicate file handling  
✅ Background operation  
✅ Comprehensive logging

## Troubleshooting

**Antivirus blocks the file**:

- Add exception for `NSE_DataDownloader.exe`
- The file is safe, just unsigned

**Chrome not found**:

- Install Google Chrome browser
- Make sure it's the latest version

**Downloads not working**:

- Check internet connection
- Verify Chrome is installed
- Check log file for details

## Support

- Check `nse_downloader.log` for error details
- GitHub Issues: https://github.com/Avisav24/NSE_Data_Downloader/issues
- Full Documentation: See main README.md

---

**Build Date**: October 1, 2025  
**Python Version**: 3.13  
**Dependencies**: Bundled (Selenium, Schedule, Requests)
