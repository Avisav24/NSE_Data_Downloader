# Installation Guide - NSE Data Downloader

There are **4 different ways** to use NSE Data Downloader. Choose the method that works best for you!

---

## 🎯 Method 1: Windows Executable (Recommended - Easiest)

**Best for**: Non-technical users, quick setup

### Download & Run

1. **Download the executable**:
   - [Direct Download Link](https://github.com/Avisav24/NSE_Data_Downloader/raw/main/releases/NSE_DataDownloader.exe)
   
2. **Double-click to run**: `NSE_DataDownloader.exe`

3. **First-time setup**: Windows may show a security warning
   - Click "More info" → "Run anyway"
   - This is normal for unsigned executables

### Requirements
- ✅ Windows 10/11 (64-bit)
- ✅ Google Chrome installed
- ❌ NO Python needed
- ❌ NO installation needed

### Pros & Cons
✅ **Pros**: Easiest, no setup, just download and run  
❌ **Cons**: Larger file size (~40 MB), Windows only

---

## 🐍 Method 2: Python Script (Recommended for Developers)

**Best for**: Python developers, cross-platform users, those who want to modify code

### Installation Steps

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Version 3.8 or higher required
   - During installation, check "Add Python to PATH"

2. **Download the repository**:
   ```bash
   git clone https://github.com/Avisav24/NSE_Data_Downloader.git
   cd NSE_Data_Downloader
   ```
   
   **OR** download ZIP:
   - Go to: https://github.com/Avisav24/NSE_Data_Downloader
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python nse_downloader.py
   ```

### Requirements
- Python 3.8+
- Google Chrome browser
- Dependencies: selenium, schedule, webdriver-manager, requests

### Pros & Cons
✅ **Pros**: Cross-platform (Windows/Mac/Linux), smaller download, can modify code  
✅ **Pros**: Always get latest features, can customize  
❌ **Cons**: Requires Python installation, more setup steps

---

## 📦 Method 3: Pip Install (Coming Soon!)

**Best for**: Installing as a system-wide tool

### Future Installation (Not Yet Available)

```bash
pip install nse-data-downloader
```

Then run from anywhere:
```bash
nse-downloader
```

**Status**: 🚧 Not yet published to PyPI  
**ETA**: Future release

---

## 🐳 Method 4: Docker Container (For Advanced Users)

**Best for**: Containerized environments, servers, scheduled automation

### Create Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY nse_downloader.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory
RUN mkdir -p /app/data

# Run the application
CMD ["python", "nse_downloader.py"]
```

### Build and Run

```bash
# Build the Docker image
docker build -t nse-downloader .

# Run the container
docker run -it -v $(pwd)/downloads:/app/data nse-downloader
```

### Pros & Cons
✅ **Pros**: Isolated environment, runs on any OS with Docker, server-friendly  
✅ **Pros**: Easy to deploy on cloud servers  
❌ **Cons**: Requires Docker knowledge, more complex setup

---

## 🌐 Method 5: Online/Cloud Solutions

### Option A: GitHub Codespaces

1. Go to: https://github.com/Avisav24/NSE_Data_Downloader
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment to load
4. Run in terminal:
   ```bash
   pip install -r requirements.txt
   python nse_downloader.py
   ```

**Pros**: No local installation, runs in browser  
**Cons**: Requires GitHub account, may have usage limits

### Option B: Repl.it / Google Colab

1. Upload `nse_downloader.py` and `requirements.txt`
2. Install dependencies
3. Run the script

**Pros**: Free, cloud-based  
**Cons**: May require modifications for GUI

---

## 🔧 Method 6: Build Your Own Executable

**Best for**: Creating customized versions

### Windows Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller nse_downloader.spec

# Find executable in dist/ folder
```

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed steps.

### macOS Application

```bash
# Build for macOS
pyinstaller --onefile --windowed --name "NSE_DataDownloader" nse_downloader.py
```

### Linux Executable

```bash
# Build for Linux
pyinstaller --onefile --name "nse_downloader" nse_downloader.py
```

---

## 📊 Comparison Table

| Method | Ease of Use | Setup Time | Platform | Size | Best For |
|--------|-------------|------------|----------|------|----------|
| **Windows EXE** | ⭐⭐⭐⭐⭐ | 1 min | Windows | 40 MB | End users |
| **Python Script** | ⭐⭐⭐⭐ | 5-10 min | All | <1 MB | Developers |
| **Docker** | ⭐⭐⭐ | 10-15 min | All | ~500 MB | Servers |
| **Codespaces** | ⭐⭐⭐⭐ | 2-3 min | Browser | N/A | Testing |
| **Build Own** | ⭐⭐ | 15-20 min | All | Varies | Customization |

---

## 🎯 Quick Decision Guide

**Choose Windows EXE if**:
- You just want it to work
- You're on Windows
- You don't have Python installed

**Choose Python Script if**:
- You're comfortable with command line
- You want to modify the code
- You're on Mac/Linux
- You want the latest updates

**Choose Docker if**:
- You're running on a server
- You need isolation
- You're automating in production

**Choose Build Your Own if**:
- You want to customize
- You need a different platform
- You want to learn the build process

---

## ❓ Common Questions

### Q: Which method is fastest to get started?
**A**: Windows EXE - just download and run!

### Q: Which method is best for learning?
**A**: Python Script - you can see and modify the code

### Q: Can I use this on Mac or Linux?
**A**: Yes! Use Python Script or Docker method

### Q: Which method gets updates first?
**A**: Python Script (just `git pull` to update)

### Q: Can I run this on a server without a GUI?
**A**: Yes! The app runs in headless mode (no visible browser)

### Q: Do I need to keep the terminal open?
**A**: Only for Python Script method. EXE runs as a standalone app.

---

## 🆘 Need Help?

- **Issues**: Report at https://github.com/Avisav24/NSE_Data_Downloader/issues
- **Documentation**: See [README.md](README.md)
- **Logs**: Check `nse_downloader.log` for troubleshooting

---

## 📝 Installation Troubleshooting

### Windows EXE Issues

**Problem**: "Windows protected your PC" warning  
**Solution**: Click "More info" → "Run anyway"

**Problem**: Antivirus blocking the file  
**Solution**: Add exception for the file or use Python Script method

### Python Script Issues

**Problem**: `pip: command not found`  
**Solution**: Python not in PATH. Reinstall Python with "Add to PATH" checked

**Problem**: `ModuleNotFoundError`  
**Solution**: Run `pip install -r requirements.txt` again

**Problem**: Chrome not found  
**Solution**: Install Google Chrome browser

### Docker Issues

**Problem**: Permission denied  
**Solution**: Run with `sudo` or add user to docker group

**Problem**: Container won't start  
**Solution**: Check Chrome installation in container

---

**Happy Downloading! 🎉**

For more details, visit: https://github.com/Avisav24/NSE_Data_Downloader
