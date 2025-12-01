# main_modern.py
"""
Entry point for the modern insurance report generator application.
"""
import tkinter as tk
from src.gui.modern_app import ModernInsuranceApp


def main():
    """Launch the modern insurance report application."""
    root = tk.Tk()
    app = ModernInsuranceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
