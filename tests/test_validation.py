# tests/test_validation.py
"""
Unit tests for form validation functionality.
Tests empty field detection and placeholder filling.
"""
import unittest
import tkinter as tk
from src.data.data_manager import DataManager


class TestFormValidation(unittest.TestCase):
    """Test form validation features."""

    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = DataManager()
        # Create a hidden root window for tkinter widgets
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        """Clean up after tests."""
        self.root.destroy()

    def test_get_empty_fields_with_all_empty(self):
        """Test getting empty fields when all fields are empty."""
        # Create tkinter Entry widgets with empty values
        entry1 = tk.Entry(self.root)
        entry1.insert(0, "")

        entry2 = tk.Entry(self.root)
        entry2.insert(0, "   ")  # Whitespace only

        # Add to form_data
        self.data_manager.form_data['claim_number'] = entry1
        self.data_manager.form_data['full_name'] = entry2

        # Get empty fields
        empty_fields = self.data_manager.get_empty_fields()

        # Should find both fields empty
        self.assertEqual(len(empty_fields), 2)
        field_names = [name for name, _ in empty_fields]
        self.assertIn('claim_number', field_names)
        self.assertIn('full_name', field_names)

    def test_get_empty_fields_with_some_filled(self):
        """Test getting empty fields when some fields are filled."""
        # Create tkinter Entry widgets
        entry_filled = tk.Entry(self.root)
        entry_filled.insert(0, "12345")

        entry_empty = tk.Entry(self.root)
        entry_empty.insert(0, "")

        # Add to form_data
        self.data_manager.form_data['claim_number'] = entry_filled
        self.data_manager.form_data['full_name'] = entry_empty

        # Get empty fields
        empty_fields = self.data_manager.get_empty_fields()

        # Should find only one field empty
        self.assertEqual(len(empty_fields), 1)
        self.assertEqual(empty_fields[0][0], 'full_name')

    def test_get_empty_fields_with_all_filled(self):
        """Test getting empty fields when all fields are filled."""
        # Create tkinter Entry widgets with values
        entry1 = tk.Entry(self.root)
        entry1.insert(0, "12345")

        entry2 = tk.Entry(self.root)
        entry2.insert(0, "John Doe")

        # Add to form_data
        self.data_manager.form_data['claim_number'] = entry1
        self.data_manager.form_data['full_name'] = entry2

        # Get empty fields
        empty_fields = self.data_manager.get_empty_fields()

        # Should find no empty fields
        self.assertEqual(len(empty_fields), 0)

    def test_hebrew_labels_returned(self):
        """Test that Hebrew labels are returned for empty fields."""
        # Create empty Entry widget
        entry_empty = tk.Entry(self.root)
        entry_empty.insert(0, "")

        # Add to form_data
        self.data_manager.form_data['claim_number'] = entry_empty

        # Get empty fields
        empty_fields = self.data_manager.get_empty_fields()

        # Check Hebrew label is returned
        self.assertEqual(len(empty_fields), 1)
        field_name, hebrew_label = empty_fields[0]
        self.assertEqual(field_name, 'claim_number')
        self.assertEqual(hebrew_label, 'מספר תביעה')

    def test_fill_empty_fields_with_placeholder(self):
        """Test filling empty fields with NOT_FILLED placeholder."""
        # Create Entry widget
        entry = tk.Entry(self.root)
        entry.insert(0, "")

        # Add to form_data
        self.data_manager.form_data['claim_number'] = entry

        # Fill with placeholder
        self.data_manager.fill_empty_fields_with_placeholder(['claim_number'])

        # Verify value was set to NOT_FILLED
        self.assertEqual(entry.get(), 'NOT_FILLED')

    def test_text_widget_empty_detection(self):
        """Test empty field detection works for Text widgets."""
        # Create Text widget (multi-line)
        text_widget = tk.Text(self.root, height=5)
        text_widget.insert('1.0', '')

        # Add to form_data
        self.data_manager.form_data['circumstances'] = text_widget

        # Get empty fields
        empty_fields = self.data_manager.get_empty_fields()

        # Should find field empty
        self.assertEqual(len(empty_fields), 1)
        self.assertEqual(empty_fields[0][0], 'circumstances')


if __name__ == '__main__':
    unittest.main()
