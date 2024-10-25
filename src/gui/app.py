# src/gui/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from .tabs import TabManager
from ..data.data_manager import DataManager
from ..document.report_generator import ReportGenerator

class InsuranceReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("מערכת דוחות ביטוח")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configure Hebrew RTL
        self.root.tk.call('tk', 'scaling', 1.3)
        
        # Initialize managers
        self.data_manager = DataManager()
        self.tab_manager = TabManager(self.root, self.data_manager)
        self.report_generator = ReportGenerator()
        
        # Create bottom buttons
        self.create_bottom_buttons()
        
        # Load saved data - Changed this line
        self.data_manager.load_saved_data()

    def create_bottom_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        save_button = ttk.Button(
            button_frame, 
            text="שמור", 
            command=self.data_manager.save_data
        )
        save_button.pack(side="left", padx=5)

        generate_report_button = ttk.Button(
            button_frame, 
            text="צור דוח", 
            command=self.generate_report
        )
        generate_report_button.pack(side="left", padx=5)

    def generate_report(self):
        try:
            self.report_generator.generate(self.data_manager.form_data)
            messagebox.showinfo("הצלחה", "הדו\"ח נוצר בהצלחה!")
        except Exception as e:
            messagebox.showerror(
                "שגיאה", 
                f"אירעה שגיאה בעת יצירת הדו\"ח: {str(e)}"
            )