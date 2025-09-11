import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class plot_widget(ctk.CTkFrame):
    def __init__(self, master, app_state):
        super().__init__(master)    
        self.app_state = app_state   
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1,2,3), weight=3)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.plots_toggled = [False, False, False]

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
        
        self.toggle_plot(0) # Start with load 1 selected
        self.update_period = 1000 
        self.update_status() # Start updating the plots



    def toggle_plot(self, load_index):
        self.plots_toggled[load_index] = not self.plots_toggled[load_index]
        if load_index == 0:
            self.button_load1.configure(fg_color="#6551D4") if self.plots_toggled[load_index] else self.button_load1.configure(fg_color="gray")
        elif load_index == 1:
            self.button_load2.configure(fg_color="#4D80D0") if self.plots_toggled[load_index] else self.button_load2.configure(fg_color="gray")
        else:
            self.button_load3.configure(fg_color="#0ee69e") if self.plots_toggled[load_index] else self.button_load3.configure(fg_color="gray")
        
    # Update the plot values based on load selections
    def update_status(self):
        # Todo: With a new test, have the plots be reset
        # with self.app_state.lock:
        if self.app_state.serial_connected:
            # print("Updating plots...")
            # Clear axes if any plot is toggled
            if any(self.plots_toggled):
                self.ax_voltage.cla()
                self.ax_current.cla()
                self.ax_temperature.cla()

            if self.plots_toggled[0]:
                try:
                    self.line_L1_voltage = self.ax_voltage.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L1_voltage'],
                        label='Load 1 (V)', color='purple')
                    self.line_L1_current = self.ax_current.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L1_current'],
                        label='Load 1 (A)', color='purple')
                    self.line_L1_temperature = self.ax_temperature.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L1_temperature'],
                        label='Temperature 1 (°C)', color='purple')
                except Exception as e:
                    print(f"Error while getting load 1 data: {e}")

            if self.plots_toggled[1]:
                try:
                    self.line_L2_voltage = self.ax_voltage.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L2_voltage'],
                        label='Load 2 (V)', color='blue')
                    self.line_L2_current = self.ax_current.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L2_current'],
                        label='Load 2 (A)', color='blue')
                    self.line_L2_temperature = self.ax_temperature.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L2_temperature'],
                        label='Temperature 2 (°C)', color='blue')
                except Exception:
                    print("Error while getting load 2 data")

            if self.plots_toggled[2]:
                try:
                    self.line_L3_voltage = self.ax_voltage.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L3_voltage'],
                        label='Load 3 (V)', color='green')
                    self.line_L3_current = self.ax_current.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L3_current'],
                        label='Load 3 (A)', color='green')
                    self.line_L3_temperature = self.ax_temperature.plot(
                        self.app_state.latest_data['time'], self.app_state.latest_data['L3_temperature'],
                        label='Temperature 3 (°C)', color='green')
                except Exception:
                    print("Error while getting load 3 data")

            # Restore axes labels, legends, and grids after clearing
            if any(self.plots_toggled):
                self.ax_voltage.set_xlabel('Time (s)')
                self.ax_voltage.set_ylabel('Voltage (V)')
                self.ax_voltage.legend()
                self.ax_voltage.grid(True)

                self.ax_current.set_xlabel('Time (s)')
                self.ax_current.set_ylabel('Current (A)')
                self.ax_current.legend()
                self.ax_current.grid(True)

                self.ax_temperature.set_xlabel('Time (s)')
                self.ax_temperature.set_ylabel('Temperature (°C)')
                self.ax_temperature.legend()
                self.ax_temperature.grid(True)

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

        self.after(self.update_period, self.update_status)
