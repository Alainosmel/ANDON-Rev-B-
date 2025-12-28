"""
ANDON System - Command Line Monitor

Simple command-line interface for the ANDON system.
Useful for testing and headless operation.
"""

import serial
import serial.tools.list_ports
import sys
import time
from datetime import datetime


class ANDONCLIMonitor:
    def __init__(self, port=None, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_port = None
        self.running = False
        
    def list_ports(self):
        """List available serial ports"""
        ports = serial.tools.list_ports.comports()
        print("\nAvailable ports:")
        for i, port in enumerate(ports):
            print(f"  [{i}] {port.device} - {port.description}")
        return [port.device for port in ports]
        
    def connect(self, port=None):
        """Connect to Arduino"""
        if port:
            self.port = port
            
        if not self.port:
            ports = self.list_ports()
            if not ports:
                print("ERROR: No serial ports found")
                return False
            try:
                idx = int(input("\nSelect port number: "))
                self.port = ports[idx]
            except (ValueError, IndexError):
                print("ERROR: Invalid selection")
                return False
                
        try:
            print(f"\nConnecting to {self.port}...")
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino reset
            print("Connected successfully!")
            return True
        except Exception as e:
            print(f"ERROR: Connection failed - {e}")
            return False
            
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None
            print("Disconnected")
            
    def send_command(self, command):
        """Send command to Arduino"""
        if not self.serial_port:
            print("ERROR: Not connected")
            return False
            
        try:
            self.serial_port.write(f"{command}\n".encode('utf-8'))
            print(f"Sent: {command}")
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"ERROR: Send failed - {e}")
            return False
            
    def read_response(self, timeout=2):
        """Read response from Arduino"""
        if not self.serial_port:
            return None
            
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.serial_port.in_waiting:
                try:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if line:
                        return line
                except Exception as e:
                    print(f"ERROR: Read failed - {e}")
            time.sleep(0.1)
        return None
        
    def monitor(self):
        """Monitor ANDON system in real-time"""
        if not self.serial_port:
            print("ERROR: Not connected")
            return
            
        print("\n=== ANDON System Monitor ===")
        print("Press Ctrl+C to stop monitoring\n")
        
        self.running = True
        try:
            while self.running:
                if self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if line:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{timestamp}] {line}")
                        
                        # Handle alerts
                        if line.startswith("ALERT:"):
                            alert_type = line.split(":")[1]
                            self.handle_alert(alert_type)
                            
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped")
            self.running = False
            
    def handle_alert(self, alert_type):
        """Handle alert notification"""
        alert_messages = {
            "EMERGENCY": "🚨 EMERGENCY ALERT! Immediate action required!",
            "QUALITY_ISSUE": "⚠️  Quality Issue detected",
            "MATERIAL_SHORTAGE": "📦 Material Shortage",
            "MAINTENANCE_NEEDED": "🔧 Maintenance Required"
        }
        message = alert_messages.get(alert_type, f"Alert: {alert_type}")
        print(f"\n{'='*50}")
        print(f"  {message}")
        print(f"{'='*50}\n")
        
    def interactive_mode(self):
        """Interactive command mode"""
        print("\n=== ANDON Interactive Mode ===")
        print("Commands:")
        print("  status  - Get system status")
        print("  reset   - Reset system to normal")
        print("  test    - Test system components")
        print("  monitor - Start monitoring mode")
        print("  quit    - Exit program")
        print()
        
        while True:
            try:
                cmd = input("ANDON> ").strip().lower()
                
                if cmd == "quit" or cmd == "exit":
                    break
                elif cmd == "status":
                    self.send_command("STATUS")
                    response = self.read_response()
                    if response:
                        print(f"Response: {response}")
                elif cmd == "reset":
                    self.send_command("RESET")
                    response = self.read_response()
                    if response:
                        print(f"Response: {response}")
                elif cmd == "test":
                    self.send_command("TEST")
                    print("Running system test...")
                    for _ in range(5):
                        response = self.read_response()
                        if response:
                            print(f"Response: {response}")
                elif cmd == "monitor":
                    self.monitor()
                elif cmd == "help":
                    print("Commands: status, reset, test, monitor, quit")
                elif cmd:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                print("\n")
                break
            except Exception as e:
                print(f"ERROR: {e}")


def main():
    print("=" * 50)
    print("  ANDON System - Command Line Monitor")
    print("=" * 50)
    
    monitor = ANDONCLIMonitor()
    
    # Check for command line port argument
    if len(sys.argv) > 1:
        port = sys.argv[1]
        if monitor.connect(port):
            monitor.interactive_mode()
    else:
        if monitor.connect():
            monitor.interactive_mode()
            
    monitor.disconnect()
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
