# tests/test_text_handler.py
"""
Tests for TextWidgetHandler.
"""
import unittest
import tkinter as tk

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.widget_handlers.text_widget_handler import TextWidgetHandler


class TestTextWidgetHandler(unittest.TestCase):
    """Test TextWidgetHandler functionality."""

    def setUp(self):
        """Create a hidden root window and handler for testing."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.handler = TextWidgetHandler()
        self.widget = tk.Text(self.root)

    def tearDown(self):
        """Destroy the root window after tests."""
        self.root.destroy()

    def test_get_value_returns_text_content(self):
        """Test that get_value returns text content."""
        test_text = "This is test content"
        self.widget.insert('1.0', test_text)
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, test_text)

    def test_get_value_strips_trailing_whitespace(self):
        """Test that get_value strips trailing whitespace."""
        test_text = "Content with spaces   \n\n"
        self.widget.insert('1.0', test_text)
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, "Content with spaces")

    def test_get_value_returns_empty_string_for_empty_widget(self):
        """Test that get_value returns empty string for empty widget."""
        result = self.handler.get_value(self.widget)
        self.assertEqual(result, '')

    def test_set_value_inserts_text(self):
        """Test that set_value inserts text correctly."""
        test_text = "New content"
        self.handler.set_value(self.widget, test_text)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, test_text)

    def test_set_value_replaces_existing_text(self):
        """Test that set_value replaces existing text."""
        self.widget.insert('1.0', "Old content")
        self.handler.set_value(self.widget, "New content")
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, "New content")

    def test_set_value_with_multiline_text(self):
        """Test that set_value handles multiline text."""
        test_text = "Line 1\nLine 2\nLine 3"
        self.handler.set_value(self.widget, test_text)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, test_text)

    def test_set_value_with_hebrew_text(self):
        """Test that set_value handles Hebrew text."""
        test_text = "טקסט בעברית"
        self.handler.set_value(self.widget, test_text)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, test_text)

    def test_set_value_with_empty_string(self):
        """Test that set_value with empty string clears widget."""
        self.widget.insert('1.0', "Some content")
        self.handler.set_value(self.widget, "")
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, '')

    def test_set_value_with_none_does_not_insert(self):
        """Test that set_value with None doesn't insert anything."""
        self.widget.insert('1.0', "Original")
        self.handler.set_value(self.widget, None)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, '')  # Should be cleared

    def test_set_value_converts_non_string_to_string(self):
        """Test that set_value converts non-string values to strings."""
        self.handler.set_value(self.widget, 12345)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, '12345')

    def test_clear_value_removes_all_content(self):
        """Test that clear_value removes all content."""
        self.widget.insert('1.0', "Content to clear")
        self.handler.clear_value(self.widget)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, '')

    def test_clear_value_on_empty_widget(self):
        """Test that clear_value works on empty widget."""
        self.handler.clear_value(self.widget)
        result = self.widget.get('1.0', 'end-1c')
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
