import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotDisplayFrame(ctk.CTkFrame):
    def __init__(self, master, selected_load):
        super().__init__(master)       
                # Configure grid rows for proper layout
        self.selected_load = selected_load
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1,2,3), weight=3)
        self.grid_columnconfigure((0,1,2), weight=1)

        # Initialize the plot
        # Create three independent figures for voltage, current, and temperature
        self.fig_voltage, self.ax_voltage = plt.subplots(figsize=(6, 4))
        self.fig_current, self.ax_current = plt.subplots(figsize=(6, 4))
        self.fig_temperature, self.ax_temperature = plt.subplots(figsize=(6, 4))

        # Voltage plot
        self.line_L1_voltage = self.ax_voltage.plot([], [],
                                                      label='Load 1 (V)', color='purple')
        self.line_L2_voltage = self.ax_voltage.plot([], [], 
                                                    label='Load 2 (V)', color='blue')
        self.line_L3_voltage = self.ax_voltage.plot([], [], 
                                                    label='Load 3 (V)', color='green')
        self.ax_voltage.set_xlabel('Time (s)')
        self.ax_voltage.set_ylabel('Voltage (V)')
        # self.ax_voltage.set_title('Voltage vs Time')
        self.ax_voltage.legend()
        self.ax_voltage.grid(True)

        # Current plot
        self.line_L1_current = self.ax_current.plot([], [],
                                                      label='Load 1 (A)', color='purple')
        self.line_L2_current = self.ax_current.plot([], [], 
                                                    label='Load 2 (A)', color='blue')
        self.line_L3_current = self.ax_current.plot([], [], 
                                                    label='Load 3 (A)', color='green')

        self.ax_current.set_xlabel('Time (s)')
        self.ax_current.set_ylabel('Current (A)')
        # self.ax_current.set_title('Current vs Time')
        self.ax_current.legend()
        self.ax_current.grid(True)

        # Temperature plot
        self.line_L1_temperature = self.ax_temperature.plot([], [],
                                                      label='Temperature 1 (°C)', color='purple')
        self.line_L2_temperature = self.ax_temperature.plot([], [], 
                                                    label='Temperature 2 (°C)', color='blue')
        self.line_L3_temperature = self.ax_temperature.plot([], [], 
                                                    label='Temperature 3 (°C)', color='green')

        self.ax_temperature.set_xlabel('Time (s)')
        self.ax_temperature.set_ylabel('Temperature (°C)')
        # self.ax_temperature.set_title('Temperature vs Time')
        self.ax_temperature.legend()
        self.ax_temperature.grid(True)

        self.button_load1 = ctk.CTkButton(self, text="Load 1", 
              fg_color="gray",
              hover_color="#6551D4",
              command=lambda: self.toggle_plot(0))
        self.button_load1.grid(row=0, column=0, 
                   padx=10, pady=10, sticky="nsew")

        self.button_load2 = ctk.CTkButton(self, text="Load 2", 
                  fg_color="gray",
                  hover_color="#4D80D0",  
                  command=lambda: self.toggle_plot(1))
        self.button_load2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.button_load3 = ctk.CTkButton(self, text="Load 3",
                  fg_color="gray",
                  hover_color="#0ee69e", 
                  command=lambda: self.toggle_plot(2))        
        self.button_load3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Create canvases for each figure
        self.canvas_voltage = FigureCanvasTkAgg(self.fig_voltage, master=self)
        self.canvas_voltage_widget = self.canvas_voltage.get_tk_widget()
        self.canvas_voltage_widget.grid(row=1, column=0, columnspan=3, padx=10,
                                         pady=10, sticky="nsew")

        self.canvas_current = FigureCanvasTkAgg(self.fig_current, master=self)
        self.canvas_current_widget = self.canvas_current.get_tk_widget()
        self.canvas_current_widget.grid(row=2, column=0, columnspan=3, padx=10,
                                         pady=10, sticky="nsew")

        self.canvas_temperature = FigureCanvasTkAgg(self.fig_temperature, master=self)
        self.canvas_temperature_widget = self.canvas_temperature.get_tk_widget()
        self.canvas_temperature_widget.grid(row=3, column=0,columnspan=3,
                                         padx=10, pady=10, sticky="nsew")
        
        # Track which lines are toggled
        self.plots_toggled = [False, False, False] 
        self.loads = [
            [
                self.line_L1_voltage,
                self.line_L2_voltage,
                self.line_L3_voltage
            ],
            [
                self.line_L1_current,
                self.line_L2_current,
                self.line_L3_current
            ],
            [
                self.line_L1_temperature,
                self.line_L2_temperature,
                self.line_L3_temperature
            ]
        ]
        self.toggle_plot(0) # enable the first graph on startup.


    def toggle_plot(self, target):
        # Clear the data would go to each of the lines
        for data_idx in range(3):
            self.loads[data_idx][target][0].set_data([],[])

        self.plots_toggled[target] = not self.plots_toggled[target]
        if target == 0:
            self.button_load1.configure(fg_color="#6551D4") if self.plots_toggled[target] else self.button_load1.configure(fg_color="gray")
        elif target == 1:
            self.button_load2.configure(fg_color="#4D80D0") if self.plots_toggled[target] else self.button_load2.configure(fg_color="gray")
        else:
            self.button_load3.configure(fg_color="#0ee69e") if self.plots_toggled[target] else self.button_load3.configure(fg_color="gray")

    # Update the plot values based on load selections
    def update_plot_values(self, historical_values):
        if(self.plots_toggled[0]):
            try:
                self.line_L1_voltage[0].set_data(historical_values['time'], historical_values['L1_voltage'])
                self.line_L1_current[0].set_data(historical_values['time'], historical_values['L1_current'])
                self.line_L1_temperature[0].set_data(historical_values['time'], historical_values['L1_temperature']) 
            except:
                print("Error while getting voltage")

        if(self.plots_toggled[1]):
            try:
                self.line_L2_voltage[0].set_data(historical_values['time'], historical_values['L2_voltage'])
                self.line_L2_current[0].set_data(historical_values['time'], historical_values['L2_current'])
                self.line_L2_temperature[0].set_data(historical_values['time'], historical_values['L2_temperature']) 
            except:
                print("Error while getting current")

        if(self.plots_toggled[2]):
            try:
                self.line_L3_voltage[0].set_data(historical_values['time'], historical_values['L3_voltage'])
                self.line_L3_current[0].set_data(historical_values['time'], historical_values['L3_current'])
                self.line_L3_temperature[0].set_data(historical_values['time'], historical_values['L3_temperature']) 
            except:
                print("Error while getting temperature")

        self.ax_voltage.relim()
        self.ax_voltage.autoscale_view()

        self.ax_current.relim()
        self.ax_current.autoscale_view()

        self.ax_temperature.relim()
        self.ax_temperature.autoscale_view()

        self.canvas_voltage.draw_idle()
        self.canvas_current.draw_idle()
        self.canvas_temperature.draw_idle()

        # Force Tkinter canvas to update immediately for new plots and redraws
        self.canvas_voltage.flush_events()
        self.canvas_current.flush_events()
        self.canvas_temperature.flush_events()