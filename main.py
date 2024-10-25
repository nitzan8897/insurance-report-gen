import tkinter as tk
from src.gui.app import InsuranceReportGenerator

def main():
    root = tk.Tk()
    app = InsuranceReportGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()