import customtkinter as ctk

class table_widget(ctk.CTkFrame):
    # class handling the current display of the three programmable loads
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)  # Make rows expand equally
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Make all columns expand equally
        
        self.data_load_label = ctk.CTkLabel(self, text="Load: ", 
                        corner_radius=5, 
                        text_color="white")
        self.data_load_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.data_voltage_label = ctk.CTkLabel(self, text="Voltage:", text_color="white", font=ctk.CTkFont(weight="bold"))
        self.data_voltage_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.data_current_label = ctk.CTkLabel(self, text="Current: ", text_color="white", font=ctk.CTkFont(weight="bold"))
        self.data_current_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.data_temp_label = ctk.CTkLabel(self, text="Temperature:", text_color="white", font=ctk.CTkFont(weight="bold"))
        self.data_temp_label.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.load1_thermistor = ctk.CTkLabel(self, text="Setting:", text_color="white", font=ctk.CTkFont(weight="bold"))
        self.load1_thermistor.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        self.data_load1 = ctk.CTkLabel(self, text="Load 1: ", 
            corner_radius=5, 
            text_color="white")
        self.data_load1.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_voltage = ctk.CTkLabel(self, text="0V", text_color="white")
        self.load1_voltage.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_current = ctk.CTkLabel(self, text="0A", text_color="white")
        self.load1_current.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_temperature = ctk.CTkLabel(self, text="0", text_color="white")
        self.load1_temperature.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
        self.load1_thermistor = ctk.CTkLabel(self, text="0", text_color="white")
        self.load1_thermistor.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")

        self.data_load2 = ctk.CTkLabel(self, text="Load 2: ", 
            corner_radius=5, 
            text_color="white")
        self.data_load2.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_voltage = ctk.CTkLabel(self, text="0", text_color="white")
        self.load2_voltage.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_current = ctk.CTkLabel(self, text="0", text_color="white")
        self.load2_current.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_temperature = ctk.CTkLabel(self, text="0", text_color="white")
        self.load2_temperature.grid(row=3, column=2, padx=10, pady=5, sticky="nsew")
        self.load2_thermistor = ctk.CTkLabel(self, text="0", text_color="white")
        self.load2_thermistor.grid(row=4, column=2, padx=10, pady=5, sticky="nsew")

        self.data_load3 = ctk.CTkLabel(self, text="Load 3: ", 
            corner_radius=5, 
            text_color="white")
        self.data_load3.grid(row=0, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_voltage = ctk.CTkLabel(self, text="0", text_color="white")
        self.load3_voltage.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_current = ctk.CTkLabel(self, text="0", text_color="white")
        self.load3_current.grid(row=2, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_temperature = ctk.CTkLabel(self, text="0", text_color="white")
        self.load3_temperature.grid(row=3, column=3, padx=10, pady=5, sticky="nsew")
        self.load3_thermistor = ctk.CTkLabel(self, text="0", text_color="white")
        self.load3_thermistor.grid(row=4, column=3, padx=10, pady=5, sticky="nsew")
        # self.configure(fg_color="red")
        print("Data Table Widget Initialized")

    def update_table(self, values):
        if len(values) == 12:
            self.load1_voltage.configure(text=f"{values[6]}V")
            self.load1_current.configure(text=f"{values[3]}A")
            self.load1_temperature.configure(text=f"{values[0]}°C")
            self.load1_thermistor.configure(text=f"{values[9]}°C")
                        
            
            self.load2_current.configure(text=f"{values[4]}A")
            self.load2_voltage.configure(text=f"{values[7]}V")
            self.load2_temperature.configure(text=f"{values[1]}°C")
            self.load2_thermistor.configure(text=f"{values[10]}°C")
                        

            self.load3_current.configure(text=f"{values[5]}A")
            self.load3_voltage.configure(text=f"{values[8]}V")
            self.load3_temperature.configure(text=f"{values[2]}°C")
            self.load3_thermistor.configure(text=f"{values[11]}°C")
                        
        else:
            print("Invalid message format received.")   