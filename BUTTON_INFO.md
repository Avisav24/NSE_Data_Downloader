# NSE Download Button Reference

## Button Details

**Element Type:** `<span>`  
**ID:** `dwldcsv`  
**Text:** "Download (.csv)"

## XPath Selectors (in priority order)

1. **By ID (Most Reliable):**

   ```python
   By.ID, "dwldcsv"
   ```

2. **By XPath with ID:**

   ```xpath
   //span[@id='dwldcsv']
   //*[@id='dwldcsv']
   ```

3. **Parent Element (if span is inside a clickable element):**
   ```xpath
   //span[@id='dwldcsv']/parent::*
   ```

## Implementation

The script now uses these selectors in order:

1. Direct ID lookup (fastest and most reliable)
2. XPath with exact ID match
3. Parent element click (in case span is inside an anchor or button)
4. Fallback text-based selectors

## Usage

The `nse_downloader.py` script will automatically:

- Try the exact button ID first
- Log which selector successfully found the button
- Fall back to alternative selectors if needed
- Save debug screenshots if button cannot be found

## Testing

Run the application and click "Download Now" to test:

```powershell
python nse_downloader.py
```

Check `nse_downloader.log` for details on which selector was used.
