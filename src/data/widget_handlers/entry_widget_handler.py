# src/data/widget_handlers/entry_widget_handler.py
"""Handler for ttk.Entry widgets."""
import tkinter as tk
from tkinter import ttk
from .base_handler import BaseWidgetHandler


class EntryWidgetHandler(BaseWidgetHandler):
    """Handler for ttk.Entry single-line text input widgets."""

    def get_value(self, widget: ttk.Entry) -> str:
        """Get text from Entry widget."""
        return widget.get()

    def set_value(self, widget: ttk.Entry, value: str) -> None:
        """Set text in Entry widget."""
        widget.delete(0, tk.END)
        if value:
            widget.insert(0, str(value))

    def clear_value(self, widget: ttk.Entry) -> None:
        """Clear Entry widget content."""
        widget.delete(0, tk.END)
