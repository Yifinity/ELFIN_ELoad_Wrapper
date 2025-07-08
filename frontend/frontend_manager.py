import customtkinter as ctk
from frontend.controls_frame import ControlPanelFrame
from frontend.plot_frame import PlotDisplayFrame
from frontend.widgets.port_select_widget import PortSelectorWidget # Import your new widget

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

        # --- New: Instantiate and place the PortSelectorWidget ---
        self.port_selector_widget = PortSelectorWidget(self, self.backend)
        self.port_selector_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        # Use columnspan=2 to make it span across both columns (control and plot)
        # Place it in row 0, which is configured to not expand (weight=0)

        # Controls/Data panels (now in row 1)
        self.control_panel_frame = ControlPanelFrame(self,
                                                     self.selected_load,
                                                     self.load_tests,
                                                     self.update_selected_load)
        self.control_panel_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.plot_panel_frame = PlotDisplayFrame(self, 
                                                 selected_load=self.selected_load)
        self.plot_panel_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Update serial connection status
        # The PortSelectorWidget now handles setting the connection callback to its own UI update method.
        # You might still want to pass the connection status to other widgets if they need it.
        # For example, if ControlPanelFrame needs to know connection status, you'd add a method there:
        # self.backend.set_connection_callback(self.control_panel_frame.update_connection_status)
        # However, since PortSelectorWidget already sets this, you might need to chain them
        # or have PortSelectorWidget pass the status along if other widgets need it directly.
        # For now, I'll keep the original line as it might be used by ControlPanelFrame for other purposes.
        self.backend.set_connection_callback(self.control_panel_frame.update_connection_status)
        self.backend.add_data_callback(self.control_panel_frame.update_data_table)
        self.backend.set_plot_callback(self.plot_panel_frame.update_plot_values)
            
    def update_message(self, message):
        # This method seems to be for a data_label that is not defined in this class.
        # If you have a data_label in FrontendManager, ensure it's initialized.
        # self.data_label.configure(text=f"Data Received: {message}")
        pass # Placeholder or remove if not used

    def update_selected_load(self, target_load):
        self.selected_load = target_load

