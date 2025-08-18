import customtkinter as ctk
import serial
import threading
import serial.tools.list_ports # Import to list available serial ports
import json # Import for JSON operations
import os   # Import for path operations

class BackendManager:
    def __init__(self, main_root):
        print("Backend Initialized")
        self.main = main_root

        # Connection and threading variables
        self.thread_running = False
        self.arduino = None  # Initialize to None, will be set when a port is selected
        self.connected = False
        self.reading_thread = None
        self.latest_message = None
        self.port_name = None # To store the currently selected port name
        self.consecutive_failed_instances = 0 # Num of consecutive failed reads
        self.write_lock = threading.Lock() # Required for concurrent writes


        # Prob not needed
        self.connection_callback = None
        self.plot_callback = None 
        self.data_callbacks = []
        self.history_file_path = "app_history.json" # Define a file path for history
        
        # Initialize historical_values as empty lists for a fresh start every run
        self.historical_values = {
            "time": [],
            "L1_voltage": [],
            "L1_current": [],
            "L1_temperature": [],
            "L1_thermistor": [],

            "L2_voltage": [],
            "L2_current": [],
            "L2_temperature": [],
            "L2_thermistor": [],

            "L3_voltage": [],
            "L3_current": [],
            "L3_temperature": [],
            "L3_thermistor": [],
        }


    def set_connection_callback(self, callback):
        self.connection_callback = callback

    def add_data_callback(self, callback):
        self.data_callbacks.append(callback)

    def set_plot_callback(self, callback):
        self.plot_callback = callback

    def list_available_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        print(f"Available ports: {available_ports}")
        return available_ports

    def connect_to_port(self, port_name):
        if self.arduino and self.arduino.is_open:
            self.arduino.close() # Close existing connection if any
            self.connected = False

        try:
            self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=0.1)
            self.port_name = port_name
            self.connected = True
            print(f"Successfully connected to {port_name}")

            # Publish connected event to CSV, Table, and Plot
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(True))
            return True
        except serial.SerialException as e:
            self.connected = False
            self.port_name = None
            self.arduino = None
            print(f"Failed to connect to {port_name}: {e}")

            # Publish disconnected event to CSV, Table, and Plot
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))
            return False

    def run(self):
        while self.thread_running:
            if not self.connected or not self.arduino or not self.arduino.is_open:
                # If not connected or arduino object is not ready, wait a bit and continue
                if self.connection_callback:
                    self.main.after(0, lambda: self.connection_callback(False))
                self.main.after(100, lambda: None) # Small delay to prevent busy-waiting
                continue

            try:
                self.input_msg = self.arduino.readline() 
                
                if self.input_msg:
                    self.connected = True
                    self.consecutive_failed_instances = 0 # Reset the failed instances
                    self.latest_message = self.input_msg.decode('utf-8', errors='replace').strip()
                    
                    self.parsed_values = self.parse_message(self.latest_message)
                    if self.parsed_values is None:
                        continue

                    self.update_history(self.parsed_values)
                    if self.plot_callback:
                        self.main.after(0, lambda: self.plot_callback(self.historical_values))

                    for data_callback in self.data_callbacks:
                        self.main.after(0, lambda: data_callback(self.parsed_values))
                    
                else:
                    self.consecutive_failed_instances += 1
                    # Increased threshold for consecutive failed instances for robustness
                    if self.consecutive_failed_instances >= 5000: # Approx 500 seconds at 100ms delay
                        print("Failed to read data for 5000 consecutive times. Disconnecting.")
                        self.connected = False
                        if self.connection_callback:
                            self.main.after(0, lambda: self.connection_callback(False))
                        self.stop_reading_thread() # Stop the thread entirely on prolonged failure
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")
                self.connected = False
                if self.connection_callback:
                    self.main.after(0, lambda: self.connection_callback(False))
                self.stop_reading_thread() # Stop the thread on critical error
            except Exception as e:
                print(f"An unexpected error occurred in run loop: {e}")
                self.connected = False
                if self.connection_callback:
                    self.main.after(0, lambda: self.connection_callback(False))
                self.stop_reading_thread()


    def update_history(self, parsed_values):
        """Updates the historical data dictionary with new parsed values."""
        if len(parsed_values) == 12:
            try:
                # Append time, ensuring it's sequential
                self.historical_values["time"].append(len(self.historical_values["time"])) 
                self.historical_values["L1_current"].append(float(parsed_values[3]))
                self.historical_values["L1_voltage"].append(float(parsed_values[6]))
                self.historical_values["L1_temperature"].append(float(parsed_values[0]))
                self.historical_values["L1_thermistor"].append(float(parsed_values[9]))


                self.historical_values["L2_current"].append(float(parsed_values[4]))
                self.historical_values["L2_voltage"].append(float(parsed_values[7]))
                self.historical_values["L2_temperature"].append(float(parsed_values[1]))
                self.historical_values["L2_thermistor"].append(float(parsed_values[10]))

                self.historical_values["L3_current"].append(float(parsed_values[5]))
                self.historical_values["L3_voltage"].append(float(parsed_values[8]))
                self.historical_values["L3_temperature"].append(float(parsed_values[2]))
                self.historical_values["L3_thermistor"].append(float(parsed_values[11]))

            except ValueError as e:
                print(f"Error converting parsed values to float: {e}. Message: {parsed_values}")
        else:
            print(f"Invalid message format received. Expected 12 values, got {len(parsed_values)}. Message: {parsed_values}")



