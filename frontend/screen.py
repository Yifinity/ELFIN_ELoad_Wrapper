from backend.serial_backend import SerialManager
from backend.csv_manager import CSVManager


class Screen:
    def __init__(self):
        # Publishers
        self.serial_manager = SerialManager() # Manages serial connection and data reading
        self.controls_manager = ControlsManager() # Manages test parameters and commands

        # Subscribers
        self.csv_manager = CSVManager()
        self.table_manager = TableManager()
        self.plot_manager = PlotManager()   

        # Subscribe to publishers
        self.serial_manager.subscribe(self.csv_manager)
        self.serial_manager.subscribe(self.table_manager)
        self.serial_manager.subscribe(self.plot_manager)
        
        self.controls_manager.subscribe(self.csv_manager)
        self.controls_manager.subscribe(self.table_manager)
        self.controls_manager.subscribe(self.plot_manager)