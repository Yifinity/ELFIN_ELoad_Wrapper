import customtkinter as ctk

class serial_widget(ctk.CTkFrame):
    def __init__(self, master, backend):
        super().__init__(master)
        self.backend = backend
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=0)         
        self.grid_rowconfigure((0,1), weight=1)   # Allow row to expand

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Disconnected",
            text_color="red",
        )

        self.status_label.grid(
            row=0, 
            column=0, 
            padx=5, 
            pady=5, 
            sticky="nsew")

        self.connect_button = ctk.CTkButton(
            self,
            text="Connect",
            command=self._toggle_connection,
            fg_color="green"
        )

        self.connect_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.port_variable = ctk.StringVar()
        self.port_option_menu = ctk.CTkOptionMenu(
            self,
            variable=self.port_variable,
            command=self._on_port_selected # Callback when a port is chosen
        )

        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            command=self._populate_ports
        )
        self.refresh_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.port_option_menu.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self._populate_ports() # Initial population of ports

    def _toggle_connection(self):
        print("Toggling connection...")

    def _populate_ports(self):
        print("Populating ports...")

    def _on_port_selected(self, selected_port):
        print(f"Selected port: {selected_port}")