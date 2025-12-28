"""
ANDON System - Python Monitor Application

This application provides a GUI interface to monitor and control
the Arduino-based ANDON system.

Features:
- Real-time monitoring of ANDON alerts
- Visual indicators for different alert types
- Alert history logging
- System control commands
- Serial communication with Arduino
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
import json
import os


class ANDONMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("ANDON System Monitor")
        self.root.geometry("800x600")
        
        self.serial_port = None
        self.is_running = False
        self.current_status = "DISCONNECTED"
        
        self.alert_history = []
        self.log_file = "andon_log.json"
        
        self.setup_gui()
        self.load_history()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Connection", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, padx=5)
        self.port_combo = ttk.Combobox(conn_frame, width=20)
        self.port_combo.grid(row=0, column=1, padx=5)
        self.refresh_ports()
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=2, padx=5)
        
        ttk.Button(conn_frame, text="Refresh Ports", command=self.refresh_ports).grid(row=0, column=3, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        self.status_label = tk.Label(status_frame, text="DISCONNECTED", 
                                     font=("Arial", 24, "bold"),
                                     bg="gray", fg="white",
                                     width=20, height=3)
        self.status_label.pack(pady=10)
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=5)
        
        ttk.Button(control_frame, text="Reset System", 
                  command=self.reset_system).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Get Status", 
                  command=self.get_status).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Test System", 
                  command=self.test_system).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Clear History", 
                  command=self.clear_history).pack(fill=tk.X, pady=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Alert History", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=90)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
    def refresh_ports(self):
        """Refresh available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
            
    def toggle_connection(self):
        """Connect or disconnect from Arduino"""
        if not self.is_running:
            self.connect()
        else:
            self.disconnect()
            
    def connect(self):
        """Connect to Arduino"""
        try:
            port = self.port_combo.get()
            if not port:
                self.log_message("ERROR: No port selected")
                return
                
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            
            self.is_running = True
            self.connect_btn.config(text="Disconnect")
            self.log_message(f"Connected to {port}")
            
            # Start reading thread
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
        except Exception as e:
            self.log_message(f"ERROR: Connection failed - {str(e)}")
            
    def disconnect(self):
        """Disconnect from Arduino"""
        self.is_running = False
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None
        self.connect_btn.config(text="Connect")
        self.update_status("DISCONNECTED", "gray")
        self.log_message("Disconnected")
        
    def read_serial(self):
        """Read data from Arduino in separate thread"""
        while self.is_running:
            try:
                if self.serial_port and self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if line:
                        self.process_message(line)
            except Exception as e:
                self.log_message(f"ERROR: Read failed - {str(e)}")
                self.is_running = False
            time.sleep(0.1)
            
    def process_message(self, message):
        """Process messages from Arduino"""
        self.log_message(f"Arduino: {message}")
        
        if message.startswith("ALERT:"):
            alert_type = message.split(":")[1]
            self.handle_alert(alert_type)
        elif message.startswith("STATUS:"):
            status = message.split(":")[1]
            self.update_status_from_arduino(status)
            
    def handle_alert(self, alert_type):
        """Handle incoming alerts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert = {
            "timestamp": timestamp,
            "type": alert_type,
            "status": "ACTIVE"
        }
        self.alert_history.append(alert)
        self.save_history()
        
        # Update status display
        self.update_status(alert_type, self.get_color_for_alert(alert_type))
        
    def get_color_for_alert(self, alert_type):
        """Get color based on alert type"""
        colors = {
            "EMERGENCY": "red",
            "QUALITY_ISSUE": "orange",
            "MATERIAL_SHORTAGE": "yellow",
            "MAINTENANCE_NEEDED": "orange",
            "NORMAL": "green"
        }
        return colors.get(alert_type, "gray")
        
    def update_status(self, status, color):
        """Update status display"""
        self.current_status = status
        self.status_label.config(text=status, bg=color)
        
    def update_status_from_arduino(self, status):
        """Update status based on Arduino response"""
        color = self.get_color_for_alert(status)
        self.update_status(status, color)
        
    def send_command(self, command):
        """Send command to Arduino"""
        if self.serial_port and self.is_running:
            try:
                self.serial_port.write(f"{command}\n".encode('utf-8'))
                self.log_message(f"Sent: {command}")
            except Exception as e:
                self.log_message(f"ERROR: Send failed - {str(e)}")
        else:
            self.log_message("ERROR: Not connected")
            
    def reset_system(self):
        """Reset the ANDON system"""
        self.send_command("RESET")
        
    def get_status(self):
        """Get current system status"""
        self.send_command("STATUS")
        
    def test_system(self):
        """Test system components"""
        self.send_command("TEST")
        
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def save_history(self):
        """Save alert history to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.alert_history, f, indent=2)
        except Exception as e:
            self.log_message(f"ERROR: Failed to save history - {str(e)}")
            
    def load_history(self):
        """Load alert history from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    self.alert_history = json.load(f)
                self.log_message(f"Loaded {len(self.alert_history)} historical alerts")
        except Exception as e:
            self.log_message(f"WARNING: Failed to load history - {str(e)}")
            
    def clear_history(self):
        """Clear alert history"""
        self.alert_history = []
        self.save_history()
        self.log_message("History cleared")


def main():
    root = tk.Tk()
    app = ANDONMonitor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
