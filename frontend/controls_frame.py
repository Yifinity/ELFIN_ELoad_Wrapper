import customtkinter as ctk
from frontend.widgets.serial_connection_widget import SerialConnectionWidget
from frontend.widgets.data_table_widget import DataTableWidget
from frontend.widgets.test_manager_widget import TestManagerWidget

class ControlPanelFrame(ctk.CTkFrame):
    def __init__(self, master, selected_load, load_tests, update_load_callback):
        super().__init__(master)
        # Callback used to update selected load in the plot frame
        self.selected_load = selected_load
        self.load_tests = load_tests
        self.update_load_callback = update_load_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_rowconfigure(2, weight=6)

        self.connection_widget = SerialConnectionWidget(self)
        self.connection_widget.grid(row=0, column=0, padx=10, pady=5,
                                    sticky="nsew")

        self.test_manager_widget = TestManagerWidget(self, self.selected_load,
                                                     self.load_tests,
                                                     self.update_load_callback)
        self.test_manager_widget.grid(row=1, column=0, padx=10, pady=5, 
                                      sticky="nsew")
        
        self.data_table_widget = DataTableWidget(self)
        self.data_table_widget.grid(row=2, column=0, padx=10, pady=5, 
                                    sticky="nsew")

        print("Control Panel Initialized")


    def update_connection_status(self, status):
        self.connection_widget.update_connection(status)
    
    def update_data_table(self, values):
        self.data_table_widget.update_table(values)