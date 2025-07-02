import customtkinter as ctk
from frontend.widgets.test_info_widget import TestInfoWidget

# Widget with three buttons to select between loads
class TestManagerWidget(ctk.CTkFrame):
    def __init__(self, master, selected_load, load_tests, update_load_callback):
        super().__init__(master)
        self.selected_load = selected_load
        self.load_tests = load_tests
        self.update_load_callback = update_load_callback
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        self.grid_columnconfigure((0,1,2,3), weight=1)

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


        self.test_info_widget = TestInfoWidget(self, self.load_tests)
        self.test_info_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        self.loads = [self.button_load1, self.button_load2, self.button_load3]
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
       