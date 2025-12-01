# src/data/data_manager.py
"""
Data manager for handling form data persistence and widget value management.
Uses widget handlers for clean separation of concerns.
Supports file-based persistence by claim number.
"""
import json
import os
from tkinter import messagebox

from .widget_handlers import WidgetHandlerFactory
from .file_persistence import FilePersistenceHandler


class DataManager:
    def __init__(self):
        self.form_data = {}
        self.uploaded_video = None
        self.uploaded_image = None
        self.file_persistence = FilePersistenceHandler()
        self.current_claim_number = None

    def load_saved_data(self):
        """
        Loads data from saved_data.json if it exists.
        If the file doesn't exist, it silently continues without error.

        Returns:
            dict: The loaded data dictionary, or None if no data found
        """
        try:
            # Check if save file exists
            if os.path.exists('saved_data.json'):
                # Open and read the file
                with open('saved_data.json', 'r', encoding='utf-8') as f:
                    try:
                        # Load JSON data
                        saved_data = json.load(f)
                        if saved_data:  # Make sure we have data
                            # Pass the loaded data to load_data_from_json
                            self.load_data_from_json(saved_data)
                            print("Data loaded successfully")  # Debug message
                            return saved_data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        messagebox.showwarning(
                            "אזהרה",
                            "קובץ הנתונים השמורים פגום. מתחיל עם טופס ריק."
                        )
                        return None
            else:
                print("No saved data file found")  # Debug message
                # File doesn't exist - that's okay for first run
                return None

        except Exception as e:
            print(f"Error in load_saved_data: {str(e)}")
            messagebox.showwarning(
                "אזהרה",
                f"שגיאה בטעינת נתונים שמורים: {str(e)}"
            )
            return None

    def load_data_from_json(self, saved_data):
        """
        Loads data from a JSON object into the form fields.
        Uses widget handlers for clean, maintainable code.

        Args:
            saved_data (dict): Dictionary containing the saved form data
        """
        if not saved_data:
            print("No data to load")
            return

        try:
            self._load_widget_values(saved_data)
            self._load_file_paths(saved_data)
            print("Data loaded into widgets successfully")

        except Exception as e:
            print(f"Error loading data into widgets: {str(e)}")
            messagebox.showerror(
                "שגיאה",
                f"שגיאה בטעינת הנתונים לטופס: {str(e)}"
            )

    def _load_widget_values(self, saved_data):
        """
        Load values into widgets using appropriate handlers.

        Args:
            saved_data (dict): Dictionary with field names and values
        """
        for key, value in saved_data.items():
            if key not in self.form_data:
                print(f"Field {key} not found in form")
                continue

            widget = self.form_data[key]
            self._set_widget_value(widget, value, key)

    def _set_widget_value(self, widget, value, field_name):
        """
        Set a single widget's value using the appropriate handler.

        Args:
            widget: The Tkinter widget to set value for
            value: The value to set
            field_name: Name of the field (for error reporting)
        """
        try:
            handler = WidgetHandlerFactory.get_handler(widget)
            handler.set_value(widget, value)
        except ValueError as e:
            # Unsupported widget type
            print(f"Cannot set value for {field_name}: {e}")
        except Exception as e:
            print(f"Error setting value for {field_name}: {e}")

    def _load_file_paths(self, saved_data):
        """
        Load file paths from saved data.

        Args:
            saved_data (dict): Dictionary containing saved data
        """
        if 'video_file' in saved_data:
            self.uploaded_video = saved_data['video_file']
        if 'correspondence_image' in saved_data:
            self.uploaded_image = saved_data['correspondence_image']

    def save_data(self):
        """
        Saves the current form data.
        If claim number exists, saves to file-based storage.
        Otherwise falls back to single file.
        """
        try:
            data_to_save = self._collect_widget_values()
            self._add_file_paths_to_save(data_to_save)

            # Get claim number
            claim_number = data_to_save.get('claim_number', '').strip()

            if claim_number:
                # Save to file-based storage (saved_data/claim_number.json)
                self.file_persistence.save_by_claim_number(claim_number, data_to_save)
                self.current_claim_number = claim_number
                messagebox.showinfo("הצלחה", f"הנתונים נשמרו בהצלחה!\nתיק: {claim_number}")
            else:
                # Fallback to single file
                self._write_to_json_file(data_to_save)
                messagebox.showinfo("הצלחה", "הנתונים נשמרו בהצלחה!")

        except Exception as e:
            print(f"Error saving data: {str(e)}")
            messagebox.showerror(
                "שגיאה",
                f"שגיאה בשמירת הנתונים: {str(e)}"
            )

    def load_by_claim_number(self, claim_number):
        """
        Load data for a specific claim number.

        Args:
            claim_number: Claim number to load
        """
        if not claim_number:
            return

        try:
            data = self.file_persistence.load_by_claim_number(claim_number)
            if data:
                self.load_data_from_json(data)
                self.current_claim_number = claim_number
                print(f"Loaded data for claim: {claim_number}")
            else:
                messagebox.showwarning(
                    "לא נמצא",
                    f"לא נמצאו נתונים עבור תיק מספר: {claim_number}"
                )
        except Exception as e:
            print(f"Error loading claim {claim_number}: {e}")
            messagebox.showerror(
                "שגיאה",
                f"שגיאה בטעינת נתוני התיק: {str(e)}"
            )

    def get_recent_claims(self, limit=10):
        """
        Get list of recent claim numbers.

        Args:
            limit: Maximum number of claims to return

        Returns:
            list: List of claim numbers
        """
        all_claims = self.file_persistence.get_all_claim_numbers()
        return all_claims[-limit:] if limit else all_claims

    def _collect_widget_values(self):
        """
        Collect values from all widgets using appropriate handlers.

        Returns:
            dict: Dictionary with field names and their values
        """
        data_to_save = {}
        for key, widget in self.form_data.items():
            try:
                handler = WidgetHandlerFactory.get_handler(widget)
                data_to_save[key] = handler.get_value(widget)
            except ValueError:
                # Unsupported widget type, skip it
                print(f"Skipping unsupported widget type for {key}")
            except Exception as e:
                print(f"Error getting value for {key}: {e}")
        return data_to_save

    def _add_file_paths_to_save(self, data_dict):
        """
        Add file paths to the data dictionary.

        Args:
            data_dict (dict): Dictionary to add file paths to
        """
        if self.uploaded_video:
            data_dict['video_file'] = self.uploaded_video
        if self.uploaded_image:
            data_dict['correspondence_image'] = self.uploaded_image

    def _write_to_json_file(self, data, filename='saved_data.json'):
        """
        Write data dictionary to a JSON file.

        Args:
            data (dict): Data to write
            filename (str): Name of the file to write to
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_field_value(self, field_name):
        """
        Gets the value of a form field using the appropriate handler.

        Args:
            field_name (str): Name of the field to get value from

        Returns:
            str: The field's value, or empty string if not found
        """
        if field_name not in self.form_data:
            return ""

        widget = self.form_data[field_name]
        try:
            handler = WidgetHandlerFactory.get_handler(widget)
            return handler.get_value(widget)
        except Exception as e:
            print(f"Error getting value for {field_name}: {e}")
            return ""

    def set_field_value(self, field_name, value):
        """
        Sets the value of a form field using the appropriate handler.

        Args:
            field_name (str): Name of the field to set value for
            value: The value to set
        """
        if field_name not in self.form_data:
            return

        widget = self.form_data[field_name]
        self._set_widget_value(widget, value, field_name)

    def clear_all_fields(self):
        """
        Clears all form fields using appropriate handlers.
        """
        for widget in self.form_data.values():
            try:
                handler = WidgetHandlerFactory.get_handler(widget)
                handler.clear_value(widget)
            except Exception as e:
                print(f"Error clearing widget: {e}")

        self.uploaded_video = None
        self.uploaded_image = None

    def get_empty_fields(self):
        """
        Get list of field names that are empty.

        Returns:
            list: List of tuples (field_name, hebrew_label) for empty fields
        """
        # Field name to Hebrew label mapping
        field_labels = {
            'event_date': 'תאריך אירוע',
            'claim_number': 'מספר תביעה',
            'full_name': 'שם מלא של המבוטח',
            'policy_number': 'מספר פוליסה',
            'vehicle_company': 'יצרן הרכב',
            'vehicle_color': 'צבע הרכב',
            'vehicle_model': 'דגם הרכב',
            'vehicle_manufacture_year': 'שנת ייצור',
            'vehicle_license_number': 'מספר רישוי',
            'vehicle_engine_type': 'סוג מנוע',
            'vehicle_engine_capacity': 'נפח מנוע',
            'vehicle_engine_power': 'הספק מנוע',
            'vehicle_gearbox': 'סוג גיר',
            'third_party_name': 'שם צד ג\'',
            'third_party_policy_number': 'מספר פוליסה צד ג\'',
            'third_party_contact': 'טלפון צד ג\'',
            'circumstances': 'נסיבות האירוע',
            'investigation': 'החקירה עצמה',
            'summary': 'סיכום'
        }

        empty_fields = []
        for field_name, widget in self.form_data.items():
            try:
                handler = WidgetHandlerFactory.get_handler(widget)
                value = handler.get_value(widget)

                # Check if value is empty (empty string or whitespace only)
                if not value or str(value).strip() == '':
                    hebrew_label = field_labels.get(field_name, field_name)
                    empty_fields.append((field_name, hebrew_label))
            except Exception as e:
                print(f"Error checking field {field_name}: {e}")

        return empty_fields

    def fill_empty_fields_with_placeholder(self, empty_field_names):
        """
        Fill specified empty fields with 'NOT_FILLED' placeholder.

        Args:
            empty_field_names: List of field names to fill
        """
        for field_name in empty_field_names:
            if field_name in self.form_data:
                self.set_field_value(field_name, 'NOT_FILLED')