import customtkinter as ctk

class PortSelectorWidget(ctk.CTkFrame):
    def __init__(self, master, backend_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.backend = backend_manager
        
        # Ensure the backend's connection callback points to this widget's update method
        self.backend.set_connection_callback(self._update_connection_status_ui)

        self.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.port_label = ctk.CTkLabel(self, text="Serial Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.port_variable = ctk.StringVar()
        self.port_option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.port_variable,
            command=self._on_port_selected # Callback when a port is chosen
        )
        self.port_option_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self._populate_ports() # Initial population of ports

        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            command=self._populate_ports
        )
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # --- Connect/Disconnect Button ---
        self.connect_button = ctk.CTkButton(
            self,
            text="Connect",
            command=self._toggle_connection,
            fg_color="green"
        )
        self.connect_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # --- Connection Status Label ---
        self.status_label = ctk.CTkLabel(self, text="Status: Disconnected", text_color="red")
        self.status_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="w")

    def _populate_ports(self):
        """
        Fetches available serial ports from the backend and updates the dropdown menu.
        """
        available_ports = self.backend.list_available_ports()
        if not available_ports:
            available_ports = ["No Ports Found"]
            print("No serial ports found.")
        
        self.port_option_menu.configure(values=available_ports)
        
        # Set the selected value to the first available port, or "No Ports Found"
        if available_ports:
            # If the currently selected port is still in the list, keep it.
            # Otherwise, default to the first available port.
            current_selection = self.port_variable.get()
            if current_selection not in available_ports:
                self.port_variable.set(available_ports[0])
        else:
            self.port_variable.set("No Ports Found")

        print(f"Ports refreshed. Current selection: {self.port_variable.get()}")

    def _on_port_selected(self, selected_port):
        print(f"Port selected: {selected_port}")
        # You can add logic here if you want to automatically connect on selection
        # For now, connection is handled by the 'Connect' button.

    def _toggle_connection(self):
        if self.backend.connected:
            # Disconnect logic
            print("Attempting to disconnect...")
            self.backend.stop_reading_thread()
        else:
            # Connect logic
            selected_port = self.port_variable.get()
            if selected_port == "No Ports Found":
                self.status_label.configure(text="Status: No valid port selected", text_color="orange")
                print("Connection failed: No valid port selected.")
                return

            print(f"Attempting to connect to {selected_port}...")
            if self.backend.connect_to_port(selected_port):
                self.backend.begin_reading_thread()
                # The _update_connection_status_ui will be called by backend's callback
            else:
                self.status_label.configure(text=f"Status: Failed to connect to {selected_port}", text_color="red")
                print(f"Connection failed to {selected_port}.")

    def _update_connection_status_ui(self, is_connected):
        if is_connected:
            self.status_label.configure(text=f"Status: Connected to {self.backend.port_name}", text_color="green")
            self.connect_button.configure(text="Disconnect", fg_color="red")
            print(f"UI updated: Connected to {self.backend.port_name}")
        else:
            self.status_label.configure(text="Status: Disconnected", text_color="red")
            self.connect_button.configure(text="Connect", fg_color="green")
            print("UI updated: Disconnected.")
            # Re-populate ports in case a connection dropped and ports changed
            self._populate_ports()

