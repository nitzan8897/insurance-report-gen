import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from .utils import create_scrollable_frame
from ..data.constants import Constants


class ModernTabManager:
    """Manages dynamic form display based on case type."""

    # Define which tabs to show for each case type
    TAB_VISIBILITY_RULES = {
        'גניבת רכב': ['basic', 'vehicle', 'additional'],
        'צד ג\' - רכב': ['basic', 'vehicle', 'third_party', 'additional'],
        'נזק לרכב': ['basic', 'vehicle', 'additional'],
        'נזקי פריצה': ['basic', 'vehicle', 'additional'],
        'חבויות': ['basic', 'additional'],
        'נח"ל': ['basic', 'additional'],
        'פריצה לעסק': ['basic', 'additional'],
        'נזקי אש': ['basic', 'additional'],
        'פריצה לדירה': ['basic', 'additional'],
        'גניבת כלי צמ"ה': ['basic', 'additional'],
        'אבדן תכשיט': ['basic', 'additional'],
        'גניבת תכשיטים': ['basic', 'additional'],
        'נזקי מים': ['basic', 'additional'],
    }

    def __init__(self, parent, data_manager, case_type):
        self.parent = parent
        self.data_manager = data_manager
        self.case_type = case_type

        # Create notebook
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)

        # Style notebook tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Alef', 11), padding=[15, 8])

        # Determine which tabs to show
        tabs_to_show = self.TAB_VISIBILITY_RULES.get(
            case_type,
            ['basic', 'additional']  # Default fallback
        )

        # Create only the relevant tabs
        if 'basic' in tabs_to_show:
            self.create_basic_tab()

        if 'vehicle' in tabs_to_show:
            self.create_vehicle_tab()

        if 'third_party' in tabs_to_show:
            self.create_third_party_tab()

        if 'additional' in tabs_to_show:
            self.create_additional_tab()

    def create_basic_tab(self):
        """Create basic information tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='פרטים בסיסיים')

        scrollable = create_scrollable_frame(frame)

        # Date (DatePicker)
        self.create_field(scrollable, 0, 'תאריך אירוע', 'event_date',
                         widget_type='date')

        # Basic text fields
        fields = [
            ('claim_number', 'מספר תביעה'),
            ('full_name', 'שם מלא של המבוטח'),
            ('policy_number', 'מספר פוליסה')
        ]

        for i, (field_name, label_text) in enumerate(fields, start=1):
            self.create_field(scrollable, i, label_text, field_name)

    def create_vehicle_tab(self):
        """Create vehicle information tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='פרטי רכב')

        scrollable = create_scrollable_frame(frame)

        # Manufacturer (Dropdown)
        self.create_field(scrollable, 0, 'יצרן הרכב', 'vehicle_company',
                         widget_type='combo', values=Constants.CAR_MANUFACTURERS)

        # Color (Dropdown)
        self.create_field(scrollable, 1, 'צבע הרכב', 'vehicle_color',
                         widget_type='combo', values=Constants.CAR_COLORS)

        # Vehicle text fields
        fields = [
            ('vehicle_model', 'דגם הרכב'),
            ('vehicle_manufacture_year', 'שנת ייצור'),
            ('vehicle_license_number', 'מספר רישוי'),
            ('vehicle_engine_type', 'סוג מנוע'),
            ('vehicle_engine_capacity', 'נפח מנוע'),
            ('vehicle_engine_power', 'הספק מנוע'),
            ('vehicle_gearbox', 'סוג גיר')
        ]

        for i, (field_name, label_text) in enumerate(fields, start=2):
            self.create_field(scrollable, i, label_text, field_name)

    def create_third_party_tab(self):
        """Create third party information tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='פרטי צד ג\'')

        scrollable = create_scrollable_frame(frame)

        fields = [
            ('third_party_name', 'שם צד ג\''),
            ('third_party_policy_number', 'מספר פוליסה צד ג\''),
            ('third_party_contact', 'טלפון צד ג\'')
        ]

        for i, (field_name, label_text) in enumerate(fields):
            self.create_field(scrollable, i, label_text, field_name)

    def create_additional_tab(self):
        """Create additional information tab with text areas."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='פרטים נוספים')

        scrollable = create_scrollable_frame(frame)

        # Circumstances
        self.create_field(scrollable, 0, 'נסיבות האירוע', 'circumstances',
                         widget_type='text', height=5)

        # File uploads
        ttk.Label(scrollable, text='סרטוני וידאו',
                 font=('Alef', 10)).grid(row=1, column=1, padx=5, pady=5, sticky='e')
        video_btn = ttk.Button(scrollable, text='בחר קובץ וידאו',
                              command=lambda: self.upload_file('video'))
        video_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        ttk.Label(scrollable, text='התכתבויות / תמונות',
                 font=('Alef', 10)).grid(row=2, column=1, padx=5, pady=5, sticky='e')
        image_btn = ttk.Button(scrollable, text='בחר קובץ תמונה',
                              command=lambda: self.upload_file('image'))
        image_btn.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        # Investigation
        self.create_field(scrollable, 3, 'החקירה עצמה', 'investigation',
                         widget_type='text', height=5)

        # Summary
        self.create_field(scrollable, 4, 'סיכום', 'summary',
                         widget_type='text', height=5)

    def create_field(self, parent, row, label_text, field_name,
                    widget_type='entry', **kwargs):
        """
        Create a form field with label and appropriate widget.

        Args:
            parent: Parent frame
            row: Grid row
            label_text: Label text
            field_name: Field name for data_manager
            widget_type: 'entry', 'combo', 'text', or 'date'
            **kwargs: Additional arguments for widget
        """
        # Label
        ttk.Label(parent, text=label_text,
                 font=('Alef', 10)).grid(row=row, column=1, padx=5, pady=5, sticky='e')

        # Widget
        if widget_type == 'entry':
            widget = ttk.Entry(parent, width=40, font=('Alef', 10))
            widget.grid(row=row, column=0, padx=5, pady=5, sticky='ew')

        elif widget_type == 'combo':
            values = kwargs.get('values', [])
            widget = ttk.Combobox(parent, values=values, width=37,
                                 state='readonly', font=('Alef', 10))
            widget.grid(row=row, column=0, padx=5, pady=5, sticky='ew')

        elif widget_type == 'text':
            height = kwargs.get('height', 5)
            widget = tk.Text(parent, width=40, height=height, font=('Alef', 10))
            widget.grid(row=row, column=0, padx=5, pady=5, sticky='ew')

        elif widget_type == 'date':
            widget = DateEntry(parent, width=37, background='darkblue',
                             foreground='white', borderwidth=2,
                             date_pattern='dd/mm/yyyy', font=('Alef', 10))
            widget.grid(row=row, column=0, padx=5, pady=5, sticky='ew')

        # Store widget in data manager
        self.data_manager.form_data[field_name] = widget

    def upload_file(self, file_type):
        """Handle file upload."""
        if file_type == 'video':
            file_path = filedialog.askopenfilename(
                title="בחר קובץ וידאו",
                filetypes=[("Video Files", "*.mp4;*.avi;*.mov")]
            )
            if file_path:
                self.data_manager.uploaded_video = file_path
                messagebox.showinfo("הצלחה", f"וידאו נבחר: {file_path.split('/')[-1]}")
        else:
            file_path = filedialog.askopenfilename(
                title="בחר קובץ תמונה",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
            )
            if file_path:
                self.data_manager.uploaded_image = file_path
                messagebox.showinfo("הצלחה", f"תמונה נבחרה: {file_path.split('/')[-1]}")
