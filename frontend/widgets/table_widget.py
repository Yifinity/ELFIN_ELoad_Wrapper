import customtkinter as ctk

class table_widget(ctk.CTkFrame):
    # class handling the current display of the three programmable loads
    def __init__(self, master, app_state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app_state = app_state
        self.connected = False
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Make rows expand equally
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Make all columns expand equally
        
        self.data_load_label = ctk.CTkLabel(self, text="Load: ", 
            corner_radius=5, 
            text_color="white", 
            font=ctk.CTkFont(weight="bold"))
        self.data_load_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.data_voltage_label = ctk.CTkLabel(self, text="Voltage:", text_color="white")
        self.data_voltage_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.data_current_label = ctk.CTkLabel(self, text="Current: ", text_color="white")
        self.data_current_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.data_temp_label = ctk.CTkLabel(self, text="Temperature:", text_color="white")
        self.data_temp_label.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.load1_thermistor = ctk.CTkLabel(self, text="Setting:", text_color="white")
        self.load1_thermistor.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        self.data_load1 = ctk.CTkLabel(self, text="Load 1: ", 
            corner_radius=5, 
            text_color="white",
            font=ctk.CTkFont(weight="bold"))
        self.data_load1.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_voltage = ctk.CTkLabel(self, text="0V", text_color="grey")
        self.load1_voltage.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_current = ctk.CTkLabel(self, text="0A", text_color="grey")
        self.load1_current.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_temperature = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load1_temperature.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_thermistor = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load1_thermistor.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")
        self.data_load2 = ctk.CTkLabel(self, text="Load 2: ", 
            corner_radius=5, 
            text_color="white",
            font=ctk.CTkFont(weight="bold"))
        self.data_load2.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_voltage = ctk.CTkLabel(self, text="0V", text_color="grey")
        self.load2_voltage.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_current = ctk.CTkLabel(self, text="0A", text_color="grey")
        self.load2_current.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_temperature = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load2_temperature.grid(row=3, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_thermistor = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load2_thermistor.grid(row=4, column=2, padx=10, pady=5, sticky="nsew")

        self.data_load3 = ctk.CTkLabel(self, text="Load 3: ", 
            corner_radius=5, 
            text_color="white",
            font=ctk.CTkFont(weight="bold"))
        self.data_load3.grid(row=0, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_voltage = ctk.CTkLabel(self, text="0V", text_color="grey")
        self.load3_voltage.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_current = ctk.CTkLabel(self, text="0A", text_color="grey")
        self.load3_current.grid(row=2, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_temperature = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load3_temperature.grid(row=3, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_thermistor = ctk.CTkLabel(self, text="0°C", text_color="grey")
        self.load3_thermistor.grid(row=4, column=3, padx=10, pady=5, sticky="nsew")
        # self.configure(fg_color="red")
        print("Data Table Widget Initialized")
        self.update_period = 1000
        self.update_status()



    def update_status(self):
        if self.app_state.serial_connected:
            self.connected = True
            if len(self.app_state.latest_data) == 13:
                if(len(self.app_state.latest_data['L1_voltage']) != 0):
                    self.load1_voltage.configure(text=f"{self.app_state.latest_data['L1_voltage'][-1]}V")
                    self.load1_current.configure(text=f"{self.app_state.latest_data['L1_current'][-1]}A")
                    self.load1_temperature.configure(text=f"{self.app_state.latest_data['L1_temperature'][-1]}°C")
                    self.load1_thermistor.configure(text=f"{self.app_state.latest_data['L1_thermistor'][-1]}°C")
                                
                    self.load2_voltage.configure(text=f"{self.app_state.latest_data['L2_voltage'][-1]}V")
                    self.load2_current.configure(text=f"{self.app_state.latest_data['L2_current'][-1]}A")
                    self.load2_temperature.configure(text=f"{self.app_state.latest_data['L2_temperature'][-1]}°C")
                    self.load2_thermistor.configure(text=f"{self.app_state.latest_data['L2_thermistor'][-1]}°C")
                                
                    self.load3_voltage.configure(text=f"{self.app_state.latest_data['L3_voltage'][-1]}V")
                    self.load3_current.configure(text=f"{self.app_state.latest_data['L3_current'][-1]}A")
                    self.load3_temperature.configure(text=f"{self.app_state.latest_data['L3_temperature'][-1]}°C")
                    self.load3_thermistor.configure(text=f"{self.app_state.latest_data['L3_thermistor'][-1]}°C")

                    # Set all value labels to white when connected
                    self.load1_voltage.configure(text_color="white")
                    self.load1_current.configure(text_color="white")
                    self.load1_temperature.configure(text_color="white")
                    self.load1_thermistor.configure(text_color="white")
                    self.load2_voltage.configure(text_color="white")
                    self.load2_current.configure(text_color="white")
                    self.load2_temperature.configure(text_color="white")
                    self.load2_thermistor.configure(text_color="white")
                    self.load3_voltage.configure(text_color="white")
                    self.load3_current.configure(text_color="white")
                    self.load3_temperature.configure(text_color="white")
                    self.load3_thermistor.configure(text_color="white")

            else:
                print("Invalid message format received.")   
        else:
            self.load1_voltage.configure(text_color="grey")
            self.load1_current.configure(text_color="grey")
            self.load1_temperature.configure(text_color="grey")
            self.load1_thermistor.configure(text_color="grey")
            self.load2_voltage.configure(text_color="grey")
            self.load2_current.configure(text_color="grey")
            self.load2_temperature.configure(text_color="grey")
            self.load2_thermistor.configure(text_color="grey")
            self.load3_voltage.configure(text_color="grey")
            self.load3_current.configure(text_color="grey")
            self.load3_temperature.configure(text_color="grey")
            self.load3_thermistor.configure(text_color="grey")
        
        if not self.app_state.serial_connected and self.connected:
            self.connected = False
            self.load1_voltage.configure(text="0V")
            self.load1_current.configure(text="0A")
            self.load1_temperature.configure(text="0°C")
            self.load1_thermistor.configure(text="0°C")
                        
            self.load2_voltage.configure(text="0V")
            self.load2_current.configure(text="0A")
            self.load2_temperature.configure(text="0°C")
            self.load2_thermistor.configure(text="0°C")
                        
            self.load3_voltage.configure(text="0V")
            self.load3_current.configure(text="0A")
            self.load3_temperature.configure(text="0°C")
            self.load3_thermistor.configure(text="0°C")

        self.after(self.update_period, self.update_status)