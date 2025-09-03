import customtkinter as ctk
from app_backend import app_backend
from serial_widget import serial_widget
from plot_widget import plot_widget
from controls_widget import controls_widget   
from table_widget import table_widget

# --- main.py --- #
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("ELFIN - Programmable Electronics Load")
app.geometry("1200x800")

app_backend = app_backend()

# Core components of the app
app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=5)
app.grid_rowconfigure((0,1,2), weight=1, minsize=100)

serial_screen = serial_widget(app, app_backend)
serial_screen.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

controls_screen = controls_widget(app, app_backend)
controls_screen.grid(row=1, column=0,  padx=10, pady=20, sticky="nsew")

table_screen = table_widget(app)
table_screen.grid(row=2, column=0,  padx=10, pady=20, sticky="nsew")

plot_screen = plot_widget(app, app_backend)
plot_screen.grid(row=0, column=1, rowspan=3, padx=10, pady=20, sticky="nsew")

def on_closing():
    print("Application Stopped")
    # backend.stop_reading_thread() # Close our connection
    app.destroy() 

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()