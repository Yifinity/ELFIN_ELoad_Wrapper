import serial
import serial.tools.list_ports 
from publisher import Publisher

class SerialManager:
    def __init__(self, write_lock):
        self.write_lock = write_lock
        self.consecutive_failed_instances = 0 # Num of consecutive failed reads
        self.arduino = None
        self.port_name = None

        self.connection_publisher = Publisher() # used to manage connection events
        self.data_publisher = Publisher() # used to manage data events
    
    def is_connected(self):
        return self.arduino and self.arduino.is_open
    
    def close_arduino(self):
        if self.is_connected():
            self.send_command("-1") # Disconnect char
            self.arduino.close()
            self.connection_publisher.publish(False) 
        else:
            print("No active serial connection to close.")
 
    def list_available_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        print(f"Available ports: {available_ports}")
        return available_ports

    def connect_to_port(self, port_name):
        if self.is_connected():
            self.arduino.close() # Close existing connection if any
        try:
            self.arduino = serial.Serial(port=port_name, baudrate=115200, timeout=0.1)
            self.port_name = port_name
            print(f"Successfully connected to {port_name}")
            self.connection_publisher.publish(True)
            return True
        except serial.SerialException as e:
            self.port_name = None
            self.arduino = None
            print(f"Failed to connect to {port_name}: {e}")
            self.connection_publisher.publish(False)
            return False

    def parse_message(self, message):
        try:
            values = message.split(',')
            return values
        except Exception as e:
            print(f"Error parsing message '{message}': {e}")
            return None
        

    def run(self):
        if not self.is_connected():
            self.connection_publisher.publish(False)
            return -1

        try:
            self.input_msg = self.arduino.readline() 
            
            if self.input_msg:
                self.connected = True
                self.consecutive_failed_instances = 0 # Reset the failed instances
                self.latest_message = self.input_msg.decode('utf-8', errors='replace').strip()
                self.parsed_values = self.parse_message(self.latest_message)
                if self.parsed_values is None:
                    return -2
                self.data_publisher.publish(self.parsed_values) # 
                # -- Add publish event here (CSV, plot):
                
            else:
                self.consecutive_failed_instances += 1
                if self.consecutive_failed_instances >= 5000:
                    self.connected = False
                    # -- Add publish event here connection:
                    return -3               
                                     
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            self.connected = False
            return -4
        except Exception as e:
            print(f"An unexpected error occurred in run loop: {e}")
            self.connected = False
            return -5

    def send_command(self, command):
        if self.is_connected():
            with self.write_lock:
                try:
                    self.arduino.write(command.encode('utf-8'))
                    print(f"Command Sent: {command}")
                except serial.SerialException as e:
                    print(f"Command ERROR sending '{command}': {e}")         
        else:
            print("Comms Failed: No active serial connection to send command.")