# gui/tabs.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from .utils import create_scrollable_frame
from ..data.constants import Constants

class TabManager:
    def __init__(self, root, data_manager):
        self.root = root
        self.data_manager = data_manager
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Initialize frames
        self.basic_frame = None
        self.vehicle_frame = None
        self.third_party_frame = None
        self.additional_frame = None
        
        # Create tabs
        self.create_tabs()
        
        # Bind event type change if the combobox exists
        if 'event_type' in self.data_manager.form_data:
            self.data_manager.form_data['event_type'].bind(
                '<<ComboboxSelected>>', self.on_event_type_change)

    def create_tabs(self):
        # Basic Info Tab
        self.basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_frame, text='פרטים בסיסיים')
        self.create_basic_info_fields(self.basic_frame)

        # Vehicle Info Tab
        self.vehicle_frame = ttk.Frame(self.notebook)
        self.create_vehicle_info_fields(self.vehicle_frame)

        # Third Party Tab
        self.third_party_frame = ttk.Frame(self.notebook)
        self.create_third_party_fields(self.third_party_frame)

        # Additional Info Tab
        self.additional_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.additional_frame, text='פרטים נוספים')
        self.create_additional_info_fields(self.additional_frame)

    def create_basic_info_fields(self, parent):
        scrollable_frame = create_scrollable_frame(parent)

        # Event Type (Dropdown)
        ttk.Label(scrollable_frame, text='סוג תיק').grid(row=0, column=1, padx=5, pady=5, sticky='e')
        event_type = ttk.Combobox(scrollable_frame, values=Constants.EVENT_TYPES, width=37, state='readonly')
        event_type.grid(row=0, column=0, padx=5, pady=5)
        self.data_manager.form_data['event_type'] = event_type

        # Date (DatePicker)
        ttk.Label(scrollable_frame, text='תאריך אירוע').grid(row=1, column=1, padx=5, pady=5, sticky='e')
        date_picker = DateEntry(scrollable_frame, width=37, background='darkblue',
                              foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        date_picker.grid(row=1, column=0, padx=5, pady=5)
        self.data_manager.form_data['event_date'] = date_picker

        # Other basic fields
        fields = [
            ('claim_number', 'מספר תביעה'),
            ('full_name', 'שם מלא של המבוטח'),
            ('policy_number', 'מספר פוליסה')
        ]

        for i, (field_name, label_text) in enumerate(fields, start=2):
            ttk.Label(scrollable_frame, text=label_text).grid(row=i, column=1, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(scrollable_frame, width=40)
            entry.grid(row=i, column=0, padx=5, pady=5)
            self.data_manager.form_data[field_name] = entry

    def create_vehicle_info_fields(self, parent):
        scrollable_frame = create_scrollable_frame(parent)

        # Manufacturer (Dropdown)
        ttk.Label(scrollable_frame, text='יצרן הרכב').grid(row=0, column=1, padx=5, pady=5, sticky='e')
        manufacturer = ttk.Combobox(scrollable_frame, values=Constants.CAR_MANUFACTURERS, width=37, state='readonly')
        manufacturer.grid(row=0, column=0, padx=5, pady=5)
        self.data_manager.form_data['vehicle_company'] = manufacturer

        # Color (Dropdown)
        ttk.Label(scrollable_frame, text='צבע הרכב').grid(row=1, column=1, padx=5, pady=5, sticky='e')
        color = ttk.Combobox(scrollable_frame, values=Constants.CAR_COLORS, width=37, state='readonly')
        color.grid(row=1, column=0, padx=5, pady=5)
        self.data_manager.form_data['vehicle_color'] = color

        # Vehicle fields
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
            ttk.Label(scrollable_frame, text=label_text).grid(row=i, column=1, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(scrollable_frame, width=40)
            entry.grid(row=i, column=0, padx=5, pady=5)
            self.data_manager.form_data[field_name] = entry

    def create_third_party_fields(self, parent):
        scrollable_frame = create_scrollable_frame(parent)

        fields = [
            ('third_party_name', 'שם צד ג\''),
            ('third_party_policy_number', 'מספר פוליסה צד ג\''),
            ('third_party_contact', 'טלפון צד ג\'')
        ]

        for i, (field_name, label_text) in enumerate(fields):
            ttk.Label(scrollable_frame, text=label_text).grid(row=i, column=1, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(scrollable_frame, width=40)
            entry.grid(row=i, column=0, padx=5, pady=5)
            self.data_manager.form_data[field_name] = entry

    def create_additional_info_fields(self, parent):
        scrollable_frame = create_scrollable_frame(parent)

        # Circumstances
        ttk.Label(scrollable_frame, text='נסיבות האירוע').grid(row=0, column=1, padx=5, pady=5, sticky='e')
        circumstances_text = tk.Text(scrollable_frame, width=40, height=5)
        circumstances_text.grid(row=0, column=0, padx=5, pady=5)
        self.data_manager.form_data['circumstances'] = circumstances_text

        # File upload buttons
        ttk.Label(scrollable_frame, text='סרטוני וידאו').grid(row=1, column=1, padx=5, pady=5, sticky='e')
        video_upload_button = ttk.Button(scrollable_frame, text='בחר קובץ', 
                                       command=lambda: self.upload_file('video'))
        video_upload_button.grid(row=1, column=0, padx=5, pady=5)

        ttk.Label(scrollable_frame, text='התכתבויות').grid(row=2, column=1, padx=5, pady=5, sticky='e')
        image_upload_button = ttk.Button(scrollable_frame, text='בחר קובץ', 
                                       command=lambda: self.upload_file('image'))
        image_upload_button.grid(row=2, column=0, padx=5, pady=5)

        # Investigation and Summary
        ttk.Label(scrollable_frame, text='החקירה עצמה').grid(row=3, column=1, padx=5, pady=5, sticky='e')
        investigation_text = tk.Text(scrollable_frame, width=40, height=5)
        investigation_text.grid(row=3, column=0, padx=5, pady=5)
        self.data_manager.form_data['investigation'] = investigation_text

        ttk.Label(scrollable_frame, text='סיכום').grid(row=4, column=1, padx=5, pady=5, sticky='e')
        summary_text = tk.Text(scrollable_frame, width=40, height=5)
        summary_text.grid(row=4, column=0, padx=5, pady=5)
        self.data_manager.form_data['summary'] = summary_text

    def upload_file(self, file_type):
        if file_type == 'video':
            file_path = filedialog.askopenfilename(
                title="בחר קובץ וידאו",
                filetypes=[("Video Files", "*.mp4;*.avi;*.mov")]
            )
            if file_path:
                self.data_manager.uploaded_video = file_path
                messagebox.showinfo("Uploaded", "וידאו הועלה בהצלחה!")
        else:
            file_path = filedialog.askopenfilename(
                title="בחר קובץ תמונה",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
            )
            if file_path:
                self.data_manager.uploaded_image = file_path
                messagebox.showinfo("Uploaded", "תמונה הועלתה בהצלחה!")

    def on_event_type_change(self, event=None):
        event_type = self.data_manager.form_data['event_type'].get()
        vehicle_related_events = ['גניבת רכב', 'צד ג\' - רכב', 'נזק לרכב', 'נזקי פריצה']

        # Remove all optional tabs
        for tab in [self.vehicle_frame, self.third_party_frame]:
            if tab in self.notebook.tabs():
                self.notebook.forget(tab)

        # Add relevant tabs based on event type
        if event_type in vehicle_related_events:
            self.notebook.add(self.vehicle_frame, text='פרטי רכב')
            if event_type == 'צד ג\' - רכב':
                self.notebook.add(self.third_party_frame, text='פרטי צד ג׳')