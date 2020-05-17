import tkinter as tk
from tkinter import ttk


class TreeViewInterface(tk.Frame):
    """Treeview Widget Showing CSV data"""

    def __init__(self, parent, columns, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columns = columns
        self.callbacks = callbacks
        # Create base tree
        self.tree = ttk.Treeview(self, columns=self.columns,
                                 show='headings', selectmode='browse')

        # Columns
        for field in self.columns:
            self.tree.heading(field, text=field.title())
            self.tree.column(field, anchor="w", stretch=True,
                             width=300 if field=="Name" else 100)

        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind("<<TreeviewSelect>>", self.callbacks['change_img'])
        self.tree.bind("<<TreeviewOpen>>", self.callbacks['open_browser'])

    def populate(self, data, fields):
        # Delete everything, before populate
        self.tree.delete()

        for iid, row in enumerate(data):
            values = [row[key] for key in fields]
            # get image path
            self.tree.insert(parent='', index='end',
                             iid=str(iid), values=values)



class LabelImage(tk.Frame):
    """Label showing image"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.thumbnail = ttk.Label(self)
        self.thumbnail.grid(row=0, column=0)






