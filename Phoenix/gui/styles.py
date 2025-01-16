from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    
    # Configure colors
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))

    # Add more style configurations as needed