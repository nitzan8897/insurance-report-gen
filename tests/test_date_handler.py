# tests/test_date_handler.py
"""
Comprehensive tests for DateWidgetHandler.
"""
import unittest
import tkinter as tk
from datetime import datetime
from tkcalendar import DateEntry

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.widget_handlers.date_widget_handler import DateWidgetHandler


class TestDateWidgetHandler(unittest.TestCase):
    """Test DateWidgetHandler functionality."""

    def setUp(self):
        """Create a hidden root window and handler for testing."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.handler = DateWidgetHandler()
        self.widget = DateEntry(self.root)

    def tearDown(self):
        """Destroy the root window after tests."""
        self.root.destroy()

    def test_get_value_returns_correct_format(self):
        """Test that get_value returns date in dd/mm/yyyy format."""
        test_date = datetime(2024, 10, 25)
        self.widget.set_date(test_date)
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '25/10/2024')

    def test_set_value_with_datetime_object(self):
        """Test setting date with datetime object."""
        test_date = datetime(2024, 12, 1)
        self.handler.set_value(self.widget, test_date)
        result = self.widget.get_date()
        self.assertEqual(result, test_date.date())

    def test_set_value_with_dd_mm_yyyy_format(self):
        """Test setting date with dd/mm/yyyy string format."""
        self.handler.set_value(self.widget, '25/10/2024')
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '25/10/2024')

    def test_set_value_with_yyyy_mm_dd_format(self):
        """Test setting date with yyyy-mm-dd string format."""
        self.handler.set_value(self.widget, '2024-10-25')
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '25/10/2024')

    def test_set_value_with_dd_dot_mm_dot_yyyy_format(self):
        """Test setting date with dd.mm.yyyy string format."""
        self.handler.set_value(self.widget, '25.10.2024')
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '25/10/2024')

    def test_set_value_with_dd_dash_mm_dash_yyyy_format(self):
        """Test setting date with dd-mm-yyyy string format."""
        self.handler.set_value(self.widget, '25-10-2024')
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '25/10/2024')

    def test_set_value_with_empty_string(self):
        """Test that setting empty string doesn't crash."""
        original_date = self.widget.get_date()
        self.handler.set_value(self.widget, '')
        # Date should remain unchanged
        self.assertEqual(self.widget.get_date(), original_date)

    def test_set_value_with_none(self):
        """Test that setting None doesn't crash."""
        original_date = self.widget.get_date()
        self.handler.set_value(self.widget, None)
        # Date should remain unchanged
        self.assertEqual(self.widget.get_date(), original_date)

    def test_set_value_with_invalid_format(self):
        """Test that invalid date format doesn't crash."""
        original_date = self.widget.get_date()
        self.handler.set_value(self.widget, 'invalid-date')
        # Date should remain unchanged
        self.assertEqual(self.widget.get_date(), original_date)

    def test_clear_value_sets_current_date(self):
        """Test that clear_value resets to current date."""
        # Set a specific date
        self.widget.set_date(datetime(2020, 1, 1))
        # Clear it
        self.handler.clear_value(self.widget)
        # Should be today
        result = self.widget.get_date()
        today = datetime.now().date()
        self.assertEqual(result, today)

    def test_parse_date_string_with_all_formats(self):
        """Test _parse_date_string with all supported formats."""
        test_cases = [
            ('25/10/2024', datetime(2024, 10, 25)),
            ('2024-10-25', datetime(2024, 10, 25)),
            ('25.10.2024', datetime(2024, 10, 25)),
            ('25-10-2024', datetime(2024, 10, 25)),
        ]

        for date_str, expected in test_cases:
            with self.subTest(date_str=date_str):
                result = self.handler._parse_date_string(date_str)
                self.assertEqual(result, expected)

    def test_parse_date_string_returns_none_for_invalid(self):
        """Test that _parse_date_string returns None for invalid dates."""
        result = self.handler._parse_date_string('not-a-date')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
