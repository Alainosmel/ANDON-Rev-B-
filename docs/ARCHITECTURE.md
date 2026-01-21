# ANDON System Architecture

## System Overview

The ANDON system consists of three main components working together:

```
┌────────────────────────────────────────────────────────────────┐
│                        ANDON SYSTEM                            │
└────────────────────────────────────────────────────────────────┘

┌─────────────────┐        ┌──────────────┐       ┌──────────────┐
│   Input Layer   │───────►│ Control Unit │──────►│ Output Layer │
│   (Buttons)     │        │  (Arduino)   │       │ (LED/Buzzer) │
└─────────────────┘        └──────────────┘       └──────────────┘
                                  │
                                  │ Serial
                                  │ Communication
                                  ▼
                           ┌──────────────┐
                           │  Monitoring  │
                           │   Software   │
                           │   (Python)   │
                           └──────────────┘
```

## Component Details

### 1. Input Layer
**4 Push Buttons** - Operator interface for triggering alerts

| Button | Function | Priority |
|--------|----------|----------|
| 1 | Emergency Stop | Critical |
| 2 | Quality Issue | High |
| 3 | Material Shortage | Medium |
| 4 | Maintenance Request | Medium |

### 2. Control Unit (Arduino)
**Microcontroller**: Arduino Uno (ATmega328P)

**Responsibilities**:
- Read button inputs with debouncing
- Process alert states
- Control visual/audio indicators
- Manage serial communication
- Execute commands from Python

**State Machine**:
```
        ┌──────────┐
        │  NORMAL  │◄────────┐
        └────┬─────┘         │
             │               │
   Button    │               │ RESET
   Press     │               │ Command
             ▼               │
      ┌─────────────┐        │
      │   ALERT     │────────┘
      │   ACTIVE    │
      └─────────────┘
```

### 3. Output Layer

**Visual Indicators** (LEDs):
- 🔴 Red LED: Emergency / Critical alerts
- 🟡 Yellow LED: Warnings / Medium priority
- 🟢 Green LED: Normal operation

**Audio Indicator**:
- 🔊 Buzzer: Emergency alerts only

**Behavior Matrix**:

| State | Red LED | Yellow LED | Green LED | Buzzer |
|-------|---------|------------|-----------|--------|
| Normal | OFF | OFF | ON | OFF |
| Emergency | ON | OFF | OFF | PULSING |
| Quality Issue | OFF | ON | OFF | OFF |
| Material Shortage | OFF | BLINKING | OFF | OFF |
| Maintenance | OFF | ON | OFF | OFF |

### 4. Monitoring Software (Python)

**Two Applications**:

#### A. GUI Monitor (`andon_monitor.py`)
```
┌─────────────────────────────────────────┐
│        ANDON System Monitor             │
├─────────────────────────────────────────┤
│  Connection: [COM3 ▼] [Connect]        │
├─────────────────────────────────────────┤
│                                         │
│         ┌───────────────────┐           │
│         │                   │           │
│         │     NORMAL        │           │
│         │                   │           │
│         └───────────────────┘           │
│                                         │
│  [Reset]  [Status]  [Test]  [Clear]    │
├─────────────────────────────────────────┤
│  Alert History:                         │
│  ┌───────────────────────────────────┐  │
│  │ [2025-12-28 10:30] EMERGENCY     │  │
│  │ [2025-12-28 10:25] RESET OK      │  │
│  │ [2025-12-28 10:20] QUALITY_ISSUE │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

#### B. CLI Monitor (`andon_cli.py`)
```
$ python andon_cli.py

Available ports:
  [0] /dev/ttyUSB0 - USB Serial

Select port: 0

Connected to /dev/ttyUSB0

ANDON> status
Response: STATUS:NORMAL

ANDON> monitor
[2025-12-28 10:30:45] ALERT:EMERGENCY
🚨 EMERGENCY ALERT! Immediate action required!

ANDON> reset
Response: STATUS:RESET_OK
```

## Communication Protocol

### Serial Configuration
- **Baud Rate**: 9600
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Flow Control**: None

### Message Format

#### Arduino → Python
```
ALERT:<alert_type>
STATUS:<current_state>
TEST:START
TEST:COMPLETE
```

#### Python → Arduino
```
STATUS\n
RESET\n
TEST\n
```

### Message Types

**Alerts** (Arduino → Python):
```
ALERT:EMERGENCY
ALERT:QUALITY_ISSUE
ALERT:MATERIAL_SHORTAGE
ALERT:MAINTENANCE_NEEDED
```

**Status Reports** (Arduino → Python):
```
STATUS:NORMAL
STATUS:EMERGENCY
STATUS:QUALITY_ISSUE
STATUS:MATERIAL_SHORTAGE
STATUS:MAINTENANCE_NEEDED
```

**Commands** (Python → Arduino):
```
RESET    - Reset system to normal state
STATUS   - Request current system status
TEST     - Run component test sequence
```

## Data Flow

### Alert Trigger Flow
```
1. Operator presses button
        │
        ▼
2. Arduino detects button press (with debounce)
        │
        ▼
3. Arduino updates internal state
        │
        ▼
4. Arduino activates LEDs/Buzzer
        │
        ▼
5. Arduino sends ALERT message via serial
        │
        ▼
6. Python receives alert
        │
        ▼
7. Python logs to history file (JSON)
        │
        ▼
8. Python updates GUI/CLI display
        │
        ▼
9. Python can send RESET command to clear
```

### Status Query Flow
```
1. User clicks "Get Status" or types "status"
        │
        ▼
2. Python sends "STATUS\n" command
        │
        ▼
3. Arduino receives command
        │
        ▼
4. Arduino sends "STATUS:<state>" response
        │
        ▼
5. Python parses response
        │
        ▼
6. Python updates display
```

## File Structure

```
ANDON-Rev-B-/
├── arduino/
│   └── ANDON_System.ino       # Main Arduino sketch
│       ├── setup()            # Initialize pins and serial
│       ├── loop()             # Main control loop
│       ├── checkButton()      # Debounced button reading
│       ├── handleButtonPress()# Process button events
│       ├── processCommand()   # Handle serial commands
│       ├── updateStateIndicators() # Update LEDs/Buzzer
│       └── testSystem()       # Component testing
│
├── python/
│   ├── andon_monitor.py       # GUI application
│   │   └── ANDONMonitor       # Main class
│   │       ├── setup_gui()    # Create interface
│   │       ├── connect()      # Serial connection
│   │       ├── read_serial()  # Receive messages
│   │       ├── send_command() # Send commands
│   │       └── handle_alert() # Process alerts
│   │
│   ├── andon_cli.py           # CLI application
│   │   └── ANDONCLIMonitor    # Main class
│   │       ├── connect()      # Serial connection
│   │       ├── monitor()      # Real-time monitoring
│   │       └── interactive_mode() # Command mode
│   │
│   ├── test_system.py         # Automated testing
│   └── requirements.txt       # Python dependencies
│
└── docs/
    ├── SETUP.md               # Installation guide
    ├── WIRING.md              # Hardware connections
    └── ARCHITECTURE.md        # This file
```

## Technical Specifications

### Arduino
- **MCU**: ATmega328P
- **Clock Speed**: 16 MHz
- **Flash Memory**: 32 KB
- **SRAM**: 2 KB
- **EEPROM**: 1 KB
- **Operating Voltage**: 5V
- **Input Voltage**: 7-12V (external power)

### Pins Used
- **Digital Pins**: 2-5 (inputs), 8-11 (outputs)
- **Analog Pins**: None
- **PWM Pins**: None (could be used for LED dimming)
- **I2C/SPI**: Available for expansion

### Power Requirements
- Arduino: ~50 mA (typical)
- LEDs: ~20 mA each × 3 = 60 mA
- Buzzer: ~30 mA
- **Total**: ~140 mA (USB powered is sufficient)

### Timing
- **Button Debounce**: 50 ms
- **Buzzer Pulse**: 500 ms on/off
- **LED Blink**: 1000 ms on/off
- **Serial Timeout**: 1 second

## Expansion Possibilities

### Hardware Expansions
- Additional button inputs
- More LED colors/indicators
- LCD display for status
- Network connectivity (Ethernet/WiFi shield)
- SD card logging
- Real-time clock module

### Software Expansions
- Web-based dashboard
- Email notifications
- SMS alerts
- Database integration (MySQL, PostgreSQL)
- REST API
- Multi-station monitoring
- Statistical analysis
- Report generation

### Integration Options
- SCADA systems
- Manufacturing execution systems (MES)
- Enterprise resource planning (ERP)
- Internet of Things (IoT) platforms
- Cloud services (AWS, Azure, Google Cloud)

## Performance Characteristics

- **Response Time**: < 100 ms from button press to alert
- **Serial Latency**: < 50 ms typical
- **Button Debounce**: 50 ms
- **Maximum Alert Rate**: ~10 per second (limited by serial bandwidth)
- **Uptime**: Continuous operation (limited by hardware reliability)

## Safety Considerations

1. **Emergency Handling**: Emergency alerts are processed with highest priority
2. **Visual Confirmation**: All alerts provide immediate visual feedback
3. **Audio Alert**: Emergency situations trigger buzzer
4. **Logging**: All events are logged with timestamps
5. **Reset Capability**: System can be reset remotely or via button
6. **Fail-Safe**: System defaults to NORMAL state on power-up

## Maintenance

### Regular Checks
- Button functionality
- LED operation
- Buzzer sound
- Serial connection
- Log file size

### Troubleshooting Points
- Serial communication
- Power supply
- Button debouncing
- LED brightness
- Buzzer volume

### Calibration
- Debounce timing (if needed)
- LED brightness (via resistors)
- Buzzer volume (via resistor or PWM)
