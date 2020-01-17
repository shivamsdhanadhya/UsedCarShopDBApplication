from model.dao import Dao
from services.public_page_service import PublicPageService
from ui.table_sheet import TableSheet
from ui.searchbox import SearchBox
from tkinter import *
class PublicPage:

    def __init__(self, window):
        self.dao =  Dao().get_instance()
        self.records = None
        self.table = None
        self.message = None
        self.public_page_service = PublicPageService()
        self.main_screen = window
        self.public_screen = None
        self.v = None

    def get_vehicles_model_type(self, vehicle_type, pp_service):
        return pp_service.list_vehicles_vehicle_type(vehicle_type)

    def get_vehicles_manufacturer(self,mfg_name, pp_service):
        return pp_service.list_vehicle_mfg_name(mfg_name)

    def get_vehicles_model_year(self,model_year, pp_service):
        return pp_service.list_vehicle_model_year(model_year)

    def get_vehicle_color(self, color, pp_service):
        return pp_service.list_vehicle_color(color)

    def get_vehicle_any_keyword(self, keyword, pp_service):
        return pp_service.list_vehicle_any_keyword(keyword)

    def list_public_vehicles(self, filter_text, arguments):
        options = {0: "get_vehicles_model_type",
                   1: "get_vehicles_manufacturer",
                   2: "get_vehicles_model_year",
                   3: "get_vehicle_color",
                   4: "get_vehicle_any_keyword"
                   }
        public_page_service = PublicPageService()
        self.records = getattr(self, options.get(self.v.get()))(filter_text, public_page_service)
        if len(self.records) > 0:
            if self.table is not None:
                self.table.sdem.destroy()
            self.table = TableSheet(self.records, ["vin", "vehicle type", "model year", "model", "Odometer", "selling price",
                                             "manufacturer", "color"], self.public_screen)
            self.table.sdem.bind("<Double-Button-1>", self.show_vehicle_detail_page)
            if self.message is not None:
                self.message.destroy()
                self.message = None
        else:
            if self.message is None:
                self.message = Label(self.public_screen, text="Sorry, it looks like we don’t have that in stock!", bg="white")
                self.message.pack()

    def show_vehicle_detail_page(self, event):
        rows = self.table.sdem.get_selected_rows(get_cells=True)
        record = self.table.records[rows[0]]
        root = Tk()
        root.geometry("800x600")
        root.configure(background="#e2e8f0")
        root.title("##Vehicle Details##")
        vin = Label(root, text="VIN:",bg="#e2e8f0")
        vin_dat = Label(root, text=record[0],bg="#e2e8f0")
        v_type = Label(root, text="Vehicle Type:",bg="#e2e8f0")
        v_type_dat = Label(root, text=record[1],bg="#e2e8f0")
        v_model_year = Label(root, text="Vehicle Model Year:", bg="#e2e8f0")
        v_model_year_dat = Label(root, text=record[2], bg="#e2e8f0")
        v_model = Label(root, text="Vehicle Model:", bg="#e2e8f0")
        v_model_dat = Label(root, text=record[3], bg="#e2e8f0")
        v_odometer = Label(root, text="Vehicle Odometer:", bg="#e2e8f0")
        v_odometer_dat = Label(root, text=record[4], bg="#e2e8f0")
        v_selling_price = Label(root, text="Selling Price:", bg="#e2e8f0")
        v_selling_price_dat = Label(root, text=record[5], bg="#e2e8f0")
        v_mfg = Label(root, text="Manufacturer:", bg="#e2e8f0")
        v_mfg_dat = Label(root, text=record[6] ,bg="#e2e8f0")
        v_color = Label(root, text="Color(s):", bg="#e2e8f0")
        v_color_dat = Label(root, text=record[7], bg="#e2e8f0")
        v_desc = Label(root, text="Description", bg="#e2e8f0")
        v_desc_dat = Label(root, text=self.dao.get_vehicle_description(record[0])[0], bg="#e2e8f0")

        vin.grid(row=1,column=0)
        vin_dat.grid(row=1, column = 1)
        v_model_year.grid(row=3,column=0)
        v_model_year_dat.grid(row=3,column=1)
        v_type.grid(row=5,column=0)
        v_type_dat.grid(row=5,column=1)
        v_model.grid(row=7,column=0)
        v_model_dat.grid(row=7,column=1)
        v_odometer.grid(row=9,column=0)
        v_odometer_dat.grid(row=9,column=1)
        v_selling_price.grid(row=11,column=0)
        v_selling_price_dat.grid(row=11,column=1)
        v_mfg.grid(row=13,column=0)
        v_mfg_dat.grid(row=13,column=1)
        v_color.grid(row=15,column=0)
        v_color_dat.grid(row=15,column=1)
        v_desc.grid(row=17,column=0)
        v_desc_dat.grid(row=17,column=1)
        root.mainloop()

    def show_public_page(self):

        self.public_screen = Toplevel(self.main_screen)
        self.public_screen.title("Public Page")
        self.public_screen.geometry("600x500")
        Label(self.public_screen, text="Total Number of cars available for purchase", bg="white").pack()
        public_page_service = PublicPageService()
        Label(self.public_screen, text=public_page_service.vehicle_available_for_purchase()).pack()
        self.v = IntVar()
        filters = [
            ("Vehicle Type", 1),
            ("Manufacturer", 2),
            ("Model year", 3),
            ("Color", 4),
            ("Keyword", 5)
        ]
        Label(self.public_screen, text="""Choose the filter to filter Vehicles""", justify=LEFT, padx=20).pack()
        for val, fil in enumerate(filters):
            Radiobutton(self.public_screen, text=fil[0], padx=20, justify=LEFT, variable=self.v, command=self.show_choice,
                        value=val).pack()
        SearchBox(self.public_screen, command=self.list_public_vehicles, command_arguments=(), placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)
        Label(self.public_screen, text="*Double click on row number to view respective vehicle details", justify=LEFT, padx=20).pack()

    def show_choice(self):
        pass