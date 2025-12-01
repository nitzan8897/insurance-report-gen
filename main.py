import tkinter as tk
from src.gui.app import ModernInsuranceApp


def main():
    """Launch the modern insurance report application."""
    root = tk.Tk()
    app = ModernInsuranceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
