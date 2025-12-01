# src/data/widget_handlers/text_widget_handler.py
"""Handler for tk.Text widgets."""
import tkinter as tk
from .base_handler import BaseWidgetHandler


class TextWidgetHandler(BaseWidgetHandler):
    """Handler for tk.Text multi-line text widgets."""

    def get_value(self, widget: tk.Text) -> str:
        """Get text content from Text widget."""
        return widget.get('1.0', 'end-1c').strip()

    def set_value(self, widget: tk.Text, value: str) -> None:
        """Set text content in Text widget."""
        widget.delete('1.0', tk.END)
        if value:
            widget.insert('1.0', str(value))

    def clear_value(self, widget: tk.Text) -> None:
        """Clear Text widget content."""
        widget.delete('1.0', tk.END)
