# import customtkinter as ctk
import threading
# import json # Import for JSON operations

from backend.serial_manager import SerialManager
from backend.csv_manager import CSVManager
from frontend.plot_frame import PlotDisplayFrame

class BackendManager:
    def __init__(self):
        print("Backend Initialized")        
        self.thread_running = False
        self.write_lock = threading.Lock() # Required for concurrent writes
        
        self.serial_manager = SerialManager(self.write_lock)
        self.csv_manager = CSVManager()

        # Fix selected_load
        self.plot_panel_frame = PlotDisplayFrame(self, selected_load=self.selected_load)
        self.plot_panel_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
    def begin_reading_thread(self):
        if self.serial_manager.is_connected():
            if not self.thread_running: # Only start if not already running
                self.thread_running = True
                #Todo: Call run from serial_manager
                self.reading_thread = threading.Thread(target=self.run, daemon=True)
                self.reading_thread.start()
                print("Data Processing Thread Started")
            else:
                print("Reading thread is already running.")
        else:
            print("Cannot start reading thread: No active serial connection.")
            if self.connection_callback:
                self.main.after(0, lambda: self.connection_callback(False))

    def stop_reading_thread(self):
        self.thread_running = False
        if self.reading_thread and self.reading_thread.is_alive():
            self.reading_thread.join(timeout=1) # Waits for thread to finish
            if self.reading_thread.is_alive():
                print("Warning: Reading thread did not terminate gracefully.")

        # Save history before closing
        self.save_history_to_file()
        
        # Now close the arduino
        self.serial_manager.close_arduino()
        print("Serial Reading Thread Stopped") 


    def run(self):
        while self.thread_running:
            output = self.serial_manager.run()
            if output == -1:
                print("Connection/Arduino Error")
                self.main.after(100, lambda: None) # Small delay to prevent busy-waiting
            elif output == -2:
                print("No parsed values")
            elif output == -3:
                print("Data Read Failure for 5000 consecutive occurance")
                self.stop_reading_thread() # Stop the thread entirely on prolonged failure
            elif output == -4 or output == -5:
                self.stop_reading_thread()



    # def save_history_to_file(self):
    #     if not self.historical_values or not self.historical_values.get("time"):
    #         print("No data to save to history file.")
    #         return

    #     try:
    #         with open(self.history_file_path, 'w') as f: # 'w' mode correctly overwrites
    #             json.dump(self.historical_values, f, indent=4)
    #         print(f"Historical data saved to {self.history_file_path}")
    #     except Exception as e:
    #         print(f"Error saving history to file: {e}")
