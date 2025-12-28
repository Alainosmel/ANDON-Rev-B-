"""
ANDON System - Test Script

Simple script to test the ANDON system functionality
"""

import serial
import serial.tools.list_ports
import time


def find_arduino():
    """Automatically find Arduino port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Common Arduino identifiers
        if 'Arduino' in port.description or 'CH340' in port.description or 'USB Serial' in port.description:
            return port.device
    return None


def test_andon_system():
    """Run automated tests on ANDON system"""
    print("=" * 60)
    print("ANDON System Automated Test")
    print("=" * 60)
    
    # Find Arduino
    print("\n[1/5] Searching for Arduino...")
    port = find_arduino()
    
    if not port:
        print("❌ No Arduino found. Listing all ports:")
        ports = serial.tools.list_ports.comports()
        for p in ports:
            print(f"  - {p.device}: {p.description}")
        return False
    
    print(f"✅ Found Arduino on {port}")
    
    # Connect
    print("\n[2/5] Connecting to Arduino...")
    try:
        ser = serial.Serial(port, 9600, timeout=2)
        time.sleep(2)  # Wait for Arduino reset
        print("✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Check for ready message
    print("\n[3/5] Waiting for ready message...")
    time.sleep(1)
    if ser.in_waiting:
        msg = ser.readline().decode('utf-8').strip()
        print(f"✅ Received: {msg}")
    else:
        print("⚠️  No initial message (this is okay)")
    
    # Test STATUS command
    print("\n[4/5] Testing STATUS command...")
    ser.write(b"STATUS\n")
    time.sleep(1)
    
    if ser.in_waiting:
        response = ser.readline().decode('utf-8').strip()
        print(f"✅ Response: {response}")
        if response.startswith("STATUS:"):
            print("✅ STATUS command working correctly")
        else:
            print("⚠️  Unexpected response format")
    else:
        print("❌ No response to STATUS command")
    
    # Test RESET command
    print("\n[5/5] Testing RESET command...")
    ser.write(b"RESET\n")
    time.sleep(1)
    
    if ser.in_waiting:
        response = ser.readline().decode('utf-8').strip()
        print(f"✅ Response: {response}")
        if "RESET" in response:
            print("✅ RESET command working correctly")
        else:
            print("⚠️  Unexpected response format")
    else:
        print("❌ No response to RESET command")
    
    # Run system test
    print("\n[BONUS] Running system test...")
    ser.write(b"TEST\n")
    print("Watch for LED sequence and buzzer sound...")
    
    for i in range(10):  # Read test responses
        time.sleep(0.5)
        if ser.in_waiting:
            response = ser.readline().decode('utf-8').strip()
            print(f"  {response}")
    
    # Cleanup
    ser.close()
    
    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Try pressing buttons on Arduino")
    print("  2. Run Python monitor: python andon_monitor.py")
    print("  3. Run Python CLI: python andon_cli.py")
    
    return True


if __name__ == "__main__":
    try:
        test_andon_system()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
