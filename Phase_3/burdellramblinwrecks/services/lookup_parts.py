from tkinter import *
from model.dao import Dao
from services.add_vehicle import AddVehicleService
from ui.searchbox import SearchBox
from ui.table_sheet import TableSheet
from services.public_page_service import PublicPageService
from datetime import datetime


class LookupParts:

    def __init__(self, window):
        self.root = window
        self.dao = Dao().get_instance()
        self.table = None
        self.message = None
        self.view_parts_page = None

    def list_vehicle_parts(self, filter_text, window):

        records = self.dao.get_all_vehicle_parts(filter_text)
        if len(records) > 0:
                if self.table is not None:
                    self.table.sdem.destroy()
                self.table = TableSheet(records,["Part Number", "Cost", "Description"],window)
                if self.message is not None:
                    self.message.destroy()
                    self.message = None
        else:
            if self.message is None:
                self.message = Label(self.view_parts_page, text="Sorry, it looks like we don’t have that in stock!", bg="#e2e8f0")
                self.message.pack()

    def show_vehicle_parts(self):
        public_screen = Toplevel(self.root)
        public_screen.title("Lookup Parts")
        public_screen.geometry("1300x1000")
        Label(public_screen, text="List of Parts", bg="#ADD8E6").pack()
        SearchBox(public_screen, command=self.list_vehicle_parts, command_arguments=(public_screen),
                  placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)
        self.view_parts_page = public_screen