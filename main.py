import customtkinter as ctk
from frontend.frontend_manager import FrontendManager
from backend.backend_manager import BackendManager

# --- main.py --- #
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("ELFIN - Programmable Electronics Load")
app.geometry("1200x700")

# Core components of the app
backend = BackendManager(app)
main_page = FrontendManager(app, backend)
 
backend.begin_reading_thread()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

def on_closing():
    print("Application Stopped")
    backend.stop_reading_thread() # Close our connection
    app.destroy() 

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()