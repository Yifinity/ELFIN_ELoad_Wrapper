import serial
import threading
import serial.tools.list_ports # Import to list available serial ports

class SerialManager:
    def __init__(self, ):
        # Connection variables
        self.arduino = None  
        self.connected = False
        self.consecutive_failed_instances = 0
        self.port_name = None 
        self.baudrate = 115200
        self.write_lock = threading.Lock() # Required for concurrent writes

        # Reading thread variables
        self.reading_thread = None
        self.thread_running = False
        self.latest_message = None

    def list_available_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        # print(f"Available ports: {available_ports}")
        return available_ports

    def connect_to_port(self, port_name):
        # Close existing connection if any
        if self.arduino and self.arduino.is_open:
            self.arduino.close() 
            self.connected = False

        try:
            self.arduino = serial.Serial(port=port_name, baudrate=self.baudrate, timeout=0.1)
            self.port_name = port_name
            self.connected = True

            # Publish connected event to Table and Plot
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(True))
#            print(f"Successfully connected to {port_name}")
            return True
        except serial.SerialException as e:
            self.connected = False
            self.port_name = None
            self.arduino = None

            # Publish disconnected event to CSV, Table, and Plot
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))
            # print(f"Failed to connect to {port_name}: {e}")
            return False

    def begin_reading_thread(self):
        if self.arduino and self.arduino.is_open:
            if not self.thread_running: 
                self.thread_running = True
                self.reading_thread = threading.Thread(target=self.run, daemon=True)
                self.reading_thread.start()
                print("Data Processing Thread Started")
            else:
                print("Reading thread is already running.")
        else:
            print("Cannot start reading thread: No active serial connection.")

    def stop_reading_thread(self):
        self.thread_running = False
        if self.reading_thread and self.reading_thread.is_alive():
            self.reading_thread.join(timeout=1) # Waits for thread to finish
            if self.reading_thread.is_alive():
                print("Warning: Reading thread did not terminate gracefully.")

        # Now close the arduino
        if self.arduino and self.arduino.is_open:
            self.send_command("-1") # Disconnect char
            self.arduino.close()
            self.connected = False

            # Send disconnect event
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))
            print("Serial Connection Closed")
        else:
            print("No active serial connection to close.")
        print("Serial Reading Thread Stopped") 

    def parse_message(self, message):
        try:
            values = message.split(',')
            return values
        except Exception as e:
            print(f"Error parsing message '{message}': {e}")
            return None

    # Run function that runs simultaneously with GUI main thread
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

    def send_command(self, command):
        if self.arduino and self.arduino.is_open:
            with self.write_lock:
                try:
                    self.arduino.write(command.encode('utf-8'))
                    print(f"Command Sent: {command}")
                except serial.SerialException as e:
                    print(f"Command ERROR sending '{command}': {e}")         
        else:
            print("Comms Failed: No active serial connection to send command.")

