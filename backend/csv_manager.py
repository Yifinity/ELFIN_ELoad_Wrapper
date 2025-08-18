import datetime
import csv

class CSVManager:
    def __init__(self):
        self.backend = None
        self.csv_input_length = 12
        self.csv_file = None
        self.csv_writer = None
        self.logging_active = False
        self.current_test_load = None
        
    def receive(self, message, data):
        if message == "CONNECTION":
            if data[0] == False and self.logging_active:
                self.stop_csv_logging()
        if message == "DATA" and self.logging_active:
            self.csv_data_callback(data)
        elif message == "START_CSV":
            self.start_csv_logging(data[0]) # Selected load idx

    # To-do: Add filename into function. 
    def start_csv_logging(self, load_idx):
        self.current_test_load = load_idx
        filename = f"test_load{load_idx}_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        self.csv_file = open(filename, "w", newline="")
        self.csv_writer = self.csv_file
        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow(["timestamp", "L1_temperature", "L2_temperature", "L3_temperature", "L1_current", "L2_current", "L3_current", "L1_voltage", "L2_voltage","L3_voltage", "L1_thermistor", "L2_thermistor", "L3_thermistor"])
        self.logging_active = True

    def stop_csv_logging(self):
        self.logging_active = False
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None

    # Take data from backend and write to CSV
    def csv_data_callback(self, parsed_values):
        if self.logging_active and len(parsed_values) == self.csv_input_length:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.csv_writer.writerow([timestamp] + parsed_values)     