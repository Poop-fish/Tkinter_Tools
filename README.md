# Random Utility Tools

Here is a collection of tools built using Python and `tkinter`:

- **Auto Clicker**: Automates mouse clicks with customizable intervals and hotkey support.  
- **ICO Converter**: Converts PNG images to ICO format with multiple size options and live preview.  
- **Python to EXE Converter**: Converts `.py` files to standalone `.exe` executables with PyInstaller.  
- **ASCII Generator**: Converts text and images into ASCII art with customizable fonts and stylized output.  
- **Bug Rporting App**: Easy and simple way to track bugs 
---

## Features

### **Auto Clicker**
 Customizable click intervals (predefined & manual input).  
Hotkey support (`F6` to start, `F7` to stop).  
Right-click on Start/Stop buttons to set custom keybinds.  
Multi-threaded execution to prevent UI freezing.  
  
---

### **ICO Converter**
 Converts **PNG** images to **ICO** format with multiple sizes.  
 Live preview of the selected image.  
 Supports maintaining aspect ratio and transparency.  
 Select multiple icon sizes (16x16, 32x32, 48x48, etc.).  
 Saves in high-quality `.ico` format.  

---

### **Python to EXE Converter**
 Converts `.py` scripts into `.exe` executables using **PyInstaller**.  
 Options to create a **single executable file** (`--onefile`).  
 Toggle **console window visibility** (`--console` / `--noconsole`).  
 Supports **custom icons** for EXE files.  
 Live **conversion output** inside the app.  

---

### **ASCII Generator**
 Convert text to **ASCII art** using customizable fonts.  
 Convert images to ASCII art using a selected width.  
 Stylize output with borders and copy the result to clipboard.  
 Adjustable font size and selection from a wide range of fonts.  
 Supports **PNG**, **JPG**, and **JPEG** image formats for conversion.  
 
---

### **Bug Reporting App**
- A user-friendly application designed to report bugs with detailed descriptions, reproduction steps, severity, platform, and game version.  

- **Features:**
  - Submit and view detailed bug reports with options to add screenshots and videos.
  - Filter and search through submitted reports based on title, severity, and status.
  - Edit, delete, and mark reports as resolved.
  - Real-time status updates and reports management.
- The app provides a dynamic UI with a customizable sidebar and progress indicators for uploading files.
- Bug reports are saved to a JSON file, allowing for persistent storage and management.
- Includes a color cycling background for an engaging user experience.  

---

### **Install dependencies**

```python
pip install pyautogui keyboard pillow pyinstaller pyfiglet pyperclip numpy tkinter tk colorsys
```

After you intsall these if it still doesnt work just copy paste all the imports into chatgpt or google for the insalls.

---

### **Run Applications**

- AutoClicker.py

- IconConverter.py

- PyExE.py

- ASCII_Generator.py

--- 

# How to Basics

### Auto Clicker

 - Run the script
AutoClicker.py

- Set Click Interval

- Select a predefined interval from the dropdown, or
Enter a custom interval in the text box.
Start Clicking

- Press F6 or click the Start button.
Pressing the start key multiple times increases the click speed.
Stop Clicking

- Press F7 or click the Stop button.
Change Keybinds

- Right-click the Start/Stop button and press a new key.

### ICO Converter

- Run the script
IconConverter.py

- Load an Image
Click the "Browse PNG" button and select a .png file.
Select Icon Sizes

Choose one or more sizes from the checkboxes (16x16, 32x32, etc.).
The preview updates automatically.
Convert the Image

- Click "Convert to ICO", select a save location, and done! 🎉


### Py to EXE Converter

- Run the script
PyExE.py

- Select a Python file (.py)

- Click the Browse button and select your script.
Choose Conversion Options

- One File Mode: Select if you want a single .exe file (--onefile).
Console Mode: Choose whether to show the console window (--console).
Icon File: Select a custom .ico file for your application.
Additional Arguments: Add extra PyInstaller options if needed.
Start Conversion

- Click "Convert to EXE", and the conversion process will begin.
The live console output will show progress.

### ASCII Generator

- Run the script
ASCII_Generator.py

- Open Image (PNG, JPG, JPEG)
Click the Open Image button to select a file and convert it to ASCII art.
Convert Text to ASCII

Type your text in the output box, select a font from the dropdown, and press Text to ASCII.
Stylize Text

- Click Frame Text to add a border to your ASCII output.

- Copy to Clipboard
Use the Copy to Clipboard button to copy the ASCII output for use elsewhere.

---

# Disclaimer
### ⚠ Use these tools responsibly.

The Auto Clicker may be considered cheating in certain applications—use it ethically.
The ICO Converter supports PNG transparency, but results may vary based on input quality.
The Python to EXE Converter requires PyInstaller and works best with scripts that don’t have external dependencies.
The ASCII Generator supports images in PNG, JPG, and JPEG formats, but results may vary based on input image complexity.
