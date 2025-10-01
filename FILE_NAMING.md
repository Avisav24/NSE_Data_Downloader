# File Naming Convention

## Overview

All downloaded CSV files are automatically renamed with a timestamp to help you organize and identify when the data was downloaded.

## Naming Format

```
NIFTY500_YYYYMMDD_HHMMmin.csv
```

### Components:

- **NIFTY500**: Fixed prefix indicating the data source
- **YYYYMMDD**: Date in format Year-Month-Day
- **HHMM**: Time in 24-hour format (Hours-Minutes)
- **min**: Suffix to indicate "minutes"
- **.csv**: File extension

## Examples

| Download Time | Filename                        |
| ------------- | ------------------------------- |
| 9:30 AM       | `NIFTY500_20251001_0930min.csv` |
| 10:15 AM      | `NIFTY500_20251001_1015min.csv` |
| 2:30 PM       | `NIFTY500_20251001_1430min.csv` |
| 11:45 PM      | `NIFTY500_20251001_2345min.csv` |

## How It Works

1. **Download**: The script downloads the CSV file from NSE India website
2. **Wait**: Waits 10 seconds for the download to complete
3. **Find**: Locates the most recently downloaded CSV file in your download folder
4. **Rename**: Automatically renames it with the timestamp format
5. **Log**: Records the rename action in the log file

## Benefits

- ✅ **No Duplicate Confusion**: Each file has a unique name based on download time
- ✅ **Easy Sorting**: Files are automatically sorted by date and time
- ✅ **Quick Identification**: Know exactly when the data was downloaded
- ✅ **Organized Archive**: Build a historical archive of market data

## Location

Files are saved in your configured download folder (default: `Downloads/NSE_Data`)

## Troubleshooting

If file renaming fails:

- The original file will remain with its default name
- Check `nse_downloader.log` for error details
- Ensure you have write permissions in the download folder
