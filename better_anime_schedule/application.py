import tkinter as tk
import webbrowser
from datetime import date
from tkinter import ttk
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Main application controller"""

    def __init__(self, *args, **kwargs):
        # Main Windows
        super().__init__(*args, **kwargs)
        self.today = date.today()
        self.title("Anime Schedule")
        self.geometry("900x390")
        ttk.Label(self,
                  text="Anime Schedule {}".format(self.today.strftime("%d, %B %Y")),
                  font=("TkDefaultFont", 18, "bold"))\
                  .grid(row=0, column=0, columnspan=2)

        # Data Model
        self.data_model = m.CSVModel()
        self.fields = getattr(self.data_model, 'desc')
        self.rows = self.data_model.get_csv()
        self.callbacks = {'change_img': self.change_img,
                          'open_browser': self.open_browser}

        # Tree Widget
        self.treeview = v.TreeViewInterface(self, columns=self.fields,
                                            callbacks=self.callbacks)
        self.treeview.grid(row=1, column=0, padx=10, pady=50)
        self.treeview.populate(data=self.rows, fields=self.fields) # mark thread

        # Label Widget
        self.label = v.LabelImage(self)
        self.label.grid(row=1, column=1, padx=15)
        self.columnconfigure(index=1, weight=1)

        # Image show
        self.imgkey = getattr(self.data_model, 'imgsrc')
        self.imgsource = self.data_model.get_source(data=self.rows, field=self.imgkey)
        self.photoimage = {}

        # Loop through image url dict
        for index, imgpath in self.imgsource.items(): # mark thread
            self.imgpath = self.data_model.open_image(imgpath)
            self.photoimage[index] = tk.PhotoImage(file=self.imgpath)

        # Get anime url
        self.url_key = getattr(self.data_model, 'redirect')
        self.urlsource = self.data_model.get_source(data=self.rows, field=self.url_key)
        self.url_redirect = {}
        for index, link in self.urlsource.items(): # mark thread
            self.url_redirect[index] = link

        # Status bar
        self.status = tk.Label(self, text="Press enter or double-click on selection will redirect your webbrowser"
                                " to the anime url", font=("Helvetica", 12),
                                relief='sunken', anchor="center")
        self.status.grid(row=2, column=0, columnspan=2,
                         sticky="nsew")


    def change_img(self, *args):
        self.current_img = getattr(self.label, 'thumbnail')
        selected_id = self.treeview.tree.selection()[0]
        self.current_img.config(image=self.photoimage[selected_id])

    def open_browser(self, *args):
        selected_id = self.treeview.tree.selection()[0]
        webbrowser.open(url=self.url_redirect[selected_id],
                        new=1)