# Building Executable for NSE Data Downloader

This guide explains how to build the Windows executable (.exe) file.

## Prerequisites

1. Python 3.8+ installed
2. All dependencies installed: `pip install -r requirements.txt`
3. PyInstaller installed: `pip install pyinstaller`

## Building the Executable

### Method 1: Using the Spec File (Recommended)

```powershell
pyinstaller nse_downloader.spec
```

### Method 2: Command Line

```powershell
pyinstaller --onefile --windowed --name "NSE_DataDownloader" --hidden-import selenium --hidden-import schedule --hidden-import requests nse_downloader.py
```

## Output Location

After successful build:
- Executable file: `dist/NSE_DataDownloader.exe`
- Build files: `build/` folder (can be deleted)
- Spec file: `nse_downloader.spec` (configuration)

## File Size

The executable will be approximately 30-50 MB due to bundled dependencies.

## Testing the Executable

1. Navigate to `dist/` folder
2. Double-click `NSE_DataDownloader.exe`
3. The GUI should open without needing Python installed

## Distribution

To distribute to others:
1. Copy `NSE_DataDownloader.exe` from `dist/` folder
2. Users need:
   - Google Chrome browser installed
   - Internet connection
   - No Python required!

## Important Notes

### Chrome/ChromeDriver
- Users must have Google Chrome installed
- ChromeDriver is handled automatically by Selenium

### First Run
- Windows Defender might show a warning (normal for unsigned executables)
- Click "More info" → "Run anyway"

### Files Created
The executable will create in the same folder:
- `config.json` - User settings
- `nse_downloader.log` - Activity logs
- `NSE_Data/` - Default download folder

## Troubleshooting Build Issues

### Missing Module Error
```powershell
# Add the module to hidden imports in spec file
hiddenimports=['selenium', 'schedule', 'requests', 'your_missing_module']
```

### Large File Size
This is normal. The executable bundles:
- Python interpreter
- All dependencies (Selenium, Schedule, etc.)
- Required libraries

### Antivirus False Positive
- Unsigned executables may trigger warnings
- This is normal and safe
- Consider code signing for professional distribution

## Clean Build

To rebuild from scratch:
```powershell
# Remove old build files
Remove-Item -Recurse -Force build, dist
# Rebuild
pyinstaller nse_downloader.spec
```

## GitHub Release

After building:
1. Create a new release on GitHub
2. Upload `NSE_DataDownloader.exe` as a release asset
3. Users can download directly from GitHub Releases page

---

**Build Date**: October 1, 2025  
**Platform**: Windows x64  
**Python Version**: 3.13
