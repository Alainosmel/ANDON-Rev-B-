# ANDON System Wiring Diagram

## Components Required

### Arduino
- 1x Arduino Uno (or compatible)
- USB cable for programming and serial communication

### Inputs (Buttons)
- 4x Push buttons (normally open)
- 4x 10kΩ resistors (optional, using internal pullups)

### Outputs (Indicators)
- 1x Red LED + 220Ω resistor (Emergency indicator)
- 1x Yellow LED + 220Ω resistor (Warning indicator)
- 1x Green LED + 220Ω resistor (Normal operation indicator)
- 1x Active buzzer (5V) or passive piezo buzzer

### Power
- Arduino can be powered via USB (during development)
- For production, use external 7-12V power supply

## Pin Connections

### Button Inputs (Active LOW with internal pullup)
```
Button 1 (Emergency)        -> Pin 2
Button 2 (Quality Issue)    -> Pin 3
Button 3 (Material Shortage)-> Pin 4
Button 4 (Maintenance)      -> Pin 5

All buttons connect between pin and GND
```

### LED Outputs (Active HIGH)
```
Red LED (Emergency)    -> Pin 8  -> 220Ω resistor -> LED -> GND
Yellow LED (Warning)   -> Pin 9  -> 220Ω resistor -> LED -> GND
Green LED (Normal)     -> Pin 10 -> 220Ω resistor -> LED -> GND
```

### Buzzer Output
```
Buzzer                 -> Pin 11 -> Buzzer (+) -> GND (-)
```

## Wiring Diagram (Text representation)

```
                    ARDUINO UNO
                   ┌──────────────┐
                   │              │
    Button 1 ──────┤ 2            │
    Button 2 ──────┤ 3            │
    Button 3 ──────┤ 4            │
    Button 4 ──────┤ 5            │
                   │              │
                   │           8  ├──────[220Ω]──── Red LED ──── GND
                   │           9  ├──────[220Ω]──── Yellow LED ─ GND
                   │          10  ├──────[220Ω]──── Green LED ── GND
                   │          11  ├──────────────── Buzzer (+) ─ GND
                   │              │
                   │     USB      ├──────────────── To Computer
                   │              │
                   │    GND       ├──────────────── Common Ground
                   │              │
                   └──────────────┘

All buttons connected between pin and GND (internal pullup enabled)
```

## Optional: External Pullup Resistors

If not using internal pullups, connect:
```
+5V ──── [10kΩ] ──── Button Pin
                  │
              Button Switch
                  │
                 GND
```

## Power Considerations

- Each LED draws approximately 10-20mA
- Buzzer draws approximately 20-30mA
- Total current draw is well within Arduino's capabilities
- For high-power indicators, use transistors or relays

## Safety Notes

1. Double-check all connections before powering on
2. Ensure correct LED polarity (long leg is positive)
3. Never connect LEDs without current-limiting resistors
4. Use appropriate gauge wire for all connections
5. Ensure good common ground between Arduino and all components
