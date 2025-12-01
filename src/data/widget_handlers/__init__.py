# src/data/widget_handlers/__init__.py
"""
Widget handlers for managing different types of Tkinter widgets.
Each handler provides a consistent interface for getting and setting widget values.
"""

from .base_handler import BaseWidgetHandler, WidgetHandlerFactory

__all__ = ['BaseWidgetHandler', 'WidgetHandlerFactory']
