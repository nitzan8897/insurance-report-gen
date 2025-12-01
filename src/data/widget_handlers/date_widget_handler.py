# src/data/widget_handlers/date_widget_handler.py
"""Handler for DateEntry widgets from tkcalendar."""
from datetime import datetime
from typing import Union
from .base_handler import BaseWidgetHandler


class DateWidgetHandler(BaseWidgetHandler):
    """Handler for tkcalendar DateEntry widgets."""

    # Supported date formats for parsing
    DATE_FORMATS = ['%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y', '%d-%m-%Y']

    def get_value(self, widget) -> str:
        """
        Get date from DateEntry widget as formatted string.

        Args:
            widget: DateEntry widget

        Returns:
            Date formatted as dd/mm/yyyy
        """
        try:
            return widget.get_date().strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Error getting date value: {e}")
            return ''

    def set_value(self, widget, value: Union[str, datetime]) -> None:
        """
        Set date in DateEntry widget.

        Args:
            widget: DateEntry widget
            value: Date as string or datetime object
        """
        if not value:
            return

        try:
            if isinstance(value, datetime):
                widget.set_date(value)
            elif isinstance(value, str):
                date_obj = self._parse_date_string(value)
                if date_obj:
                    widget.set_date(date_obj)
        except Exception as e:
            print(f"Error setting date value: {e}")

    def clear_value(self, widget) -> None:
        """
        Reset DateEntry widget to current date.

        Args:
            widget: DateEntry widget
        """
        widget.set_date(datetime.now())

    def _parse_date_string(self, date_str: str) -> Union[datetime, None]:
        """
        Parse date string trying multiple formats.

        Args:
            date_str: Date string to parse

        Returns:
            datetime object if parsing successful, None otherwise
        """
        for date_format in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue

        print(f"Could not parse date: {date_str}")
        return None
