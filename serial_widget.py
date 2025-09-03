import customtkinter as ctk

class serial_widget(ctk.CTkFrame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.backend = backend
        self._fg_color = None
        
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

    def _toggle_connection(self):
        print("Toggling connection...")

    def _populate_ports(self):
        print("Populating ports...")

    def _on_port_selected(self, selected_port):
        print(f"Selected port: {selected_port}")