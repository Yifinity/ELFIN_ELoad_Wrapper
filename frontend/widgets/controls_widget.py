import customtkinter as ctk

# Widget with three buttons to select between loads
class controls_widget(ctk.CTkFrame):
    def __init__(self, master, app_state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app_state = app_state
        self.connected = False
        self.update_period = 200
        # self.backend = backend
        self.grid_rowconfigure((0,1), weight=2)
        self.grid_rowconfigure((2,3,4,5,6), weight=1)
        # self.rowconfigure(1, weight=8)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.button_load1 = ctk.CTkButton(self, text="Load 1", 
                          fg_color="#6551D4",
                          text_color="white",
                          hover_color="#6551D4",
                          command=lambda: self.select_load(0))
        self.button_load1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_load2 = ctk.CTkButton(self, text="Load 2", 
                          fg_color="gray",
                          hover_color="#4D80D0",  
                          text_color="white",
                          command=lambda: self.select_load(1))
        self.button_load2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button_load3 = ctk.CTkButton(self, text="Load 3",
                          fg_color="gray",
                          hover_color="#0ee69e", 
                          text_color="white",
                          command=lambda: self.select_load(2))
        self.button_load3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.loads = [self.button_load1, self.button_load2, self.button_load3]

        self.load_options = ["Constant Load", "Constant Current", "Power Profile"]
        self.dropdown = ctk.CTkOptionMenu(self, values=self.load_options, text_color="white",
                            command=self.on_dropdown_selected)

        self.dropdown.set("Select Test Type")  # Set initial value to blank
        self.dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=30, sticky="nsew")

        self.button_toggle_test = ctk.CTkButton(self, text="Start Test",
                                             command=self.start_stop_test)
        self.button_toggle_test.grid(row=1, column=2, padx=10, pady=30, sticky="nsew")     


        # start_current and end_current
        self.label_startpoint = ctk.CTkLabel(self, text="Startpoint / Endpoint:", text_color="white",  anchor="w", justify="left")
        self.textbox_startpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.textbox_endpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P")) 
        self.label_startpoint.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_startpoint.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="nsew")
        self.textbox_endpoint.grid(row=2, column=2, padx=(5, 10), pady=5, sticky="nsew")
        
        # current_increment and secs_per_step
        self.label_increments = ctk.CTkLabel(self, text="Current Step (A) / Secs Per Step:",  text_color="white", anchor="w", justify="left")
        self.textbox_current_inc = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.textbox_time_inc = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.label_increments.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_current_inc.grid(row=3, column=1, padx=(10, 5), pady=5, sticky="nsew")
        self.textbox_time_inc.grid(row=3, column=2, padx=(5, 10), pady=5, sticky="nsew")

        # Filename
        self.label_filename = ctk.CTkLabel(self, text="File Name:",  text_color="white", anchor="w", justify="left")
        self.textbox_filename = ctk.CTkEntry(self, validate="key")
        self.label_filename.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_filename.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
       
        self.disable_gui()
        self.update_status()
        # # Hold times
        # self.label_secs_per_step = ctk.CTkLabel(self, text="Seconds Per Step:")
        # self.textbox_startpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        # self.textbox_current_increment = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        # self.textbox_secs_per_step = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        
        print("Test Manager Widget Initialized")

    def select_load(self, selected_load):
        self.button_load1.configure(fg_color="gray")
        self.button_load2.configure(fg_color="gray")
        self.button_load3.configure(fg_color="gray")

        if(selected_load == 0):
            print("Load 0 clicked")
            self.button_load1.configure(fg_color="#6551D4")
        elif(selected_load == 1):
            print("Load 1 clicked")
            self.button_load2.configure(fg_color="#4D80D0")
        else:
            print("Load 2 clicked")
            self.button_load3.configure(fg_color="#0ee69e")
        # self.selected_load = selected_load
    
        print(f"Selected {selected_load}")
    
    def update_status(self):
        # Disconnected Event
        if not self.app_state.serial_connected and self.connected:
            self.disable_gui()
            self.connected = False

        # Connecfted Event
        if self.app_state.serial_connected and not self.connected:
            print("Controls is connected")
            self.enable_gui()
            self.connected = True

        self.after(self.update_period, self.update_status)  # Check every second


    def disable_gui(self):
        self.button_load1.configure(state="disabled")
        self.button_load2.configure(state="disabled")
        self.button_load3.configure(state="disabled")
        self.dropdown.configure(state="disabled")
        self.button_toggle_test.configure(state="disabled")

        # self.textbox_startpoint.configure(state="disabled")
        # self.textbox_endpoint.configure(state="disabled")
        # self.textbox_current_inc.configure(state="disabled")
        # self.textbox_time_inc.configure(state="disabled")


    def enable_gui(self):
        self.button_load1.configure(state="enabled")
        self.button_load2.configure(state="enabled")
        self.button_load3.configure(state="enabled")

        # Used to re-enabled the hover
        self.button_load1._on_leave()
        self.button_load2._on_leave()
        self.button_load3._on_leave()
        self.dropdown.configure(state="enabled")
        self.button_toggle_test.configure(state="enabled")
        self.button_toggle_test._on_leave()
        # self.textbox_startpoint.configure(state="enabled")
        # self.textbox_endpoint.configure(state="enabled")
        # self.textbox_current_inc.configure(state="enabled")
        # self.textbox_time_inc.configure(state="enabled")

    def start_stop_test(self):
        print("Test Sent Button Pressed")
        self.app_state.command = ["SEND", "a"]

    def on_dropdown_selected(self, value):
        with self.app_state.lock:
            if(value not in self.load_options):
                self.app_state.test_type = None
                # print("Invalid Test Type Selected")
            self.update_test_options(value)
        
        print(f"Option selected: {self.app_state.test_type}")
    
    def update_test_options(self, test_type):
        self.app_state.test_type = test_type
        # Constant load/current just needs startpoint.

        if(test_type == "Constant Load"):
            self.textbox_endpoint.configure(state="disabled")
            self.textbox_current_inc.configure(state="disabled")
            self.textbox_time_inc.configure(state="disabled")
            self.label_increments.configure(text_color="grey")
            
        elif(test_type == "Constant Current"):
            self.textbox_endpoint.configure(state="disabled")
            self.textbox_current_inc.configure(state="disabled")
            self.textbox_time_inc.configure(state="disabled")
            self.label_increments.configure(text_color="grey")
            

        elif(test_type == "Power Profile"):
            self.textbox_endpoint.configure(state="normal")
            self.textbox_current_inc.configure(state="normal")
            self.textbox_time_inc.configure(state="normal")
            self.label_increments.configure(text_color="white")
            
        else:
            self.textbox_endpoint.configure(state="disabled")
            self.textbox_current_inc.configure(state="disabled")
            self.textbox_time_inc.configure(state="disabled")
            self.label_increments.configure(text_color="grey")
            
