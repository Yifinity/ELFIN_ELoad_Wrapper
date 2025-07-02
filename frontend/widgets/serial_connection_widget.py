import customtkinter as ctk

class SerialConnectionWidget(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.connected_label = ctk.CTkLabel(self, text="Disconnected", 
                                            corner_radius=5, text_color="white",
                                            fg_color = "#ff0000")
        self.connected_label.grid(row = 0, column = 0, padx = 20, pady = 20)
        print("Serial Connection Widget Initialized")

    def update_connection(self, status):
        if status:
            self.connected_label.configure(text="Connected", 
                                           fg_color="#008e2a")
        else:
            self.connected_label.configure(text="Disconnected", 
                                           fg_color="#ff0000")
            