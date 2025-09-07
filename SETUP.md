# Quick Setup Guide

## 🚀 Recommended: One-Click Setup

### Windows Users
1. Download/clone the project
2. Double-click `run.bat`
3. Wait for virtual environment creation and dependency installation
4. App opens in browser automatically
5. **Everything installs in `venv` folder - nothing touches your system!**

### Linux/Mac Users
1. Download/clone the project
2. Open terminal in project folder
3. Run: `chmod +x run.sh && ./run.sh`
4. Wait for setup to complete
5. App opens in browser automatically

## 🔧 Manual Setup (If needed)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
streamlit run app.py
```

## 🛡️ Virtual Environment Benefits

✅ **Isolated Installation**: All packages go to `venv` folder  
✅ **No Global Pollution**: Your system Python stays clean  
✅ **Easy Removal**: Delete `venv` folder to uninstall everything  
✅ **Consistent Environment**: Same versions for everyone  
✅ **No Admin Rights**: No need for administrator privileges  

## 🔍 Troubleshooting

### Python not found
- Install Python 3.8+ from [python.org](https://python.org)
- Make sure "Add Python to PATH" is checked during installation

### Permission error (Windows)
- Right-click `run.bat` → "Run as administrator"
- Or use manual setup method

### Virtual environment activation fails
- Try manual setup with explicit python path
- Check if antivirus is blocking script execution

### Module not found after installation
- Make sure virtual environment is activated
- Re-run the setup script

### Port already in use
- Close other Streamlit applications
- Or change port: `streamlit run app.py --server.port 8502`

## 📋 System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for dependencies
- **Browser**: Chrome, Firefox, Safari, or Edge
