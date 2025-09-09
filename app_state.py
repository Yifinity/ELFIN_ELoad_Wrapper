import threading

class app_state:
    def __init__(self):
        self.lock = threading.Lock()
        self.available_ports = []
        self.serial_connected = False
        self.selected_load = None
        self.test_running = [False, False, False]  
        self.latest_data = {
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

        self.command = None
        