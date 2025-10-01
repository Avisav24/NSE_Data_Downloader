# Multiple Schedule Times Feature

## Overview

You can now schedule downloads at **multiple times** throughout the day! This allows you to capture NIFTY 500 data at different market hours automatically.

## How to Use

### Setting Multiple Times

In the "Schedule Times" section of the GUI:

1. Enter times separated by commas
2. Use 24-hour format (HH:MM)
3. Click "Start Scheduler"

### Example Inputs

```
09:30, 12:00, 15:30
```

This will download data at:

- 9:30 AM (market open)
- 12:00 PM (midday)
- 3:30 PM (market close)

### More Examples

**Hourly during market hours:**

```
09:30, 10:30, 11:30, 12:30, 13:30, 14:30, 15:30
```

**Key market moments:**

```
09:15, 15:30
```

**Single time (still works):**

```
09:30
```

## Features

### ✅ Automatic Validation

- Checks each time for correct format
- Shows which time is invalid if error occurs
- Prevents starting with incorrect times

### ✅ Smart Scheduling

- Each time gets its own scheduled job
- Downloads happen independently
- No conflicts between times

### ✅ Unique Filenames

Each download gets a unique name based on actual download time:

- 9:30 AM → `NIFTY500_20251001_0930min.csv`
- 12:00 PM → `NIFTY500_20251001_1200min.csv`
- 3:30 PM → `NIFTY500_20251001_1530min.csv`

### ✅ Configuration Saved

Your scheduled times are automatically saved and restored when you restart the application.

## GUI Changes

### Old Interface:

```
Download Time (HH:MM): [09:30] (24-hour format)
```

### New Interface:

```
Download Times:
[09:30, 12:00, 15:30] (HH:MM, 24-hour format, separate multiple times with commas)
Example: 09:30, 12:00, 15:30
```

## Status Messages

When you start the scheduler, you'll see:

```
[2025-10-01 08:00:00] Scheduler started. Downloads scheduled for: 09:30, 12:00, 15:30
```

Each scheduled time is logged separately:

```
Download scheduled for 09:30 daily
Download scheduled for 12:00 daily
Download scheduled for 15:30 daily
```

## Benefits

### 📊 Capture Market Trends

- Opening prices (09:15)
- Mid-day movements (12:00)
- Closing prices (15:30)

### 🔄 Multiple Data Points

- Compare data across different times
- Track intraday changes
- Build comprehensive datasets

### ⏰ Set and Forget

- Configure once
- Runs automatically every day
- All files organized with timestamps

## Technical Details

### Configuration File (config.json)

**Old format:**

```json
{
  "download_path": "path/to/folder",
  "scheduled_time": "09:30"
}
```

**New format:**

```json
{
  "download_path": "path/to/folder",
  "scheduled_times": ["09:30", "12:00", "15:30"]
}
```

### Backward Compatibility

- Old configs with single `scheduled_time` are automatically converted
- No manual migration needed
- Existing setups continue to work

## Usage Tips

### Best Practices

1. **Market Hours**: NSE is open 9:15 AM to 3:30 PM
2. **Avoid Too Frequent**: Don't schedule every minute (website limits)
3. **Key Times**: Focus on market open, midday, and close
4. **Test First**: Try manual download before scheduling

### Recommended Schedules

**Conservative (3 downloads/day):**

```
09:30, 12:00, 15:30
```

**Active Trader (6 downloads/day):**

```
09:30, 10:30, 11:30, 12:30, 14:00, 15:30
```

**Quick Check (1 download/day):**

```
15:35
```

## Troubleshooting

### Invalid Time Format

- ❌ Wrong: `9:30` (missing leading zero)
- ✅ Correct: `09:30`
- ❌ Wrong: `09:30,12:00` (no space after comma is fine, but ensure commas separate)
- ✅ Correct: `09:30, 12:00` or `09:30,12:00`

### Scheduler Not Running

- Ensure the application window stays open
- Check status panel for confirmation
- Verify times are in 24-hour format

### Downloads Not Happening

- Check `nse_downloader.log` for details
- Verify computer is not in sleep mode
- Ensure internet connection is active

## Example Workflow

1. **Set Multiple Times**: `09:30, 12:00, 15:30`
2. **Click Start Scheduler**
3. **See Confirmation**: "Downloads scheduled for: 09:30, 12:00, 15:30"
4. **Keep Window Open**
5. **Files Appear Automatically**:
   - `NIFTY500_20251001_0930min.csv`
   - `NIFTY500_20251001_1200min.csv`
   - `NIFTY500_20251001_1530min.csv`

---

**Version:** 2.0  
**Feature:** Multiple Schedule Times  
**Date:** October 1, 2025
