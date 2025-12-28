# ANDON System with Arduino and Python

A comprehensive ANDON (manufacturing alert system) implementation using Arduino for hardware control and Python for monitoring and logging.

## Overview

The ANDON system is a visual and audible alert system used in manufacturing environments to signal problems on the production line. This implementation provides:

- **Hardware Control**: Arduino-based system with multiple input buttons and visual/audio indicators
- **Monitoring Software**: Python applications (GUI and CLI) for real-time monitoring
- **Alert Management**: Different alert types with appropriate visual and audio feedback
- **Logging**: Historical alert tracking and logging
- **Serial Communication**: Reliable Arduino-Python communication protocol

## Features

### Hardware (Arduino)
- ✅ 4 programmable alert buttons
- ✅ RGB LED indicators (Red/Yellow/Green)
- ✅ Buzzer for audio alerts
- ✅ Debounced button inputs
- ✅ Serial communication interface
- ✅ System test functionality

### Software (Python)
- ✅ **GUI Monitor**: User-friendly tkinter interface
- ✅ **CLI Monitor**: Command-line interface for headless operation
- ✅ Real-time status display
- ✅ Alert history logging (JSON format)
- ✅ System control commands
- ✅ Automatic port detection

## Alert Types

1. **Emergency** (Button 1)
   - Red LED indicator
   - Pulsing buzzer
   - Highest priority

2. **Quality Issue** (Button 2)
   - Yellow LED indicator
   - Silent alert
   - Medium priority

3. **Material Shortage** (Button 3)
   - Blinking yellow LED
   - Silent alert
   - Medium priority

4. **Maintenance Needed** (Button 4)
   - Yellow LED indicator
   - Silent alert
   - Medium priority

## Quick Start

### Hardware Setup
1. Wire your Arduino according to the [wiring diagram](docs/WIRING.md)
2. Upload the Arduino sketch from `arduino/ANDON_System.ino`
3. Connect Arduino to your computer via USB

### Software Setup
```bash
# Install Python dependencies
cd python
pip install -r requirements.txt

# Run GUI monitor
python andon_monitor.py

# OR run CLI monitor
python andon_cli.py
```

## Documentation

- 📘 [Setup Guide](docs/SETUP.md) - Complete installation and setup instructions
- 🔌 [Wiring Diagram](docs/WIRING.md) - Hardware connection details

## System Architecture

```
┌─────────────────┐         USB/Serial        ┌──────────────────┐
│                 │◄──────────────────────────►│                  │
│  Arduino        │                            │  Python Monitor  │
│  (Hardware)     │    Commands & Alerts      │  (Software)      │
│                 │                            │                  │
│  - Buttons      │                            │  - GUI/CLI       │
│  - LEDs         │                            │  - Logging       │
│  - Buzzer       │                            │  - History       │
└─────────────────┘                            └──────────────────┘
```

## Project Structure

```
ANDON-Rev-B-/
├── arduino/
│   └── ANDON_System.ino          # Arduino sketch
├── python/
│   ├── andon_monitor.py          # GUI application
│   ├── andon_cli.py              # CLI application
│   └── requirements.txt          # Python dependencies
├── docs/
│   ├── SETUP.md                  # Setup guide
│   └── WIRING.md                 # Wiring diagram
└── README.md                     # This file
```

## Usage Examples

### Using GUI Monitor
1. Launch the application
2. Select Arduino port from dropdown
3. Click "Connect"
4. Monitor alerts in real-time
5. Use control buttons to interact with system

### Using CLI Monitor
```bash
# Start interactive mode
python andon_cli.py

# Commands available:
ANDON> status    # Check system status
ANDON> reset     # Reset to normal state
ANDON> test      # Run system test
ANDON> monitor   # Start monitoring mode
ANDON> quit      # Exit application
```

### Arduino Commands

Send these commands via Serial Monitor or Python application:
- `STATUS` - Get current system status
- `RESET` - Reset system to normal state
- `TEST` - Run component test sequence

## Requirements

### Hardware
- Arduino Uno or compatible (ATmega328P)
- 4x Push buttons
- 3x LEDs (Red, Yellow, Green)
- 3x 220Ω resistors
- 1x Buzzer (5V)
- Breadboard and jumper wires
- USB cable

### Software
- Arduino IDE 1.8+ (for programming Arduino)
- Python 3.6+
- pyserial library

## Communication Protocol

### Arduino → Python (Alerts)
```
ALERT:EMERGENCY
ALERT:QUALITY_ISSUE
ALERT:MATERIAL_SHORTAGE
ALERT:MAINTENANCE_NEEDED
```

### Arduino → Python (Status)
```
STATUS:NORMAL
STATUS:EMERGENCY
STATUS:QUALITY_ISSUE
STATUS:MATERIAL_SHORTAGE
STATUS:MAINTENANCE_NEEDED
```

### Python → Arduino (Commands)
```
RESET          # Reset system to normal
STATUS         # Request current status
TEST           # Run system test
```

## Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Arduino not detected | Check USB cable, install drivers, try different port |
| No response to buttons | Verify wiring, check Serial Monitor |
| LEDs not working | Check polarity and resistors |
| Python import errors | Install requirements: `pip install -r requirements.txt` |
| Permission denied (Linux) | Add user to dialout group: `sudo usermod -a -G dialout $USER` |

For detailed troubleshooting, see [SETUP.md](docs/SETUP.md).

## Customization

### Pin Configuration
Edit pin definitions in `arduino/ANDON_System.ino`:
```cpp
const int BUTTON_PIN_1 = 2;  // Emergency button
const int LED_RED = 8;       // Emergency LED
// ... customize as needed
```

### Alert Behavior
Modify state handlers in `updateStateIndicators()` function to change LED patterns and buzzer behavior.

### Monitoring Interface
Extend Python applications to add:
- Email notifications
- Web dashboard
- Database logging
- SMS alerts
- Integration with other systems

## Contributing

Contributions are welcome! Areas for enhancement:
- Web-based monitoring interface
- Database integration
- Multiple Arduino support
- Additional alert types
- Wireless communication
- Mobile app integration

## License

This project is provided as-is for educational and manufacturing purposes.

## Acknowledgments

ANDON system inspired by lean manufacturing principles and Toyota Production System.
