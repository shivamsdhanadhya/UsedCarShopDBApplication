from tkinter import *
from tksheet import Sheet
class CustomizedSheet(Tk):

    def __init__(self, records, headers, title, rows=None):
        Tk.__init__(self)
        self.title(title)
        self.state("zoomed")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.data = [["Row {r} Column {c}" for c in range(100)] for r in range(5000)]
        self.sdem = Sheet(self,
                          width=1000,
                          height=700,
                          align="w",
                          header_align="center",
                          row_index_align="center",
                          show=True,
                          column_width=230,
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
        self.sdem.grid(row=0, column=0, sticky="nswe")
        if rows is not None:
            for row_no in rows:
                for col in range(0, len(headers)):
                    self.sdem.highlight_cells(row=row_no, column=col, bg="#EC7063", fg="black")
