# gui/utils.py
import tkinter as tk
from tkinter import ttk

def create_scrollable_frame(parent):
    """
    Creates a scrollable frame within the given parent widget.
    
    Args:
        parent: The parent widget to contain the scrollable frame
        
    Returns:
        ttk.Frame: The scrollable frame where widgets can be placed
    """
    # Create a canvas and scrollbar
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    
    # Create the scrollable frame within the canvas
    scrollable_frame = ttk.Frame(canvas)
    
    # Configure the canvas to scroll the frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Create a window in the canvas that contains the frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Add mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    # Bind mouse wheel event to the canvas
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Configure grid weight
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    
    # Position the canvas and scrollbar using grid
    canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    return scrollable_frame

def create_labeled_entry(parent, label_text, row, column=0, entry_width=40):
    """
    Creates a label and entry widget pair.
    
    Args:
        parent: The parent widget
        label_text: Text for the label
        row: Grid row for placement
        column: Starting grid column for placement
        entry_width: Width of the entry widget
        
    Returns:
        tuple: (ttk.Label, ttk.Entry) The created label and entry widgets
    """
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=column + 1, padx=5, pady=5, sticky='e')
    
    entry = ttk.Entry(parent, width=entry_width)
    entry.grid(row=row, column=column, padx=5, pady=5, sticky='ew')
    
    return label, entry

def create_labeled_combobox(parent, label_text, values, row, column=0, width=37):
    """
    Creates a label and combobox widget pair.
    
    Args:
        parent: The parent widget
        label_text: Text for the label
        values: List of values for the combobox
        row: Grid row for placement
        column: Starting grid column for placement
        width: Width of the combobox widget
        
    Returns:
        tuple: (ttk.Label, ttk.Combobox) The created label and combobox widgets
    """
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=column + 1, padx=5, pady=5, sticky='e')
    
    combobox = ttk.Combobox(parent, values=values, width=width, state='readonly')
    combobox.grid(row=row, column=column, padx=5, pady=5, sticky='ew')
    
    return label, combobox

def create_labeled_text(parent, label_text, row, column=0, width=40, height=5):
    """
    Creates a label and text widget pair.
    
    Args:
        parent: The parent widget
        label_text: Text for the label
        row: Grid row for placement
        column: Starting grid column for placement
        width: Width of the text widget
        height: Height of the text widget
        
    Returns:
        tuple: (ttk.Label, tk.Text) The created label and text widgets
    """
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=column + 1, padx=5, pady=5, sticky='e')
    
    text_widget = tk.Text(parent, width=width, height=height)
    text_widget.grid(row=row, column=column, padx=5, pady=5, sticky='ew')
    
    return label, text_widget

def create_labeled_date_entry(parent, label_text, row, column=0, width=37):
    """
    Creates a label and date entry widget pair.
    
    Args:
        parent: The parent widget
        label_text: Text for the label
        row: Grid row for placement
        column: Starting grid column for placement
        width: Width of the date entry widget
        
    Returns:
        tuple: (ttk.Label, DateEntry) The created label and date entry widgets
    """
    from tkcalendar import DateEntry
    
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=column + 1, padx=5, pady=5, sticky='e')
    
    date_entry = DateEntry(parent, width=width, background='darkblue',
                          foreground='white', borderwidth=2,
                          date_pattern='dd/mm/yyyy')
    date_entry.grid(row=row, column=column, padx=5, pady=5, sticky='ew')
    
    return label, date_entry

def configure_grid_weights(widget):
    """
    Configures grid weights for a widget to make it responsive.
    
    Args:
        widget: The widget to configure
    """
    widget.grid_columnconfigure(0, weight=1)
    for i in range(widget.grid_size()[1]):
        widget.grid_rowconfigure(i, weight=1)

def set_widget_state(widget, state):
    """
    Recursively sets the state of a widget and all its children.
    
    Args:
        widget: The widget to configure
        state: The state to set ('normal', 'disabled', or 'readonly')
    """
    if hasattr(widget, 'state'):
        try:
            widget.state([state])
        except:
            pass
    elif hasattr(widget, 'configure'):
        try:
            widget.configure(state=state)
        except:
            pass
            
    for child in widget.winfo_children():
        set_widget_state(child, state)