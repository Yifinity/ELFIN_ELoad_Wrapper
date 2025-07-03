import customtkinter as ctk

class TestInfoWidget(ctk.CTkFrame):
    def __init__(self, master, load_tests):
        super().__init__(master)
        self.load_tests = load_tests 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,5,6,7), weight=1)

        self.button_toggle_test = ctk.CTkButton(self, text="Start Test",
                                                 command=self.start_stop_test)
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
        self.textbox_target.grid(row=4, column=0, padx=10, pady=5, sticky="ew")


        self.textbox_startpoint = ctk.CTkEntry(self, bg_color="green", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        self.textbox_current_increment = ctk.CTkEntry(self, bg_color="blue", placeholder_text="Current Increment", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        self.textbox_secs_per_step = ctk.CTkEntry(self, bg_color="purple", placeholder_text="Seconds per Step", validate="key", validatecommand=(self.register(lambda val: val.isdigit() or val == ""), "%P")) 
        
        self.label_test_info.grid_forget() 
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

    def start_stop_test(self):
        if(self.load_tests[self.master.selected_load]["test_type"] == 0):
            if(self.check_valid_test()): 
                self.load_tests[self.master.selected_load]["test_type"] = self.dropdown.get()
                self.load_tests[self.master.selected_load]["target"] = int(self.textbox_target.get())
                if(self.load_tests[self.master.selected_load]["test_type"] == "Power Profile"):
                    self.load_tests[self.master.selected_load]["extra_params"] = [
                        int(self.textbox_startpoint.get()),
                        int(self.textbox_current_increment.get()),
                        int(self.textbox_secs_per_step.get())
                    ]
                self.clear_textboxes()

        else:
            self.load_tests[self.master.selected_load]["test_type"] = 0
            self.load_tests[self.master.selected_load]["target"] = 0
            self.load_tests[self.master.selected_load]["extra_params"] = []
        self.update_test_info(self.master.selected_load)

    def update_test_info(self, load_selection):
        self.label_test_info.grid_forget()
        self.label_dropdown.grid_forget()
        self.dropdown.grid_forget()
        self.clear_textboxes()

        # No test for that specific load
        if(self.load_tests[load_selection]["test_type"] == 0):
            self.label_dropdown.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.dropdown.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
            self.textbox_target.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
            
        else:                
            self.label_test_info.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.display_test_info(self.load_tests[load_selection])
#            self.label_test_info.configure(text=f"Running: \n {self.load_tests[load_selection]}")
        # If test is not empty, that means we're running one
        self.toggle_switch_state(self.load_tests[load_selection]["test_type"] != 0)
        
    def display_test_info(self, test_info):
        test_type = test_info["test_type"]
        test_target = test_info["target"]
        test_extra_params = test_info["extra_params"] 

        output_string = "Test Type: "
        if(test_type == "Constant Load" or test_type == "Constant Current"):
            if(test_type == 1):
                output_string += "Constant Load"
            else:
                output_string += "Constant Current"
            output_string += f"\n Target: {test_target}"
        else:
            output_string += f"Current Profile: \n"
            output_string += f"Range: {test_target}-{test_extra_params[0]}A \n"
            output_string += f"Current Increment: {test_extra_params[1]}\n"
            output_string += f"Second Per Step: {test_extra_params[2]}"
        self.label_test_info.configure(text=output_string)
            
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
            self.textbox_startpoint.configure(placeholder_text="Constant Load")
        else:
            self.textbox_startpoint.configure(placeholder_text="Constant Current")

        if selection == "Power Profile":
            self.textbox_startpoint.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
            self.textbox_current_increment.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
            self.textbox_secs_per_step.grid(row=7, column=0, padx=10, pady=5, sticky="ew")


            