import customtkinter as ctk
import serial
import threading


class BackendManager:
    def __init__(self, main_root):
        print("Backend Initialized")
        self.main = main_root
        self.thread_running = False
        self.arduino = serial.Serial(port = "COM24", baudrate=115200,
                                    timeout=0.1)
        self.connected = False;
        self.reading_thread = None
        self.latest_message = None

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
        self.connection_callback = callback

    def add_data_callback(self, callback):
        self.data_callbacks.append(callback)

    def set_plot_callback(self, callback):
        self.plot_callback = callback

    # Process that runs when the backend begins on the secondary thread. 
    def run(self):
        while(self.thread_running):
            if(self.connected):
                self.main.after(0, self.connection_callback(True))
            else:
                self.main.after(0, self.connection_callback(False))
            self.input_msg = self.arduino.readline() 
         
            if(self.input_msg):
                self.connected = True
                self.consecutive_failed_instances = 0 # Reset the failed instances
                self.latest_message = self.input_msg.decode('utf-8',
                                                             errors='replace'
                                                             ).strip()
               
                # print(f'Message Read: {self.latest_message}');   
                self.parsed_values = self.parse_message(self.latest_message)
                if self.parsed_values is None:
                    continue

                self.update_history(self.parsed_values)
                self.main.after(0, self.plot_callback(self.historical_values))


                for data_callback in self.data_callbacks:
                    self.main.after(0, data_callback(self.parsed_values))
                
            else:
                self.consecutive_failed_instances += 1
                if(self.consecutive_failed_instances >= 5):
                    print("Failed to read data for 5 consecutive times.")
                    # self.main.after(0, self.data_callback("Disconnected"))
                    self.connected = False
                print("Nothing was read")

    def update_history(self, parsed_values):
        if(len(parsed_values) == 9):
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
        else:
            print("Invalid message format received.")


    def parse_message(self, message):
        try:
            values = message.split(',')
            return values
        except Exception as e:
            return None

    # Initalize the thread for us to begin reading from the Serial monitor. 
    def begin_reading_thread(self):
        self.thread_running = True
        self.reading_thread = threading.Thread(target=self.run, daemon = True)
        self.reading_thread.start()
        print("Data Processing Thread Started")
        self.main.after(0, self.connection_callback(True))

    def stop_reading_thread(self):
        if(self.reading_thread.is_alive()):
            self.reading_thread.join(timeout=1) # waits for thread ot finish

        # No=w close the arduino
        if(self.arduino.is_open):
            self.arduino.close()
            print("Serial Connection Closed")

        self.thread_running = False
        print("Serial Reading Thread Stopped")        

    def send_command(self, command):
        if self.arduino.is_open:
            with self.write_lock:
                try:
                    self.arduino.write(command.encode('utf-8'))
                    print(f"Command Sent: {command}")
                except serial.SerialException as e:
                    print(f"Command ERROR: {command}")            
        else:
            print("Comms Failed")