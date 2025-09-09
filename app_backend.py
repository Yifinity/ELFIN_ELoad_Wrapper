import serial
import threading
import serial.tools.list_ports


class app_backend:
    def __init__(self, app_state):
        self.app_state = app_state
        self.arduino = None  # Initialize to None, will be set when a port is selected
        self.connected = False
        self.reading_thread = None
        self.port_name = None # To store the currently selected port name
        self.baud_rate = 115200
        self.thread_running = False
        self.parsed_values = None
        self.consecutive_failed_instances = 0 

        self.serial_lock = threading.Lock()
        self.begin_reading_thread() # Start the reading thread immediately
        print("Serial Thread Initialized")
     
    def begin_reading_thread(self):
        if not self.thread_running: # Only start if not already running
            self.thread_running = True
            self.reading_thread = threading.Thread(target=self.serial_thread, daemon=True)
            self.reading_thread.start()
            print("Data Processing Thread Started")
        else:
            print("Reading thread is already running.")


    def serial_thread(self):
        while self.thread_running:
            # print(f"Connected: {self.app_state.serial_connected} | Available Ports: {self.app_state.available_ports}")
            with self.app_state.lock:
                self.app_state.serial_connected = self.connected
                self.app_state.available_ports = self.list_serial_ports()
                # self.update_state_data()
            if(self.connected):
                try:
                    self.input_msg = self.arduino.readline() 
                    
                    if self.input_msg:
                        self.connected = True
                        self.consecutive_failed_instances = 0 # Reset the failed instances
                        self.latest_message = self.input_msg.decode('utf-8', errors='replace').strip()
                        
                        self.parsed_values = self.parse_message(self.latest_message)
                        if self.parsed_values is None:
                            continue    
                        self.update_state_data()

                    else:
                        self.consecutive_failed_instances += 1
                        # Increased threshold for consecutive failed instances for robustness
                        if self.consecutive_failed_instances >= 5000: # Approx 500 seconds at 100ms delay
                            print("Failed to read data for 5000 consecutive times. Disconnecting.")
                            self.connected = False
                            self.disconnect() # Stop the thread entirely on prolonged failure
                except serial.SerialException as e:
                    print(f"Serial communication error: {e}")
                    self.connected = False
                    self.disconnect() # Stop the thread on critical error
                except Exception as e:
                    print(f"An unexpected error occurred in run loop: {e}")
                    self.connected = False
                    self.disconnect()

            # print("About to wait for commands")
            with self.app_state.lock:
                if self.app_state.command:
                    if len(self.app_state.command) != 2:
                        print("Invalid Length - nothing done")
                        self.app_state.command = None
                        continue

                    if self.app_state.command[0] == "CONNECT":
                        print(f"CONNECT to {self.app_state.command[1]}")
                        self.connect_to_port(self.app_state.command[1])
                    elif self.app_state.command[0] == "DISCONNECT":
                        self.disconnect()
                    elif self.app_state.command[0] == "LIST":
                        print("LIST PORT called")
                        self.app_state.available_ports = self.list_serial_ports()
                    elif self.app_state.command[0] == "SEND":
                        self.send_command(self.app_state.command[1])
                    else:
                        print("Invalid Command")
                    self.app_state.command = None

    def update_state_data(self):
        # print(f"Parsed Values: {self.parsed_values}")
        if self.parsed_values:
            # Todo: Fix time
            self.app_state.latest_data["time"].append(len(self.app_state.latest_data["time"])) 
            self.app_state.latest_data["L1_current"].append(float(self.parsed_values[3]))
            self.app_state.latest_data["L1_voltage"].append(float(self.parsed_values[6]))
            self.app_state.latest_data["L1_temperature"].append(float(self.parsed_values[0]))
            self.app_state.latest_data["L1_thermistor"].append(float(self.parsed_values[9]))


            self.app_state.latest_data["L2_current"].append(float(self.parsed_values[4]))
            self.app_state.latest_data["L2_voltage"].append(float(self.parsed_values[7]))
            self.app_state.latest_data["L2_temperature"].append(float(self.parsed_values[1]))
            self.app_state.latest_data["L2_thermistor"].append(float(self.parsed_values[10]))

            self.app_state.latest_data["L3_current"].append(float(self.parsed_values[5]))
            self.app_state.latest_data["L3_voltage"].append(float(self.parsed_values[8]))
            self.app_state.latest_data["L3_temperature"].append(float(self.parsed_values[2]))
            self.app_state.latest_data["L3_thermistor"].append(float(self.parsed_values[11]))
            # self.app_state.latest_data[key].append(value)
        else:
            print("No parsed values to update state data.")
    
    def disconnect(self):
        if self.arduino and self.arduino.is_open:
            self.send_command("-1") # Disconnect indication
            self.arduino.close()
            print("Serial Connection Closed")
            self.connected = False
        else:
            print("No active serial connection to close.")


    def stop_reading_thread(self):
        self.thread_running = False
        if self.reading_thread and self.reading_thread.is_alive():
            self.reading_thread.join(timeout=1) # Waits for thread to finish
            if self.reading_thread.is_alive():
                print("Warning: Reading thread did not terminate gracefully.")
            self.disconnect()
        print("Serial Reading Thread Stopped") 

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect_to_port(self, port_name):
        if self.arduino and self.arduino.is_open:
            print("Already connected to a port. Disconnecting first.")
            self.arduino.close() # Close existing connection if any
        try:
            print(f"Attempting to connect to {port_name}...")
            self.arduino = serial.Serial(port=port_name, baudrate=self.baud_rate, timeout=0.1)
            self.port_name = port_name
            self.connected = True
            # print(f"Successfully connected to {port_name}")
            return True
        except serial.SerialException as e:
            self.connected = False
            self.port_name = None
            self.arduino = None
            print(f"Failed to connect to {port_name}: {e}")
            return False

    def send_command(self, command):
        if self.arduino and self.arduino.is_open:
            with self.serial_lock:
                try:
                    self.arduino.write(command.encode('utf-8'))
                    print(f"Command Sent: {command}")
                except serial.SerialException as e:
                    print(f"Command ERROR sending '{command}': {e}")         
        else:
            print("Comms Failed: No active serial connection to send command.")

    def parse_message(self, message):
        try:
            values = message.split(',')
            return values
        except Exception as e:
            print(f"Error parsing message '{message}': {e}")
            return None