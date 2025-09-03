import customtkinter as ctk
from app_backend import app_backend
from serial_widget import serial_widget

# --- main.py --- #
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("ELFIN - Programmable Electronics Load")
app.geometry("1200x800")

# Core components of the app
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=5)
app.grid_columnconfigure(2, weight=0)

app_backend = app_backend()
serial_widget = serial_widget(app, app_backend)
serial_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# backend.begin_reading_thread()

def on_closing():
    print("Application Stopped")
    # backend.stop_reading_thread() # Close our connection
    app.destroy() 

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()