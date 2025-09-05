import customtkinter as ctk

# Widget with three buttons to select between loads
class controls_widget(ctk.CTkFrame):
    def __init__(self, master, backend, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.backend = backend
        self.grid_rowconfigure((0,1), weight=2)
        self.grid_rowconfigure((2,3,4,5,6), weight=1)
        # self.rowconfigure(1, weight=8)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.button_load1 = ctk.CTkButton(self, text="Load 1", 
                          fg_color="#6551D4",
                          hover_color="#6551D4",
                          command=lambda: self.select_load(0))
        self.button_load1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_load2 = ctk.CTkButton(self, text="Load 2", 
                          fg_color="gray",
                          hover_color="#4D80D0",  
                          command=lambda: self.select_load(1))
        self.button_load2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button_load3 = ctk.CTkButton(self, text="Load 3",
                          fg_color="gray",
                          hover_color="#0ee69e", 
                          command=lambda: self.select_load(2))
        self.button_load3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.loads = [self.button_load1, self.button_load2, self.button_load3]

        self.load_options = ["Constant Load", "Constant Current", "Power Profile"]
        self.dropdown = ctk.CTkOptionMenu(self, values=self.load_options, 
                            command=self.on_dropdown_change
                            )
        self.dropdown.set("Select Test Type")  # Set initial value to blank
        self.dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=30, sticky="nsew")

        self.button_toggle_test = ctk.CTkButton(self, text="Start Test",
                                             command=self.start_stop_test)
        self.button_toggle_test.grid(row=1, column=2, padx=10, pady=30, sticky="nsew")     


        # start_current and end_current
        self.label_startpoint = ctk.CTkLabel(self, text="Startpoint / Endpoint:", anchor="w", justify="left")
        self.textbox_startpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.textbox_endpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P")) 
        self.label_startpoint.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_startpoint.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="nsew")
        self.textbox_endpoint.grid(row=2, column=2, padx=(5, 10), pady=5, sticky="nsew")
        
        # current_increment and secs_per_step
        self.label_increments = ctk.CTkLabel(self, text="Current Step (A) / Secs Per Step:", anchor="w", justify="left")
        self.textbox_current_inc = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.textbox_time_inc = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.replace('.', '', 1).isdigit() or val == ""), "%P"))
        self.label_increments.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_current_inc.grid(row=3, column=1, padx=(10, 5), pady=5, sticky="nsew")
        self.textbox_time_inc.grid(row=3, column=2, padx=(5, 10), pady=5, sticky="nsew")

        # Filename
        self.label_filename = ctk.CTkLabel(self, text="File Name:", anchor="w", justify="left")
        self.textbox_filename = ctk.CTkEntry(self, validate="key")
        self.label_filename.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        self.textbox_filename.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")
       
        # # Hold times
        # self.label_secs_per_step = ctk.CTkLabel(self, text="Seconds Per Step:")
        # self.textbox_startpoint = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        # self.textbox_current_increment = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        # self.textbox_secs_per_step = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(lambda val: val.isdigit()), "%P")) 
        
        print("Test Manager Widget Initialized")

    def select_load(self, selected_load):
        self.test_info_widget.update_test_info(selected_load)
        if(self.selected_load == 0):
            self.button_load1.configure(fg_color="gray")
        elif(self.selected_load == 1):
            self.button_load2.configure(fg_color="gray")
        else:
            self.button_load3.configure(fg_color="gray")
        self.selected_load = selected_load
        
        if(self.selected_load == 0):
            self.button_load1.configure(fg_color="#6551D4")
        elif(self.selected_load == 1):
            self.button_load2.configure(fg_color="#4D80D0")
        else:
            self.button_load3.configure(fg_color="#0ee69e")

        self.update_load_callback(self.selected_load)
        print(f"Selected {selected_load}")
    
    def start_stop_test(self):
        print("Start/Stop Test Button Pressed")

    def on_dropdown_change(self, pattern, value):
        print(f"Option added: {pattern} -> {value}")
