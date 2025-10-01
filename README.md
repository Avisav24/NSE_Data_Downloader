# NSE Data Downloader

A desktop application to automatically download NIFTY 500 data from NSE India website at scheduled times.

## Features

- **Scheduled Downloads**: Set a specific time for daily automatic downloads
- **Manual Download**: Download data instantly with a single click
- **Custom Download Location**: Choose where to save your CSV files
- **Automatic File Naming**: Files are saved with timestamp (e.g., NIFTY500_20251001_1015min.csv for 10:15 AM)
- **User-Friendly GUI**: Easy-to-use graphical interface
- **Logging**: All operations are logged for tracking
- **Background Operation**: Downloads run in the background without browser windows

## Requirements

- Python 3.8 or higher
- Google Chrome browser installed on your system
- Internet connection

## Installation

1. **Install Python Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Install ChromeDriver** (automatic):
   The application will automatically download the appropriate ChromeDriver for your Chrome version.

## Usage

1. **Run the Application**:

   ```bash
   python nse_downloader.py
   ```

2. **Configure Settings**:

   - **Download Location**: Click "Browse" to select where CSV files will be saved
   - **Schedule Time**: Enter the time in 24-hour format (e.g., 09:30 for 9:30 AM)

3. **Start Scheduled Downloads**:

   - Click "Start Scheduler" to activate daily automatic downloads
   - Keep the application window open for scheduled downloads to work

4. **Manual Download**:

   - Click "Download Now" to download the CSV file immediately

5. **Stop Scheduler**:
   - Click "Stop Scheduler" to stop automatic downloads

## Configuration

Settings are automatically saved in `config.json` and will be restored when you restart the application.

## File Naming Convention

Downloaded files are automatically renamed with the following format:

- **Format**: `NIFTY500_YYYYMMDD_HHMMmin.csv`
- **Example**: `NIFTY500_20251001_1015min.csv` (for download at 10:15 AM on October 1, 2025)
- **Example**: `NIFTY500_20251001_1430min.csv` (for download at 2:30 PM on October 1, 2025)

## Logs

All download activities and errors are logged in `nse_downloader.log` file.

## Notes

- The application must remain running for scheduled downloads to work
- Make sure Google Chrome is installed on your system
- The download runs in headless mode (no visible browser window)
- Downloaded files are saved with timestamps in the specified directory

## Troubleshooting

**Issue**: Download button not found

- **Solution**: The website structure may have changed. Check the logs for details.

**Issue**: ChromeDriver not compatible

- **Solution**: Update Chrome browser to the latest version and reinstall the application dependencies.

**Issue**: Downloads not happening at scheduled time

- **Solution**: Make sure the application window is kept open and your computer is not in sleep mode.

## Support

For issues or questions, please check the `nse_downloader.log` file for error details.
