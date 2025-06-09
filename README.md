# FletImageDownloader 🖼️

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/Flet-0.86.2-6366F1?logo=flutter&logoColor=white)](https://flet.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/mihaiapostol14/FletImageDownloader?style=social)](https://github.com/mihaiapostol14/FletImageDownloader)

A modern, lightweight desktop application for downloading images from Bing using an intuitive GUI built with Flet.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

## Preview

<div align="center">

![FletImageDownloader Preview](https://github.com/mihaiapostol14/FletImageDownloader/blob/299c14f288b4e67d55a9fa60b92d5e0fd4e9335d/assets/preview.png)

</div>



---

## 📋 Overview

**FletImageDownloader** is a Python-based desktop application that provides an elegant user interface for bulk downloading images from Bing Image Search. It leverages the power of `icrawler` for efficient web crawling and `Flet` for cross-platform UI rendering.

---

## ✨ Features

- 🔍 **Advanced Search** - Search for any keyword and download relevant images instantly
- 📊 **Batch Download** - Configure custom image count limits (1-∞)
- 📁 **Smart Organization** - Auto-creates folders named by search query
- ⌨️ **Keyboard Shortcuts** - Press `Enter` to trigger downloads
- 🖱️ **One-Click Access** - Open downloaded folders directly from the app
- 💻 **Cross-Platform** - Runs on Windows, macOS, and Linux
- 🚀 **Async Processing** - Non-blocking UI during download operations
- 📈 **Real-Time Updates** - Live count of downloaded images

---

## 📦 Prerequisites

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (included with Python)
- **Git** ([Download](https://git-scm.com/))
- **Virtual Environment** (venv) - [Learn More](https://mihaiapostol14.github.io/PyEnvLaunchpad/)

---

## 🚀 Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/mihaiapostol14/FletImageDownloader.git 
cd FletImageDownloader
```

### Step 1: Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python interface.py
```

The application window will open with dimensions of **400x450px**, displaying a clean, centered interface.

---

## 💻 Usage

1. **Enter Search Query** - Type the subject you want to download images for (e.g., "cats", "mountains", "technology")
2. **Set Image Count** - Specify the number of images to download (numeric input only)
3. **Download** - Click `Download` button or press `Enter` to start the process
4. **View Results** - The UI updates with the count of successfully downloaded images
5. **Open Folder** - Click the dynamic `Open` button to view downloaded images in your file explorer

### Example Workflow

```
Search Image: "sunset landscape"
Image Count: 50
[Download] → Downloads 50 sunset landscape images
→ "Count image sunset landscape is 50"
→ [Open sunset landscape]
```

---

## 📁 Project Structure

```
FletImageDownloader/
├── interface.py              # Main application entry point & UI logic
├── requirements.txt          # Python dependencies
├── helper/
│   ├── __init__.py          # Helper module initialization
│   └── helper.py            # Utility functions (file I/O, validation)
├── assets/
│   ├── icon/
│   │   └── icon.ico         # Application window icon
│   └── preview.png          # UI preview screenshot
└── README.md                # Project documentation
```

---

## 🏗️ Architecture

### Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **UI Framework** | Flet | 0.86.2 | Cross-platform desktop GUI |
| **Image Crawler** | iCrawler | 0.6.10 | Web scraping & image downloading |
| **Search Engine** | Bing Image Search | - | Image source provider |
| **Runtime** | Python | 3.8+ | Core application language |
| **Package Manager** | pip | Latest | Dependency management |

### Design Pattern

```
┌─────────────────────────────────────┐
│         Flet UI Layer               │
│  (Cross-platform GUI Components)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    ImageDownloader (Main Class)     │
│  - Widget initialization            │
│  - Event handling (keyboard, clicks)│
│  - Image download orchestration     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Helper (Utility Base Class)    │
│  - Directory management             │
│  - File I/O operations              │
│  - Random pause utilities           │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   iCrawler BingImageCrawler         │
│  - Bing Image Search integration    │
│  - Parallel download threads (4x)   │
│  - Logging & error handling         │
└─────────────────────────────────────┘
```

### Key Classes

#### **ImageDownloader**
- Inherits from `Helper`
- Manages Flet page and widget lifecycle
- Handles user inputs and validation
- Orchestrates BingImageCrawler operations
- Updates UI with download progress

#### **Helper**
- Base utility class with reusable methods:
  - `create_directory()` - Safe directory creation
  - `directory_exists()` - Path validation
  - `create_file_from_list()` - Batch file creation
  - `random_pause_code()` - Rate limiting

---

## 🔧 Configuration

### Window Settings (interface.py)

```python
self.page.window.width = 400           # Window width in pixels
self.page.window.height = 450          # Window height in pixels
self.page.window.icon = "../assets/icon/icon.ico"  # Custom icon
self.page.window.resizable = False     # Disable window resizing
self.page.window.maximizable = False   # Disable maximization
```

### Crawler Settings (interface.py)

```python
crawler = BingImageCrawler(
    downloader_threads=4,              # Parallel download threads
    storage={"root_dir": output_directory},
    log_level=logging.INFO,
)
```

---

## 📝 Code Quality Analysis

### PEP 8 Compliance

✅ **Line Length** - Properly formatted (< 88 characters)  
✅ **Indentation** - Consistent 4-space indentation  
✅ **Imports** - Organized by standard, third-party modules  
⚠️ **Error Handling** - Uses bare `except` in helper.py (line 20)  
⚠️ **Naming** - Typo in `crate_file()` method (should be `create_file()`)  

### Recommended Improvements

**1. Fix Typo in helper.py (Line 35)**
```python
# Current
def crate_file(self, filename='', mode='w', data=''):

# Recommended
def create_file(self, filename='', mode='w', data=''):
```

**2. Improve Error Handling (Line 20)**
```python
# Current
except OSError:
    ...

# Recommended
except OSError as e:
    print(f"Failed to create directory '{name_directory}': {e}")
```

**3. Simplify Logic (Line 24-28)**
```python
# Current
def directory_exists(self, directory_name=''):
    exist = True
    if os.path.exists(directory_name):
        return exist
    return False

# Recommended
def directory_exists(self, directory_name=''):
    return os.path.exists(directory_name)
```

---

## 🔐 Security Considerations

### Input Validation
- ✅ Search query stripped of whitespace
- ✅ Image count validated as integer
- ❓ Consider filename sanitization for special characters

### Platform Compatibility
- ✅ `os.startfile()` only works on Windows (line 184)
- 💡 Consider using cross-platform `webbrowser` or `pathlib`

### Improvements

```python
# Enhanced cross-platform folder opening
import platform
from pathlib import Path

async def open_output_directory(self, e):
        """
        Opens the downloaded folder using the
        native system file explorer.
        """

        if not self.search_query:
            return

        folder_path = (
            self.output_directory / self.search_query
        ).resolve()

        if not folder_path.exists():
            self.show_message(
                "Download folder does not exist.",
                self.colors["error"],
            )
            return

        try:
            if platform.system() == "Windows":
                os.startfile(folder_path)

            elif platform.system() == "Darwin":
                subprocess.Popen(
                    ["open", str(folder_path)]
                )

            else:
                subprocess.Popen(
                    ["xdg-open", str(folder_path)]
                )

        except Exception as error:
            print(
                f"[Error] Failed to open directory: "
                f"{error}"
            )

```

---

## 🐛 Troubleshooting

### **Issue: "ModuleNotFoundError: No module named 'flet'"**
```bash
pip install --upgrade flet flet-cli
```

### **Issue: "BingImageCrawler: No images found"**
- Check internet connection
- Try a different search keyword
- Verify Bing Image Search is accessible in your region

### **Issue: "Icon not found" warning**
- Ensure `assets/icon/` directory exists
- Verify `icon.ico` file is in the correct location
- Application will still run without the icon

### **Issue: Download fails silently**
- Check disk space availability
- Verify write permissions in the target directory
- Review console output for detailed error messages

---

## 📊 Dependencies Overview

### Core Dependencies
```
flet==0.86.2           # UI framework
icrawler==0.6.10       # Image crawler
requests==2.34.2       # HTTP library
beautifulsoup4==4.15.0 # HTML parsing
pillow==12.3.0         # Image processing
```

### Full Dependency Tree
See [requirements.txt](requirements.txt) for complete list of 56 packages.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes with clear messages (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mihai Apostol**  
GitHub: [@mihaiapostol14](https://github.com/mihaiapostol14)

---

## 📞 Support

For issues, questions, or suggestions:
- 🐛 [Open an Issue](https://github.com/mihaiapostol14/FletImageDownloader/issues)
- 💬 [Start a Discussion](https://github.com/mihaiapostol14/FletImageDownloader/discussions)
- 📧 [Contact via Email](mailto:your-email@example.com)

---

## 🎯 Roadmap

- [ ] Add image filtering (by size, resolution, date)
- [ ] Implement pause/resume functionality
- [ ] Add progress bar with ETA
- [ ] Support for multiple search engines (Google, DuckDuckGo)
- [ ] Settings panel for advanced configuration
- [ ] Download history tracking
- [ ] Unit tests and CI/CD pipeline

---

<div align="center">

**⭐ If you found this useful, consider giving it a star!**

Made with ❤️ by Mihai Apostol

</div>
