from tkinter import *
from tksheet import Sheet
class TableSheet:
    def __init__(self, records, headers,window):
        self.records = records
        self.sdem = Sheet(window,
                          width=1000,
                          height=500,
                          align="w",
                          header_align="center",
                          row_index_align="center",
                          show=True,
                          column_width=180,
                          row_index_width=50,
                          data_reference=records,
                          headers=headers)
        self.sdem.enable_bindings(("single",
                                   "drag_select",
                                   "column_drag_and_drop",
                                   "row_drag_and_drop",
                                   "column_select",
                                   "row_select",
                                   "column_width_resize",
                                   "double_click_column_resize",
                                   "row_width_resize",
                                   "column_height_resize",
                                   "arrowkeys",
                                   "row_height_resize",
                                   "double_click_row_resize"))
        self.sdem.edit_bindings(True)
        self.sdem.pack()
