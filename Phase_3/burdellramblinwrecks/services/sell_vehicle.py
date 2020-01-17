from tkinter import *
from model.dao import Dao
from services.add_vehicle import AddVehicleService
from ui.searchbox import SearchBox
from ui.table_sheet import TableSheet
from services.public_page_service import PublicPageService
from datetime import datetime

class SellVehicleService:

    def __init__(self, window, user):
        self.dao = Dao().get_instance()
        self.root = window
        self.v = None
        self.show_tab = True
        self.table = None
        self.view_vehicle_page = None
        self.message = None
        self.user = user
        self.loan = None
        self.pp_service = PublicPageService()
        self.is_loan = False

    def show_vehicle_for_sale(self):
        public_screen = Toplevel(self.root)
        public_screen.title("View and Sale Vehicle")
        #public_screen.geometry("%sx%s" % (public_screen.winfo_reqwidth(), public_screen.winfo_reqheight()))
        public_screen.geometry("1300x1000")
        Label(public_screen, text="Total Number of Vehicles available for Sale", bg="#ADD8E6").pack()
        Label(public_screen, text=self.pp_service.vehicle_available_for_purchase()).pack()
        self.v = IntVar()
        filters = [
            ("Vehicle Type", 1),
            ("Manufacturer", 2),
            ("Model year", 3),
            ("Color", 4),
            ("Keyword", 5),
            ("Vin", 6)
        ]
        Label(public_screen, text="""Choose the filter to filter Vehicles""", justify=LEFT, padx=20).pack()
        for val, fil in enumerate(filters):
            Radiobutton(public_screen, text=fil[0], padx=20, justify=LEFT, variable=self.v, command=self.show_choice,
                        value=val).pack()
        SearchBox(public_screen, command=self.list_public_vehicles, command_arguments=(public_screen),
                  placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)
        self.view_vehicle_page = public_screen

    def list_public_vehicles(self, filter_text, window):
        options = {0: "get_vehicles_model_type",
                   1: "get_vehicles_manufacturer",
                   2: "get_vehicles_model_year",
                   3: "get_vehicle_color",
                   4: "get_vehicle_any_keyword",
                   5: "get_vehicle_vin"}

        records = getattr(self, options.get(self.v.get()))(filter_text)
        if len(records) > 0:
                if self.table is not None:
                    self.table.sdem.destroy()
                self.table = TableSheet(records,["vin", "vehicle type", "model year", "model", "mileage", "price", "manufacturer","color"],window)
                self.table.sdem.bind("<Double-Button-1>", self.show_vehicle_sale_page)
                if self.message is not None:
                    self.message.destroy()
                    self.message = None
        else:
            if self.message is None:
                self.message = Label(self.view_vehicle_page, text="Sorry, it looks like we don’t have that in stock!", bg="#e2e8f0")
                self.message.pack()

    def show_vehicle_sale_page(self, event):
        add_vehicle = AddVehicleService(None)
        rows = self.table.sdem.get_selected_rows(get_cells=True)
        record = self.table.records[rows[0]]
        root = Tk()
        root.geometry("800x600")
        root.configure(background="#e2e8f0")
        root.title("Sell Vehicle")
        label1 = Label(root, text="Sell Vehicle:")
        label1.grid(row=1, column=0, ipadx="100")
        label2 = Label(root, text=str(record[0]))
        label2.grid(row=1,column=1)
        date = Label(root, text="Enter sale date (YYYY-MM-DD)", bg="#e2e8f0")
        date_entry = Entry(root)
        date.grid(row=2,column=0)
        date_entry.grid(row=2,column=1)
        customer = Label(root, text="Enter customer id", bg="#e2e8f0")
        customer_entry = Entry(root)
        customer.grid(row=3, column=0)
        customer_entry.grid(row=3, column=1)
        add_individual_customer = Button(root, text="lookup customer", fg="Black", bg="#ADD8E6",command=add_vehicle.lookup_customer_info)
        add_individual_customer.grid(row=4, column=0)
        add_loan = Button(root, text="Add Loan", fg="Black", bg="#ADD8E6", command=lambda window=root:self.add_loan(window))
        add_loan.grid(row=4, column=1)
        new_record = (date_entry, customer_entry, record[0])
        submit = Button(root, text="Make sale", fg="Black", bg="#ADD8E6", command=lambda m=new_record,p=root:self.make_vehicle_sale(m,p))
        submit.grid(row=15, column=1)
        add_individual_customer.grid(row=4, column=0)
        root.mainloop()

    def add_loan(self, window):
        self.is_loan = True
        interest_rate = Label(window, text="Interest Rate (%)", bg="#e2e8f0")
        down_payment = Label(window, text="Down Payment ($)", bg="#e2e8f0")
        monthly_payment = Label(window, text="Monthly Payment ($)", bg="#e2e8f0")
        start_month = Label(window, text="Start Month (YYYY-MM)", bg="#e2e8f0")
        term = Label(window, text="Loan Term (in month)", bg="#e2e8f0")

        interest_rate.grid(row=8, column=0)
        down_payment.grid(row=9, column=0)
        monthly_payment.grid(row=10, column=0)
        start_month.grid(row=11, column=0)
        term.grid(row=12, column=0)

        interest_rate_val = Entry(window)
        down_payment_val = Entry(window)
        monthly_payment_val = Entry(window)
        start_month_val = Entry(window)
        term_val = Entry(window)

        interest_rate_val.grid(row=8, column=1, ipadx="100")
        down_payment_val.grid(row=9, column=1, ipadx="100")
        monthly_payment_val.grid(row=10, column=1, ipadx="100")
        start_month_val.grid(row=11, column=1, ipadx="100")
        term_val.grid(row=12, column=1, ipadx="100")
        self.loan = (term_val,interest_rate_val,down_payment_val,monthly_payment_val, start_month_val)

    def is_buy_date_less_than_sell_date(self, buy_date, sale_date):
        var = str(buy_date).split("-")
        sale_var = str(sale_date).split("-")
        return datetime(int(var[0]), int(var[1]), int(var[2])) < datetime(int(sale_var[0]), int(sale_var[1]), int(sale_var[2]))

    def make_vehicle_sale(self, record, window):
        record = list(record)
        record.append(self.user)
        record.append(self.dao.get_selling_price_of_vehicle(record[2]))
        record = tuple(record)
        input_sale_date = record[0].get()
        input_vin = record[2]
        buy_date_for_vin = self.dao.get_buy_date_for_vin(input_vin)
        if not self.is_buy_date_less_than_sell_date(buy_date_for_vin, input_sale_date):
            self.popup_window("ERROR", "Input Sale Date Can't be less than Buy Date...")
            return
        self.dao.insert_into_sell(record)
        if self.is_loan:
            loan_record = [record[2], self.user,int(self.loan[0].get()),float(self.loan[1].get()),
                           float(self.loan[2].get()),float(self.loan[3].get()), self.loan[4].get()]
            self.dao.insert_into_loan(loan_record)
        sell_vehicle_success_screen = Tk()
        sell_vehicle_success_screen.title("Success")
        sell_vehicle_success_screen.geometry("150x100")
        Label(sell_vehicle_success_screen, text="Vehicle Sold Successfully").pack()
        Button(sell_vehicle_success_screen, text="OK", command=lambda m=window,c=sell_vehicle_success_screen:self.destroy(m,c)).pack()

    def destroy(self,window,child):
        child.destroy()
        window.destroy()

    def show_choice(self):
        pass

    def get_vehicles_model_type(self, vehicle_type):
        return self.pp_service.list_vehicles_vehicle_type(vehicle_type)

    def get_vehicles_manufacturer(self, mfg_name):
        return self.pp_service.list_vehicle_mfg_name(mfg_name)

    def get_vehicles_model_year(self, model_year):
        return self.pp_service.list_vehicle_model_year(model_year)

    def get_vehicle_color(self, color):
        return self.pp_service.list_vehicle_color(color)

    def get_vehicle_any_keyword(self, keyword):
        return self.pp_service.list_vehicle_any_keyword(keyword)

    def get_vehicle_vin(self, vin):
        return self.pp_service.list_vehicle_vin(vin)

    def popup_window(self, title, message):
        global popup_win
        popup_win = Tk()
        popup_win.title(title)
        popup_win.geometry("250x100")
        Label(popup_win, text=message).pack()
        Button(popup_win, text="OK", command=self.delete_popup_window).pack()
        popup_win.mainloop()

    def delete_popup_window(self):
        popup_win.destroy()