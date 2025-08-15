import datetime
import csv


class CSVManager:
    def __init__(self):
        self.is_saving = False

    def start_csv_logging(self, load_idx):
        self.is_saving = True
        self.current_test_load = load_idx
        filename = f"test_load{load_idx}_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
        self.csv_file = open(filename, "w", newline="")
        self.csv_writer = self.csv_file
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write header
        self.csv_writer.writerow([
            "timestamp",
            "L1_temperature",
            "L2_temperature", 
            "L3_temperature", 
            "L1_current", 
            "L2_current", 
            "L3_current", 
            "L1_voltage", 
            "L2_voltage",
            "L3_voltage", 
            "L1_thermistor", 
            "L2_thermistor", 
            "L3_thermistor"
        ])

    def stop_csv_logging(self):
        self.is_saving = False
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None

    def receive(self, input):        
        # length = 12 is an event for saving to file
        if len(input) == 12 and self.is_saving:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            self.csv_writer.writerow([timestamp] + input)

        if(len(input) == 1):
            self.stop_csv_logging() # length = 1 --> end logging. 

        if(len(input) == 2): 
            self.start_csv_logging    


        
    # def update_history(self, parsed_values):
    #     """Updates the historical data dictionary with new parsed values."""
    #     if len(parsed_values) == 12:
    #         try:
    #             # Append time, ensuring it's sequential
    #             self.historical_values["time"].append(len(self.historical_values["time"])) 
    #             self.historical_values["L1_current"].append(float(parsed_values[3]))
    #             self.historical_values["L1_voltage"].append(float(parsed_values[6]))
    #             self.historical_values["L1_temperature"].append(float(parsed_values[0]))
    #             self.historical_values["L1_thermistor"].append(float(parsed_values[9]))


    #             self.historical_values["L2_current"].append(float(parsed_values[4]))
    #             self.historical_values["L2_voltage"].append(float(parsed_values[7]))
    #             self.historical_values["L2_temperature"].append(float(parsed_values[1]))
    #             self.historical_values["L2_thermistor"].append(float(parsed_values[10]))

    #             self.historical_values["L3_current"].append(float(parsed_values[5]))
    #             self.historical_values["L3_voltage"].append(float(parsed_values[8]))
    #             self.historical_values["L3_temperature"].append(float(parsed_values[2]))
    #             self.historical_values["L3_thermistor"].append(float(parsed_values[11]))

    #         except ValueError as e:
    #             print(f"Error converting parsed values to float: {e}. Message: {parsed_values}")
    #     else:
    #         print(f"Invalid message format received. Expected 12 values, got {len(parsed_values)}. Message: {parsed_values}")

