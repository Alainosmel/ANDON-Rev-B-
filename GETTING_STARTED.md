# Getting Started with ANDON System - Step by Step

This guide will help you set up the ANDON system on a new computer from scratch.

## What You Need

### Hardware
- Arduino Uno (or compatible board)
- USB cable to connect Arduino to computer
- 4 push buttons
- 3 LEDs (Red, Yellow, Green)
- 3x 220Ω resistors (for LEDs)
- 1 buzzer (5V)
- Breadboard and jumper wires

### Software
- Computer with Windows, macOS, or Linux
- Internet connection for downloading software

---

## Step 1: Install Arduino IDE

1. **Download Arduino IDE**
   - Go to https://www.arduino.cc/en/software
   - Download the version for your operating system
   - Install it following the installer instructions

2. **Verify Installation**
   - Open Arduino IDE
   - You should see the main window with a blank sketch

---

## Step 2: Install Python

1. **Check if Python is already installed**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **If not installed, download Python**
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or newer
   - **Important for Windows**: Check "Add Python to PATH" during installation

3. **Verify Python installation**
   ```bash
   python --version
   # Should show: Python 3.x.x
   ```

---

## Step 3: Download/Clone the ANDON System Code

If you have this repository already, great! If not:

**Option A: Using Git**
```bash
git clone https://github.com/Alainosmel/ANDON-Rev-B-.git
cd ANDON-Rev-B-
```

**Option B: Download ZIP**
1. Go to the repository page on GitHub
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to a folder
4. Open terminal/command prompt in that folder

---

## Step 4: Wire the Arduino Hardware

Follow the wiring diagram in `docs/WIRING.md`. Quick reference:

### Connections:
```
Buttons (connected to GND when pressed):
- Button 1 (Emergency) → Pin 2
- Button 2 (Quality)   → Pin 3
- Button 3 (Material)  → Pin 4
- Button 4 (Maintenance) → Pin 5

LEDs (with 220Ω resistors):
- Red LED    → Pin 8 → [220Ω] → LED → GND
- Yellow LED → Pin 9 → [220Ω] → LED → GND
- Green LED  → Pin 10 → [220Ω] → LED → GND

Buzzer:
- Buzzer → Pin 11 → Buzzer (+) → GND (-)
```

**Tips:**
- Use a breadboard for easier connections
- Connect all GND connections to Arduino GND pin
- Ensure LED polarity is correct (long leg = positive)

---

## Step 5: Upload Arduino Code

1. **Connect Arduino to Computer**
   - Plug USB cable into Arduino and computer

2. **Open Arduino Sketch**
   - Open Arduino IDE
   - File → Open → Navigate to `arduino/ANDON_System.ino`
   - Click Open

3. **Select Board and Port**
   - Tools → Board → Select "Arduino Uno" (or your board type)
   - Tools → Port → Select the port with your Arduino
     - Windows: Usually `COM3`, `COM4`, etc.
     - Mac: Usually `/dev/cu.usbmodem...`
     - Linux: Usually `/dev/ttyUSB0` or `/dev/ttyACM0`

4. **Upload the Code**
   - Click the Upload button (→ arrow icon)
   - Wait for "Done uploading" message
   - Green LED should turn on (indicating NORMAL state)

5. **Test Arduino**
   - Open Tools → Serial Monitor
   - Set baud rate to 9600
   - You should see: `ANDON System Ready`
   - Type `STATUS` and press Enter
   - You should see: `STATUS:NORMAL`

---

## Step 6: Install Python Dependencies

1. **Navigate to Python folder**
   ```bash
   cd python
   ```

2. **Install required libraries**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using Python 3:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import serial; print('pyserial installed successfully')"
   ```

---

## Step 7: Run the ANDON Monitor Application

You have two options:

### Option A: GUI Application (Recommended)

1. **Run the GUI monitor**
   ```bash
   python andon_monitor.py
   ```
   
   Or:
   ```bash
   python3 andon_monitor.py
   ```

2. **Use the application**
   - Select your Arduino port from dropdown
   - Click "Connect"
   - Status should show "NORMAL" in green
   - Press buttons on Arduino to trigger alerts
   - Use "Reset System" button to clear alerts

### Option B: Command Line Interface

1. **Run the CLI monitor**
   ```bash
   python andon_cli.py
   ```

2. **Follow the prompts**
   - Select port number when asked
   - Type commands: `status`, `reset`, `test`, `monitor`
   - Press Ctrl+C to exit monitoring mode

---

## Step 8: Test the System

1. **Run automated test**
   ```bash
   python test_system.py
   ```
   
   This will:
   - Find your Arduino automatically
   - Test STATUS command
   - Test RESET command
   - Run system test (LEDs and buzzer)

2. **Manual testing**
   - Press Button 1 → Red LED + buzzer should activate
   - Press Button 2 → Yellow LED should turn on
   - Press Button 3 → Yellow LED should blink
   - Press Button 4 → Yellow LED should turn on
   - Use "Reset" in Python app → Green LED should turn on

---

## Common Issues and Solutions

### Issue: "Port not found" or "Permission denied"

**Windows:**
- Install Arduino drivers from Arduino IDE
- Try different USB port
- Check Device Manager for COM port

**Mac:**
- No special action needed usually
- If issues, install CH340 drivers (for clone boards)

**Linux:**
- Add user to dialout group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- Log out and log back in
- Or temporarily:
  ```bash
  sudo chmod 666 /dev/ttyUSB0
  ```

### Issue: "ModuleNotFoundError: No module named 'serial'"

**Solution:**
```bash
pip install pyserial
# or
pip3 install pyserial
```

### Issue: Arduino not responding

**Solutions:**
1. Press the reset button on Arduino
2. Re-upload the sketch
3. Check Serial Monitor (9600 baud)
4. Verify wiring connections

### Issue: LEDs not lighting up

**Solutions:**
1. Check LED polarity (long leg = positive)
2. Verify resistor connections
3. Test LEDs with multimeter
4. Check pin numbers in code match wiring

### Issue: Python GUI won't start

**Solutions:**
1. Make sure tkinter is installed:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Mac (should be included)
   # Windows (included with Python)
   ```
2. Use CLI version instead: `python andon_cli.py`

---

## Quick Command Reference

### Arduino Commands (via Serial Monitor or Python app)
```
STATUS   - Get current system status
RESET    - Reset system to normal
TEST     - Run component test
```

### Python CLI Commands
```
status   - Check system status
reset    - Reset to normal
test     - Test all components
monitor  - Start real-time monitoring
quit     - Exit application
```

---

## Next Steps

Once everything is working:

1. **Customize the system**
   - Edit pin numbers in `arduino/ANDON_System.ino`
   - Modify alert types and behaviors
   - Adjust LED patterns and buzzer sounds

2. **Add more features**
   - Connect more buttons for additional alerts
   - Add LCD display for status
   - Integrate with your existing systems

3. **Read the documentation**
   - `README.md` - Project overview
   - `docs/SETUP.md` - Detailed setup guide
   - `docs/ARCHITECTURE.md` - System design
   - `docs/WIRING.md` - Wiring details

---

## Integration with Your Flask Application

If you have an existing Flask application (like the `app.py` you mentioned), you can integrate the ANDON system:

### Option 1: Use Serial Communication from Flask

Add this to your Flask app:

```python
import serial
import threading

# Initialize ANDON connection
andon_port = None
andon_serial = None

def connect_andon(port='/dev/ttyUSB0'):
    global andon_serial
    try:
        andon_serial = serial.Serial(port, 9600, timeout=1)
        print(f"Connected to ANDON on {port}")
        return True
    except Exception as e:
        print(f"Failed to connect to ANDON: {e}")
        return False

def send_andon_alert(alert_type):
    """Send alert to ANDON system"""
    if andon_serial:
        # The Arduino receives alerts via button presses
        # To trigger from software, you could modify the Arduino
        # to accept ALERT commands via serial
        pass

def reset_andon():
    """Reset ANDON system"""
    if andon_serial:
        andon_serial.write(b"RESET\n")

# Use in your Flask routes
@app.route('/trigger_andon', methods=['POST'])
def trigger_andon():
    # Trigger ANDON alert based on production events
    reset_andon()
    return jsonify({"status": "ok"})
```

### Option 2: Run ANDON Monitor Separately

Keep the ANDON system as a separate monitoring application that runs alongside your Flask app. Operators can use both interfaces:
- Flask app for production tracking
- ANDON monitor for alerts

---

## Need More Help?

1. Check `docs/SETUP.md` for detailed troubleshooting
2. Review `docs/ARCHITECTURE.md` for system design
3. Test each component individually
4. Use Serial Monitor to debug Arduino communication

Good luck! 🚀
