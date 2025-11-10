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
        # Helper: safely set data, trimming to the shortest length if needed
        def safe_set(line_obj, x, y, label=""):
            try:
                if not x or not y:
                    line_obj[0].set_data([], [])
                    return
                lx = len(x)
                ly = len(y)
                if lx == ly:
                    line_obj[0].set_data(x, y)
                else:
                    # Trim to the shortest to avoid shape mismatch
                    m = min(lx, ly)
                    line_obj[0].set_data(x[-m:], y[-m:])
                    print(f"Warning: trimmed mismatched lengths for {label} (x={lx}, y={ly})")
            except Exception as e:
                print(f"Error setting data for {label}: {e}")

        t = historical_values.get('time', [])

        if self.plots_toggled[0]:
            safe_set(self.line_L1_voltage, t, historical_values.get('L1_voltage', []), 'L1_voltage')
            safe_set(self.line_L1_current, t, historical_values.get('L1_current', []), 'L1_current')
            safe_set(self.line_L1_temperature, t, historical_values.get('L1_temperature', []), 'L1_temperature')

        if self.plots_toggled[1]:
            safe_set(self.line_L2_voltage, t, historical_values.get('L2_voltage', []), 'L2_voltage')
            safe_set(self.line_L2_current, t, historical_values.get('L2_current', []), 'L2_current')
            safe_set(self.line_L2_temperature, t, historical_values.get('L2_temperature', []), 'L2_temperature')

        if self.plots_toggled[2]:
            safe_set(self.line_L3_voltage, t, historical_values.get('L3_voltage', []), 'L3_voltage')
            safe_set(self.line_L3_current, t, historical_values.get('L3_current', []), 'L3_current')
            safe_set(self.line_L3_temperature, t, historical_values.get('L3_temperature', []), 'L3_temperature')

        # Manually set axis limits based on data to avoid autoscale internals that caused recursion
        def set_axis_limits(ax, lines):
            xs = []
            ys = []
            for ln in lines:
                xd, yd = ln[0].get_data()
                if len(xd) and len(yd):
                    xs.extend(xd if isinstance(xd, (list, tuple)) else list(xd))
                    ys.extend(yd if isinstance(yd, (list, tuple)) else list(yd))
            if xs and ys:
                try:
                    xmin, xmax = min(xs), max(xs)
                    ymin, ymax = min(ys), max(ys)
                    if xmin == xmax:
                        xmin -= 0.5
                        xmax += 0.5
                    if ymin == ymax:
                        ymin -= 0.5
                        ymax += 0.5
                    ax.set_xlim(xmin, xmax)
                    ax.set_ylim(ymin, ymax)
                except Exception as e:
                    print(f"Error setting axis limits: {e}")

        set_axis_limits(self.ax_voltage, [self.line_L1_voltage, self.line_L2_voltage, self.line_L3_voltage])
        set_axis_limits(self.ax_current, [self.line_L1_current, self.line_L2_current, self.line_L3_current])
        set_axis_limits(self.ax_temperature, [self.line_L1_temperature, self.line_L2_temperature, self.line_L3_temperature])

        # Trigger redraw
        try:
            self.canvas_voltage.draw_idle()
            self.canvas_current.draw_idle()
            self.canvas_temperature.draw_idle()
        except Exception as e:
            print(f"Error during canvas draw: {e}")