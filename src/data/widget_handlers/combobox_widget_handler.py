# src/data/widget_handlers/combobox_widget_handler.py
"""Handler for ttk.Combobox widgets."""
import tkinter as tk
from tkinter import ttk
from .base_handler import BaseWidgetHandler


class ComboboxWidgetHandler(BaseWidgetHandler):
    """Handler for ttk.Combobox dropdown widgets."""

    def get_value(self, widget: ttk.Combobox) -> str:
        """Get selected value from Combobox widget."""
        return widget.get()

    def set_value(self, widget: ttk.Combobox, value: str) -> None:
        """Set selected value in Combobox widget."""
        # Validate value is in combobox values if possible
        if hasattr(widget, 'cget'):
            values = widget.cget('values')
            if values and value not in values:
                # Still set it, but it might not be ideal
                pass
        widget.set(value)

    def clear_value(self, widget: ttk.Combobox) -> None:
        """Clear Combobox widget selection."""
        widget.set('')
