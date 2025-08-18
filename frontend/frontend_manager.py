import customtkinter as ctk
from frontend.controls_frame import ControlPanelFrame
from frontend.plot_frame import PlotDisplayFrame
from frontend.port_select_widget import PortSelectorWidget # Import your new widget

class FrontendManager(ctk.CTkFrame):
    def __init__(self, master, backend_manager):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=20) 
        self.grid_rowconfigure(0, weight=0) # Row for port selector (fixed height)
        self.grid_rowconfigure(1, weight=1) # Row for control and plot panels (expands)
        self.backend = backend_manager

        # shared between both the control and plot frames
        self.selected_load = 0  # Default selected is 0

        # 0 = none, 1 = constant load, 2 = constant current, 3 = profile
        self.load_tests = {
            # Load 1
            0:{
                "test_type": 0,
                "target": 0, # Current/Load Target
                "extra_params": [] # Extra params for test #3
            },
            1:{
                "test_type": 0, 
                "target": 0,
                "extra_params": [] # startpoint, current_increment, secs_per_step
            },        
            2:{
                "test_type": 0,
                "target": 0, 
                "extra_params": [] 
            }
        }

        self.port_selector_widget = PortSelectorWidget(self, self.backend)
        self.port_selector_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
  
        # Controls/Data panels (now in row 1)
        self.control_panel_frame = ControlPanelFrame(self,
                                                     self.backend, 
                                                     self.selected_load,
                                                     self.load_tests,
                                                     self.update_selected_load)
        self.control_panel_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.plot_panel_frame = PlotDisplayFrame(self, 
                                                 selected_load=self.selected_load)
        self.plot_panel_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.backend.add_data_callback(self.control_panel_frame.update_data_table)
        self.backend.set_plot_callback(self.plot_panel_frame.update_plot_values)
            
    def update_message(self, message):
        pass # Placeholder or remove if not used

    def update_selected_load(self, target_load):
        self.selected_load = target_load

