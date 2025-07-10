import pandas as pd
import os
import json
import datetime

#basically converts JSON to CSV. Unnecessary tbh but it works. 

def export_history_to_csv_standalone(history_json_path="app_history.json", output_file_name="temp.csv"):
    if not os.path.exists(history_json_path):
        print(f"Error: History file not found at '{history_json_path}'.")
        print("Please ensure your main application has run and saved data.")
        return

    try:
        with open(history_json_path, 'r') as f:
            historical_values = json.load(f)

        if not historical_values or not historical_values.get("time"):
            print("No historical data found in the JSON file to export.")
            return

        # Create a pandas DataFrame from the historical_values dictionary
        df = pd.DataFrame(historical_values)

        # Determine the desktop path dynamically
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Ensure the desktop directory exists
        os.makedirs(desktop_path, exist_ok=True)

        # Construct the full file path for the CSV
        file_path = os.path.join(desktop_path, output_file_name)

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Historical data successfully exported to: {file_path}")

    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from '{history_json_path}'. File might be corrupted: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during CSV export: {e}")

# This block ensures the function runs when the script is executed directly
if __name__ == "__main__":
    # Call the function to export the history.
    # It will look for 'app_history.json' in the same directory as this script.
    export_history_to_csv_standalone()
