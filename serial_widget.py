import customtkinter as ctk

class serial_widget(ctk.CTkFrame):
    def __init__(self, master, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.num_ports = 0
        self.connected = False
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)         
        self.grid_rowconfigure((0,1), weight=1)   # Allow row to expand

        self.disconnect_button = ctk.CTkButton(
            self,
            text="Disconnect",
            command=self.on_disconnect,
            fg_color="gray",
            hover_color="#db3333"
        )

        self.disconnect_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.port_variable = ctk.StringVar()
        self.port_option_menu = ctk.CTkOptionMenu(
            self,
            values=["No Ports Found"],
            variable=self.port_variable,
            command=self.on_port_selected # Callback when a port is chosen
        )
        self.port_option_menu.configure(values=["No Ports Found"])
        self.port_option_menu.set("Select Serial Port")  # Set initial value to blank
        self.port_option_menu.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def update_status(self):
        if not self.app_state.serial_connected and self.connected:
            self.port_option_menu.set("Select Serial Port")
            self.connected = False
            self.disconnect_button.configure(text="Disconnect", fg_color="gray")
        if self.app_state.serial_connected and not self.connected:
            self.connected = True
            self.disconnect_button.configure(text="Disconnect", fg_color="#db3333")
            # self.status_label.configure(text="Status: Connected", text_color="green")

        # If the number of ports has changed, repopulate the list
        if self.num_ports != len(self.app_state.available_ports):
            print("Number of ports changed, updating...")
            self.num_ports = len(self.app_state.available_ports)
            self.repopulate_ports()

    def repopulate_ports(self):
        print("0. Time to populate ports...")
        available_ports = self.app_state.available_ports
        print(f"1. Available ports: {available_ports}")

        if not available_ports:
            available_ports = ["No Ports Found"]
            self.port_option_menu.set("Select Serial Port")
        self.port_option_menu.configure(values=available_ports)
 
    def on_port_selected(self, selected_port):
        if(selected_port == "No Ports Found"):
            return
        # self.port_option_menu.set("Connecting...")
        
        self.disconnect_button.configure(text="Connecting...")
        print("Set button state to connecting...")
        with self.app_state.lock:
            print("Send command to connect...")
            self.app_state.command = ["CONNECT", selected_port]


        print(f"Selected port: {selected_port}")

    def on_disconnect(self):
        with self.app_state.lock:
            if self.app_state.serial_connected:
                self.app_state.command = ["DISCONNECT", None]
                self.disconnect_button.configure(text="Disconnecting...")
            else:
                print("No port selected, cannot disconnect.")