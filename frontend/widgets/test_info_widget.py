import customtkinter as ctk

class TestInfoWidget(ctk.CTkFrame):
    def __init__(self, master, load_tests):
        super().__init__(master)
        self.load_tests = load_tests 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,5,6,7), weight=1)

        self.button_toggle_test = ctk.CTkButton(self, text="Start Test",
                                                 command=self.toggle_test)
        self.button_toggle_test.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")     

        self.label_test_info = ctk.CTkLabel(self, text="Test Information")  
        self.label_test_info.grid(row=1, column=0, padx=10, pady=10, sticky="nsew") 

        # Dropdown for load selection
        self.label_dropdown = ctk.CTkLabel(self, text="Select Load Type:")
        self.label_dropdown.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.load_options = ["Constant Load", "Constant Current", "Power Profile"]
        self.dropdown = ctk.CTkOptionMenu(self, values=self.load_options, command=self.on_dropdown_change)
        self.dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # start_current and end_current
        self.textbox_target = ctk.CTkEntry(self, placeholder_text="Target Load:", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        self.textbox_startpoint = ctk.CTkEntry(self, placeholder_text="Starting Current", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        # step_current
        self.textbox_current_increment = ctk.CTkEntry(self, placeholder_text="Current Increment", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        # step_dwell_time
        self.textbox_secs_per_step = ctk.CTkEntry(self, placeholder_text="Seconds per Step", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        
        self.label_test_info.grid_forget() 
        self.textbox_target.grid_forget()
        self.textbox_startpoint.grid_forget()
        self.textbox_current_increment.grid_forget()
        self.textbox_secs_per_step.grid_forget()
        self.toggle_switch_state(False) # No Test Running

        print("Test Info Widget Initialized")


    def toggle_switch_state(self, running):
        if running:
            self.button_toggle_test.configure(text="End Test", 
                                              fg_color="#ff0000")
        else:            
            self.button_toggle_test.configure(text="Start Test", 
                                              fg_color="#008e2a")


    def update_test_info(self, load_selection):
        self.label_test_info.grid_forget()
        self.label_dropdown.grid_forget()
        self.dropdown.grid_forget()
        self.clear_textboxes()

        # No Test Selected
        if(self.load_tests[load_selection]["test_type"] == 0):
            # Display Selection
            self.label_dropdown.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.dropdown.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        else:                
            self.label_test_info.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.label_test_info.configure(text=f"Running: \n {self.load_tests[load_selection]}")
        # If test is not empty, that means we're running one
        self.toggle_switch_state(self.load_tests[load_selection]["test_type"] != 0)
        


    def toggle_test(self):
        if(self.load_tests[self.master.selected_load]["test_type"] == 0):
            if(self.check_valid_test()): 
                self.load_tests[self.master.selected_load]["test_type"] = self.dropdown.get()
                self.load_tests[self.master.selected_load]["target"] = int(self.textbox_target.get())
                self.clear_textboxes()

                if(self.load_tests[self.master.selected_load]["test_type"] == "Power Profile"):
                    self.load_tests[self.master.selected_load]["extra_params"] = [
                        int(self.textbox_startpoint.get()),
                        int(self.textbox_current_increment.get()),
                        int(self.textbox_secs_per_step.get())
                    ]
        else:
            self.load_tests[self.master.selected_load]["test_type"] = 0
            self.load_tests[self.master.selected_load]["target"] = 0
            self.load_tests[self.master.selected_load]["extra_params"] = []
        self.update_test_info(self.master.selected_load)

    def clear_textboxes(self):
        self.textbox_target.delete(0, "end")
        self.textbox_startpoint.delete(0, "end")
        self.textbox_current_increment.delete(0, "end")
        self.textbox_secs_per_step.delete(0, "end")
        self.textbox_target.grid_forget()
        self.textbox_startpoint.grid_forget()
        self.textbox_current_increment.grid_forget()
        self.textbox_secs_per_step.grid_forget()

    def check_valid_test(self):
        return True

    def on_dropdown_change(self, selection):
        self.textbox_target.grid_forget()
        self.textbox_startpoint.grid_forget()
        self.textbox_current_increment.grid_forget()
        self.textbox_secs_per_step.grid_forget()

        self.textbox_target.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        if selection == "Constant Load":
            self.textbox_startpoint.configure(placeholder_text="Target Load")
        else:
            self.textbox_startpoint.configure(placeholder_text="Target Current")

        if selection == "Power Profile":
            self.textbox_startpoint.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
            self.textbox_current_increment.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
            self.textbox_secs_per_step.grid(row=7, column=0, padx=10, pady=5, sticky="ew")


            