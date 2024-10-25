# src/data/data_manager.py
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class DataManager:
    def __init__(self):
        self.form_data = {}
        self.uploaded_video = None
        self.uploaded_image = None

    def load_saved_data(self):
        """
        Loads data from saved_data.json if it exists.
        If the file doesn't exist, it silently continues without error.
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
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        messagebox.showwarning(
                            "אזהרה", 
                            "קובץ הנתונים השמורים פגום. מתחיל עם טופס ריק."
                        )
            else:
                print("No saved data file found")  # Debug message
                # File doesn't exist - that's okay for first run
                pass
                
        except Exception as e:
            print(f"Error in load_saved_data: {str(e)}")
            messagebox.showwarning(
                "אזהרה",
                f"שגיאה בטעינת נתונים שמורים: {str(e)}"
            )

    def load_data_from_json(self, saved_data):
        """
        Loads data from a JSON object into the form fields.
        
        Args:
            saved_data (dict): Dictionary containing the saved form data
        """
        if not saved_data:  # If saved_data is None or empty
            print("No data to load")  # Debug message
            return

        try:
            # Iterate through the saved data
            for key, value in saved_data.items():
                # Skip if the field doesn't exist in the form
                if key not in self.form_data:
                    print(f"Field {key} not found in form")  # Debug message
                    continue

                widget = self.form_data[key]
                
                # Handle different widget types
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
                    if value:
                        widget.insert('1.0', value)

                elif isinstance(widget, DateEntry):
                    try:
                        if value:
                            if isinstance(value, str):
                                # Try different date formats
                                for date_format in ['%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y']:
                                    try:
                                        date_obj = datetime.strptime(value, date_format)
                                        widget.set_date(date_obj)
                                        break
                                    except ValueError:
                                        continue
                    except Exception as e:
                        print(f"Error setting date for {key}: {str(e)}")

                elif isinstance(widget, ttk.Combobox):
                    if value in widget['values']:
                        widget.set(value)
                    else:
                        widget.set(value)

                elif isinstance(widget, (ttk.Entry, tk.Entry)):
                    widget.delete(0, tk.END)
                    if value:
                        widget.insert(0, str(value))

            # Handle file paths separately
            if 'video_file' in saved_data:
                self.uploaded_video = saved_data['video_file']
            if 'correspondence_image' in saved_data:
                self.uploaded_image = saved_data['correspondence_image']

            print("Data loaded into widgets successfully")  # Debug message

        except Exception as e:
            print(f"Error loading data into widgets: {str(e)}")
            messagebox.showerror(
                "שגיאה",
                f"שגיאה בטעינת הנתונים לטופס: {str(e)}"
            )

    def save_data(self):
        """Saves the current form data to a JSON file."""
        try:
            data_to_save = {}
            
            for key, widget in self.form_data.items():
                # Get values based on widget type
                if isinstance(widget, tk.Text):
                    data_to_save[key] = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, DateEntry):
                    data_to_save[key] = widget.get_date().strftime('%d/%m/%Y')
                elif isinstance(widget, (ttk.Entry, tk.Entry, ttk.Combobox)):
                    data_to_save[key] = widget.get()

            # Add file paths
            if self.uploaded_video:
                data_to_save['video_file'] = self.uploaded_video
            if self.uploaded_image:
                data_to_save['correspondence_image'] = self.uploaded_image

            # Save to file
            with open('saved_data.json', 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("הצלחה", "הנתונים נשמרו בהצלחה!")

        except Exception as e:
            print(f"Error saving data: {str(e)}")
            messagebox.showerror(
                "שגיאה", 
                f"שגיאה בשמירת הנתונים: {str(e)}"
            )

    def get_field_value(self, field_name):
        """Gets the value of a form field."""
        if field_name in self.form_data:
            widget = self.form_data[field_name]
            
            if isinstance(widget, tk.Text):
                return widget.get("1.0", tk.END).strip()
            elif isinstance(widget, DateEntry):
                return widget.get_date().strftime("%d.%m.%Y")
            elif isinstance(widget, (ttk.Entry, tk.Entry, ttk.Combobox)):
                return widget.get()
        
        return ""

    def set_field_value(self, field_name, value):
        """Sets the value of a form field."""
        if field_name not in self.form_data:
            return

        widget = self.form_data[field_name]

        try:
            if isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
                if value:
                    widget.insert('1.0', str(value))

            elif isinstance(widget, DateEntry):
                if value:
                    if isinstance(value, str):
                        try:
                            date_obj = datetime.strptime(value, '%d/%m/%Y')
                            widget.set_date(date_obj)
                        except ValueError:
                            print(f"Invalid date format for {field_name}: {value}")
                    else:
                        widget.set_date(value)

            elif isinstance(widget, ttk.Combobox):
                if value in widget['values']:
                    widget.set(value)
                else:
                    widget.set(value)

            elif isinstance(widget, (ttk.Entry, tk.Entry)):
                widget.delete(0, tk.END)
                if value:
                    widget.insert(0, str(value))

        except Exception as e:
            print(f"Error setting value for {field_name}: {str(e)}")

    def clear_all_fields(self):
        """Clears all form fields."""
        for widget in self.form_data.values():
            if isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            elif isinstance(widget, (ttk.Entry, tk.Entry, ttk.Combobox)):
                widget.delete(0, tk.END)
            elif isinstance(widget, DateEntry):
                widget.set_date(datetime.now())

        self.uploaded_video = None
        self.uploaded_image = None