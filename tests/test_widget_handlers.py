# tests/test_widget_handlers.py
"""
Tests for widget handler factory and base classes.
"""
import unittest
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.widget_handlers import WidgetHandlerFactory
from src.data.widget_handlers.text_widget_handler import TextWidgetHandler
from src.data.widget_handlers.entry_widget_handler import EntryWidgetHandler
from src.data.widget_handlers.combobox_widget_handler import ComboboxWidgetHandler
from src.data.widget_handlers.date_widget_handler import DateWidgetHandler


class TestWidgetHandlerFactory(unittest.TestCase):
    """Test the widget handler factory returns correct handlers."""

    def setUp(self):
        """Create a hidden root window for widget testing."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window

    def tearDown(self):
        """Destroy the root window after tests."""
        self.root.destroy()

    def test_factory_returns_text_handler_for_text_widget(self):
        """Test that factory returns TextWidgetHandler for tk.Text widgets."""
        widget = tk.Text(self.root)
        handler = WidgetHandlerFactory.get_handler(widget)
        self.assertIsInstance(handler, TextWidgetHandler)

    def test_factory_returns_entry_handler_for_entry_widget(self):
        """Test that factory returns EntryWidgetHandler for ttk.Entry widgets."""
        widget = ttk.Entry(self.root)
        handler = WidgetHandlerFactory.get_handler(widget)
        self.assertIsInstance(handler, EntryWidgetHandler)

    def test_factory_returns_combobox_handler_for_combobox_widget(self):
        """Test that factory returns ComboboxWidgetHandler for ttk.Combobox widgets."""
        widget = ttk.Combobox(self.root)
        handler = WidgetHandlerFactory.get_handler(widget)
        self.assertIsInstance(handler, ComboboxWidgetHandler)

    def test_factory_returns_date_handler_for_date_widget(self):
        """Test that factory returns DateWidgetHandler for DateEntry widgets."""
        widget = DateEntry(self.root)
        handler = WidgetHandlerFactory.get_handler(widget)
        self.assertIsInstance(handler, DateWidgetHandler)

    def test_factory_raises_error_for_unknown_widget_type(self):
        """Test that factory raises ValueError for unsupported widget types."""
        widget = tk.Label(self.root, text="test")
        with self.assertRaises(ValueError) as context:
            WidgetHandlerFactory.get_handler(widget)
        self.assertIn("Unsupported widget type", str(context.exception))


if __name__ == '__main__':
    unittest.main()
