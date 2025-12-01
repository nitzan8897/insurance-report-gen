# src/gui/modern_app.py
"""
Modern UI for Insurance Report Generator.
Features a clean, centered case type selector with dynamic form display.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .modern_tabs import ModernTabManager
from ..data.data_manager import DataManager
from ..data.constants import Constants
from ..document.report_generator import ReportGenerator


class ModernInsuranceApp:
    """Modern insurance report application with improved UX."""

    def __init__(self, root):
        self.root = root
        self.root.title("מערכת דוחות ביטוח - אניגמה חקירות")
        self.root.geometry("900x700")
        self.root.configure(bg='#f5f5f5')

        # Center window on screen
        self.center_window()

        # Initialize managers
        self.data_manager = DataManager()
        self.report_generator = ReportGenerator()

        # State
        self.form_visible = False
        self.tab_manager = None

        # Create UI
        self.create_header()
        self.create_case_selector()
        self.create_form_container()
        self.create_bottom_buttons()

        # Load saved data if exists
        self.data_manager.load_saved_data()

    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_header(self):
        """Create application header."""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)

        # Company name
        company_label = tk.Label(
            header_frame,
            text="אניגמה חקירות | ENIGMA INVESTIGATIONS",
            font=('David', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        company_label.pack(expand=True)

    def create_case_selector(self):
        """Create the centered case type selector."""
        self.selector_frame = tk.Frame(self.root, bg='#f5f5f5')
        self.selector_frame.pack(fill='both', expand=True, pady=50)

        # Main instruction label
        instruction_label = tk.Label(
            self.selector_frame,
            text="בחר סוג תיק",
            font=('David', 32, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50'
        )
        instruction_label.pack(pady=(0, 30))

        # Dropdown with custom styling
        style = ttk.Style()
        style.configure('Large.TCombobox', padding=10, font=('David', 14))

        self.case_type_combo = ttk.Combobox(
            self.selector_frame,
            values=Constants.EVENT_TYPES,
            state='readonly',
            font=('David', 16),
            width=35
        )
        self.case_type_combo.pack(pady=10)
        self.case_type_combo.bind('<<ComboboxSelected>>', self.on_case_type_selected)

        # Hint text
        hint_label = tk.Label(
            self.selector_frame,
            text="לאחר בחירת סוג התיק, הטופס יופיע אוטומטית",
            font=('David', 11),
            bg='#f5f5f5',
            fg='#7f8c8d'
        )
        hint_label.pack(pady=(10, 0))

    def create_form_container(self):
        """Create container for the dynamic form (hidden initially)."""
        self.form_container = tk.Frame(self.root, bg='#f5f5f5')
        # Don't pack yet - will show when case type is selected

    def create_bottom_buttons(self):
        """Create save and generate report buttons."""
        self.button_frame = tk.Frame(self.root, bg='#f5f5f5', height=70)
        self.button_frame.pack(side='bottom', fill='x', pady=10)
        self.button_frame.pack_propagate(False)

        # Button container (centered)
        btn_container = tk.Frame(self.button_frame, bg='#f5f5f5')
        btn_container.pack(expand=True)

        # Custom button styling
        button_style = {
            'font': ('David', 12, 'bold'),
            'width': 15,
            'height': 2
        }

        # Save button
        save_btn = tk.Button(
            btn_container,
            text="💾 שמור נתונים",
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.save_data,
            **button_style
        )
        save_btn.pack(side='right', padx=10)

        # Generate report button
        generate_btn = tk.Button(
            btn_container,
            text="📄 צור דוח",
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.generate_report,
            **button_style
        )
        generate_btn.pack(side='right', padx=10)

        # Initially hide buttons
        self.button_frame.pack_forget()

    def on_case_type_selected(self, event=None):
        """Handle case type selection and show appropriate form."""
        case_type = self.case_type_combo.get()

        if not case_type:
            return

        # Hide selector
        self.selector_frame.pack_forget()

        # Show form container
        self.form_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Create tab manager with selected case type
        if self.tab_manager:
            # Destroy previous tab manager
            for widget in self.form_container.winfo_children():
                widget.destroy()

        self.tab_manager = ModernTabManager(
            self.form_container,
            self.data_manager,
            case_type
        )

        # Store event type in data manager
        self.data_manager.form_data['event_type'] = self.case_type_combo

        # Show buttons
        self.button_frame.pack(side='bottom', fill='x', pady=10)

        # Add "Change Case Type" button to header
        self.add_change_case_button()

    def add_change_case_button(self):
        """Add button to change case type."""
        change_btn = tk.Button(
            self.root.winfo_children()[0],  # Header frame
            text="← שנה סוג תיק",
            font=('David', 10),
            bg='#34495e',
            fg='white',
            activebackground='#2c3e50',
            activeforeground='white',
            border=0,
            cursor='hand2',
            command=self.show_case_selector
        )
        change_btn.place(relx=0.05, rely=0.5, anchor='w')

    def show_case_selector(self):
        """Show case selector again."""
        # Hide form
        self.form_container.pack_forget()
        self.button_frame.pack_forget()

        # Show selector
        self.selector_frame.pack(fill='both', expand=True, pady=50)

        # Clear selection
        self.case_type_combo.set('')

    def save_data(self):
        """Save form data."""
        try:
            self.data_manager.save_data()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בשמירת הנתונים: {str(e)}")

    def generate_report(self):
        """Generate report document."""
        try:
            success = self.report_generator.generate(self.data_manager.form_data)
            if success:
                messagebox.showinfo("הצלחה", "הדוח נוצר בהצלחה!")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה ביצירת הדוח: {str(e)}")
