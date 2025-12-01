# src/data/widget_handlers/base_handler.py
"""
Base class for widget handlers and factory for creating appropriate handlers.
"""
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from typing import Any


class BaseWidgetHandler(ABC):
    """
    Abstract base class for widget handlers.
    Each handler manages a specific type of Tkinter widget.
    """

    @abstractmethod
    def get_value(self, widget: Any) -> Any:
        """
        Get the current value from the widget.

        Args:
            widget: The Tkinter widget to get value from

        Returns:
            The widget's current value
        """
        pass

    @abstractmethod
    def set_value(self, widget: Any, value: Any) -> None:
        """
        Set a value to the widget.

        Args:
            widget: The Tkinter widget to set value to
            value: The value to set
        """
        pass

    @abstractmethod
    def clear_value(self, widget: Any) -> None:
        """
        Clear the widget's value.

        Args:
            widget: The Tkinter widget to clear
        """
        pass


class WidgetHandlerFactory:
    """
    Factory class for creating appropriate widget handlers.
    """

    @staticmethod
    def get_handler(widget: Any) -> BaseWidgetHandler:
        """
        Get the appropriate handler for the given widget type.

        Args:
            widget: The Tkinter widget to get handler for

        Returns:
            An instance of the appropriate widget handler

        Raises:
            ValueError: If widget type is not supported
        """
        # Import handlers here to avoid circular imports
        from .text_widget_handler import TextWidgetHandler
        from .entry_widget_handler import EntryWidgetHandler
        from .combobox_widget_handler import ComboboxWidgetHandler
        from .date_widget_handler import DateWidgetHandler

        # Check for DateEntry first (before Entry, as it might inherit from it)
        widget_class_name = widget.__class__.__name__
        if widget_class_name == 'DateEntry':
            return DateWidgetHandler()

        # Check for Text widget
        if isinstance(widget, tk.Text):
            return TextWidgetHandler()

        # Check for Combobox (before Entry, as Combobox inherits from Entry)
        if isinstance(widget, ttk.Combobox):
            return ComboboxWidgetHandler()

        # Check for Entry
        if isinstance(widget, (ttk.Entry, tk.Entry)):
            return EntryWidgetHandler()

        # Unsupported widget type
        raise ValueError(
            f"Unsupported widget type: {type(widget).__name__}. "
            f"Supported types: Text, Entry, Combobox, DateEntry"
        )
