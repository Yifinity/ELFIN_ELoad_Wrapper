import customtkinter as ctk
import serial
import threading
import serial.tools.list_ports # Import to list available serial ports

class BackendManager:
    def __init__(self, main_root):
        print("Backend Initialized")
        self.main = main_root
        self.thread_running = False
        self.arduino = None  # Initialize to None, will be set when a port is selected
        self.connected = False
        self.reading_thread = None
        self.latest_message = None
        self.port_name = None # To store the currently selected port name

        self.connection_callback = None
        self.plot_callback = None 

        # Array to hold various callbacks required for data processing
        self.data_callbacks = []
        self.consecutive_failed_instances = 0 # Num of consecutive failed reads
        self.historical_values = {
            "time": [],
            "L1_voltage": [],
            "L1_current": [],
            "L1_temperature": [],
            
            "L2_voltage": [],
            "L2_current": [],
            "L2_temperature": [],
            
            "L3_voltage": [],
            "L3_current": [],
            "L3_temperature": [],
        } 

        self.write_lock = threading.Lock() # Required for concurrent writes

    def set_connection_callback(self, callback):
        """Sets the callback function for connection status updates."""
        self.connection_callback = callback

    def add_data_callback(self, callback):
        """Adds a callback function to receive parsed data updates."""
        self.data_callbacks.append(callback)

    def set_plot_callback(self, callback):
        """Sets the callback function for plot data updates."""
        self.plot_callback = callback

    def list_available_ports(self):
        """
        Lists all available serial ports.
        Returns:
            list: A list of strings, where each string is the name of an available serial port.
        """
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        print(f"Available ports: {available_ports}")
        return available_ports

    def connect_to_port(self, port_name):
        """
        Attempts to establish a serial connection to the specified port.
        Args:
            port_name (str): The name of the serial port to connect to (e.g., "COM3").
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        if self.arduino and self.arduino.is_open:
            self.arduino.close() # Close existing connection if any
            self.connected = False

        try:
            self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=0.1)
            self.port_name = port_name
            self.connected = True
            print(f"Successfully connected to {port_name}")
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(True))
            return True
        except serial.SerialException as e:
            self.connected = False
            self.port_name = None
            self.arduino = None
            print(f"Failed to connect to {port_name}: {e}")
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))
            return False

    def run(self):
        """
        The main loop for reading data from the serial port.
        This runs on a separate thread.
        """
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
                    
                    # print(f'Message Read: {self.latest_message}');   
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
                    if self.consecutive_failed_instances >= 300:
                        print("Failed to read data for 5 consecutive times. Disconnecting.")
                        self.connected = False
                        if self.connection_callback:
                            self.main.after(0, lambda: self.connection_callback(False))
                        # Optionally, you might want to close the serial port here
                        # self.stop_reading_thread() # This would stop the thread entirely
                    # print("Nothing was read") # Keep this for debugging if needed

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
        if len(parsed_values) == 9:
            try:
                # Append time, ensuring it's sequential
                self.historical_values["time"].append(len(self.historical_values["time"])) 
                self.historical_values["L1_current"].append(float(parsed_values[3]))
                self.historical_values["L1_voltage"].append(float(parsed_values[6]))
                self.historical_values["L1_temperature"].append(float(parsed_values[0]))

                self.historical_values["L2_current"].append(float(parsed_values[4]))
                self.historical_values["L2_voltage"].append(float(parsed_values[7]))
                self.historical_values["L2_temperature"].append(float(parsed_values[1]))

                self.historical_values["L3_current"].append(float(parsed_values[5]))
                self.historical_values["L3_voltage"].append(float(parsed_values[8]))
                self.historical_values["L3_temperature"].append(float(parsed_values[2]))
            except ValueError as e:
                print(f"Error converting parsed values to float: {e}. Message: {parsed_values}")
        else:
            print(f"Invalid message format received. Expected 9 values, got {len(parsed_values)}. Message: {parsed_values}")


    def parse_message(self, message):
        """
        Parses a comma-separated string message into a list of values.
        Args:
            message (str): The raw string message from the serial port.
        Returns:
            list: A list of string values, or None if parsing fails.
        """
        try:
            values = message.split(',')
            return values
        except Exception as e:
            print(f"Error parsing message '{message}': {e}")
            return None

    def begin_reading_thread(self):
        """
        Starts the serial reading thread if a connection is established.
        """
        if self.arduino and self.arduino.is_open:
            if not self.thread_running: # Only start if not already running
                self.thread_running = True
                self.reading_thread = threading.Thread(target=self.run, daemon=True)
                self.reading_thread.start()
                print("Data Processing Thread Started")
                # The connection_callback is already handled in connect_to_port
                # self.main.after(0, self.connection_callback(True)) 
            else:
                print("Reading thread is already running.")
        else:
            print("Cannot start reading thread: No active serial connection.")
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))


    def stop_reading_thread(self):
        """
        Stops the serial reading thread and closes the serial connection.
        """
        self.thread_running = False
        if self.reading_thread and self.reading_thread.is_alive():
            self.reading_thread.join(timeout=1) # Waits for thread to finish
            if self.reading_thread.is_alive():
                print("Warning: Reading thread did not terminate gracefully.")

        # Now close the arduino
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Serial Connection Closed")
            self.connected = False
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))
        else:
            print("No active serial connection to close.")
            
        print("Serial Reading Thread Stopped") 

    def send_command(self, command):
        """
        Sends a command string to the connected serial port.
        Args:
            command (str): The command string to send.
        """
        if self.arduino and self.arduino.is_open:
            with self.write_lock:
                try:
                    self.arduino.write(command.encode('utf-8'))
                    print(f"Command Sent: {command}")
                except serial.SerialException as e:
                    print(f"Command ERROR sending '{command}': {e}")         
        else:
            print("Comms Failed: No active serial connection to send command.")

