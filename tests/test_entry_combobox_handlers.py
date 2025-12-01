# tests/test_entry_combobox_handlers.py
"""
Tests for EntryWidgetHandler and ComboboxWidgetHandler.
"""
import unittest
import tkinter as tk
from tkinter import ttk

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.widget_handlers.entry_widget_handler import EntryWidgetHandler
from src.data.widget_handlers.combobox_widget_handler import ComboboxWidgetHandler


class TestEntryWidgetHandler(unittest.TestCase):
    """Test EntryWidgetHandler functionality."""

    def setUp(self):
        """Create a hidden root window and handler for testing."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.handler = EntryWidgetHandler()
        self.widget = ttk.Entry(self.root)

    def tearDown(self):
        """Destroy the root window after tests."""
        self.root.destroy()

    def test_get_value_returns_text(self):
        """Test that get_value returns text from entry."""
        test_text = "Test entry value"
        self.widget.insert(0, test_text)
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, test_text)

    def test_set_value_inserts_text(self):
        """Test that set_value inserts text correctly."""
        test_text = "New value"
        self.handler.set_value(self.widget, test_text)
        result = self.widget.get()
        self.assertEqual(result, test_text)

    def test_set_value_replaces_existing_text(self):
        """Test that set_value replaces existing text."""
        self.widget.insert(0, "Old value")
        self.handler.set_value(self.widget, "New value")
        result = self.widget.get()
        self.assertEqual(result, "New value")

    def test_set_value_with_hebrew_text(self):
        """Test that set_value handles Hebrew text."""
        test_text = "ערך בעברית"
        self.handler.set_value(self.widget, test_text)
        result = self.widget.get()
        self.assertEqual(result, test_text)

    def test_set_value_converts_to_string(self):
        """Test that set_value converts values to strings."""
        self.handler.set_value(self.widget, 42)
        result = self.widget.get()
        self.assertEqual(result, '42')

    def test_clear_value_removes_content(self):
        """Test that clear_value removes all content."""
        self.widget.insert(0, "Content")
        self.handler.clear_value(self.widget)
        result = self.widget.get()
        self.assertEqual(result, '')


class TestComboboxWidgetHandler(unittest.TestCase):
    """Test ComboboxWidgetHandler functionality."""

    def setUp(self):
        """Create a hidden root window and handler for testing."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.handler = ComboboxWidgetHandler()
        self.widget = ttk.Combobox(self.root, values=['Option 1', 'Option 2', 'Option 3'])

    def tearDown(self):
        """Destroy the root window after tests."""
        self.root.destroy()

    def test_get_value_returns_selected_value(self):
        """Test that get_value returns selected value."""
        self.widget.set('Option 2')
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, 'Option 2')

    def test_set_value_sets_selection(self):
        """Test that set_value sets the selection."""
        self.handler.set_value(self.widget, 'Option 3')
        result = self.widget.get()
        self.assertEqual(result, 'Option 3')

    def test_set_value_with_value_not_in_list(self):
        """Test that set_value works even with value not in dropdown list."""
        # This is needed for backward compatibility with saved data
        self.handler.set_value(self.widget, 'Custom Value')
        result = self.widget.get()
        self.assertEqual(result, 'Custom Value')

    def test_set_value_replaces_existing_selection(self):
        """Test that set_value replaces existing selection."""
        self.widget.set('Option 1')
        self.handler.set_value(self.widget, 'Option 2')
        result = self.widget.get()
        self.assertEqual(result, 'Option 2')

    def test_set_value_with_hebrew_option(self):
        """Test that set_value handles Hebrew options."""
        hebrew_widget = ttk.Combobox(self.root, values=['אופציה 1', 'אופציה 2'])
        self.handler.set_value(hebrew_widget, 'אופציה 2')
        result = hebrew_widget.get()
        self.assertEqual(result, 'אופציה 2')

    def test_clear_value_removes_selection(self):
        """Test that clear_value removes the selection."""
        self.widget.set('Option 1')
        self.handler.clear_value(self.widget)
        result = self.widget.get()
        self.assertEqual(result, '')

    def test_get_value_returns_empty_string_when_nothing_selected(self):
        """Test that get_value returns empty string when nothing selected."""
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
