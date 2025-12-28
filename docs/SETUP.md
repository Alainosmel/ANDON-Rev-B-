# ANDON System Setup Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Hardware Setup](#hardware-setup)
3. [Arduino Setup](#arduino-setup)
4. [Python Setup](#python-setup)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)

## Introduction

The ANDON System is a manufacturing alert system that allows operators to signal various issues on the production line. This implementation uses Arduino for hardware control and Python for monitoring and logging.

### Features
- 4 different alert types (Emergency, Quality Issue, Material Shortage, Maintenance)
- Visual indicators (Red, Yellow, Green LEDs)
- Audio alert (Buzzer for emergencies)
- Serial communication with Python application
- GUI and CLI monitoring options
- Alert history logging

## Hardware Setup

### Required Components
- Arduino Uno or compatible board
- 4 push buttons
- 3 LEDs (Red, Yellow, Green)
- 3x 220Ω resistors (for LEDs)
- 1 buzzer (5V active buzzer or piezo)
- Breadboard and jumper wires
- USB cable for Arduino

### Wiring
Refer to [WIRING.md](WIRING.md) for detailed wiring instructions.

Quick summary:
- Buttons on pins 2-5 (connected to GND, using internal pullups)
- Red LED on pin 8
- Yellow LED on pin 9
- Green LED on pin 10
- Buzzer on pin 11

## Arduino Setup

### 1. Install Arduino IDE
Download and install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software)

### 2. Upload the Sketch

1. Open Arduino IDE
2. Open `arduino/ANDON_System.ino`
3. Select your Arduino board: `Tools > Board > Arduino Uno`
4. Select the correct port: `Tools > Port > (select your Arduino port)`
5. Click Upload button (→)

### 3. Verify Operation

Open Serial Monitor (`Tools > Serial Monitor`) and set baud rate to 9600.
You should see:
```
ANDON System Ready
```

Test the system by pressing buttons or sending commands:
- `STATUS` - Get current system status
- `RESET` - Reset to normal state
- `TEST` - Run system test

## Python Setup

### 1. Install Python
Ensure Python 3.6 or higher is installed:
```bash
python --version
```

### 2. Install Dependencies
Navigate to the python directory and install requirements:
```bash
cd python
pip install -r requirements.txt
```

This installs:
- pyserial (for serial communication)

### 3. Run the Application

#### Option A: GUI Monitor (Recommended)
```bash
python andon_monitor.py
```

Features:
- Visual status display with color indicators
- Connection management
- System controls (Reset, Status, Test)
- Alert history with timestamps
- Log viewer

#### Option B: Command Line Monitor
```bash
python andon_cli.py
```

Or specify port directly:
```bash
python andon_cli.py /dev/ttyUSB0
```

Features:
- Interactive command mode
- Real-time monitoring
- Simple text-based interface
- Good for headless systems

## Usage

### Normal Operation

1. Connect Arduino via USB
2. Start Python monitor application
3. Select correct COM port
4. Click "Connect"

System should show "NORMAL" with green indicator.

### Triggering Alerts

Press any button on the Arduino:
- **Button 1**: Emergency alert (Red LED + Buzzer)
- **Button 2**: Quality issue (Yellow LED)
- **Button 3**: Material shortage (Blinking Yellow LED)
- **Button 4**: Maintenance needed (Yellow LED)

### Resetting Alerts

From Python application:
- Click "Reset System" button (GUI)
- Type `reset` command (CLI)

System returns to NORMAL state with green LED.

### Viewing History

The GUI application automatically logs all alerts to `andon_log.json`.
View history in the application log window.

### System Test

Run a system test to verify all components:
- Click "Test System" button (GUI)
- Type `test` command (CLI)

This will:
1. Light each LED sequentially
2. Sound the buzzer briefly
3. Return to normal state

## Troubleshooting

### Arduino Not Connecting

**Problem**: Cannot find Arduino port

**Solutions**:
- Check USB cable connection
- Install Arduino drivers if needed
- Check Device Manager (Windows) or `ls /dev/tty*` (Linux/Mac)
- Try different USB port
- Press "Refresh Ports" button

### No Response from Arduino

**Problem**: Connected but no response to commands

**Solutions**:
- Verify correct baud rate (9600)
- Check Serial Monitor in Arduino IDE works
- Re-upload Arduino sketch
- Reset Arduino board
- Check for loose wiring

### LEDs Not Working

**Problem**: LEDs don't light up or behave incorrectly

**Solutions**:
- Verify LED polarity (long leg = positive)
- Check resistor values (220Ω recommended)
- Test with multimeter
- Verify pin connections match code
- Check for loose connections

### Buttons Not Working

**Problem**: Button presses not detected

**Solutions**:
- Verify button connections (button to GND)
- Test button continuity with multimeter
- Check debounce timing (may need adjustment)
- Ensure internal pullups are enabled in code

### Python Import Errors

**Problem**: ModuleNotFoundError: No module named 'serial'

**Solutions**:
```bash
pip install pyserial
```

Or use pip3 on some systems:
```bash
pip3 install pyserial
```

### Permission Denied (Linux/Mac)

**Problem**: Cannot open serial port, permission denied

**Solutions**:
```bash
# Add user to dialout group (Linux)
sudo usermod -a -G dialout $USER
# Log out and back in

# Or change port permissions temporarily
sudo chmod 666 /dev/ttyUSB0
```

### GUI Not Displaying (Headless System)

**Problem**: tkinter errors on headless system

**Solution**: Use CLI version instead:
```bash
python andon_cli.py
```

## Advanced Configuration

### Changing Pin Assignments

Edit `arduino/ANDON_System.ino`:
```cpp
// Pin Definitions (lines 12-22)
const int BUTTON_PIN_1 = 2;  // Change to your pin
const int LED_RED = 8;       // Change to your pin
// ... etc
```

### Adjusting Debounce Time

Edit `arduino/ANDON_System.ino`:
```cpp
const unsigned long debounceDelay = 50;  // Change value in milliseconds
```

### Changing Baud Rate

Edit both Arduino and Python code:

Arduino (`arduino/ANDON_System.ino`):
```cpp
Serial.begin(9600);  // Change to desired baud rate
```

Python (`python/andon_monitor.py` or `andon_cli.py`):
```python
self.serial_port = serial.Serial(port, 9600)  # Change to match Arduino
```

## Support

For issues or questions:
1. Check troubleshooting section
2. Review wiring diagram
3. Test components individually
4. Check serial monitor for error messages
5. Verify all connections with multimeter

## Safety

- Always disconnect power before changing wiring
- Use appropriate current-limiting resistors
- Do not exceed Arduino's current ratings
- Ensure proper ventilation for enclosed systems
- Follow local electrical safety codes
