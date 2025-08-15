import json # Import for JSON operations

class CSVManager:
    def __init__(self):
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

    # To-do 
    def save_history_to_file(self):
        if not self.historical_values or not self.historical_values.get("time"):
            print("No data to save to history file.")
            return

        try:
            with open(self.history_file_path, 'w') as f: # 'w' mode correctly overwrites
                json.dump(self.historical_values, f, indent=4)
            print(f"Historical data saved to {self.history_file_path}")
        except Exception as e:
            print(f"Error saving history to file: {e}")

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

