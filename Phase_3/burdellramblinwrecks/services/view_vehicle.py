from model.dao import Dao
from tkinter import *
from ui.searchbox import SearchBox
from ui.table import Table
from services.public_page_service import PublicPageService
from ui.table_sheet import TableSheet
import const

class ViewVehicleService:
    def __init__(self, window, usertype):
        self.dao = Dao().get_instance()
        self.root = window
        self.v = None
        self.show_tab = True
        self.table = None
        self.view_vehicle_page = None
        self.pp_service = PublicPageService()
        self.records = None
        self.public_screen = None
        self.usertype = usertype
        self.message = None

    def show_clerk_view_vehicle_page(self):
        self.public_screen = Toplevel(self.root)
        self.public_screen.title("View Vehicles")
        self.public_screen.geometry("1300x1000")
        Label(self.public_screen, text="Total Number of Vehicles available for purchase", bg="#ADD8E6").pack()
        Label(self.public_screen, text=self.pp_service.vehicle_available_for_purchase()).pack()
        Label(self.public_screen, text="Total Number of Vehicles parts order pending", bg="#ADD8E6").pack()
        Label(self.public_screen, text=self.total_vehicles_part_pending()).pack()
        self.v = IntVar()
        filters = [
            ("Vehicle Type", 1),
            ("Manufacturer", 2),
            ("Model year", 3),
            ("Color", 4),
            ("Keyword", 5),
            ("Vin", 6)
        ]
        Label(self.public_screen, text="""Choose the filter to filter Vehicles""", justify=LEFT, padx=20).pack()
        for val, fil in enumerate(filters):
            Radiobutton(self.public_screen, text=fil[0], padx=20, justify=LEFT, variable=self.v, command=self.show_choice,
                        value=val).pack()
        SearchBox(self.public_screen, command=self.list_public_vehicles, command_arguments=(),
                  placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)
        self.view_vehicle_page = self.public_screen

    def get_parts_details_for_vehicle(self, vin):
        res = self.dao.get_parts_details_for_vehicle(vin)
        if len(res) == 0:
            return "No parts order placed for this Vehicle"
        orders = [entry[0] for entry in res]
        final_res = ""
        for order in list(set(orders)):
            order_str = order + ": \n"
            for entry in res:
                if order == entry[0]:
                    part_str = "Part ID: " + entry[1] + " status: " + entry[2] + " Cost" + str(
                        entry[3]) + "Part Desc: " + entry[4] + " Vendor: " + entry[5] + "\n"
                    # print(part_str)
                    order_str += part_str
            order_str += "\n"
            final_res += order_str
        return final_res

    def get_vehicle_sell_info(self, sell_info):
        part_str = "Sales Price: " + str(sell_info[0][0]) + " Sales Date: " + str(sell_info[0][1]) + \
                    " Sales Person Name" + str(sell_info[0][2]) + " Buyer Name: " + sell_info[0][3] +"\n"

        return part_str
    def show_manager_view_vehicle_page(self):
        self.public_screen = Toplevel(self.root)
        self.public_screen.title("View Vehicles")
        self.public_screen.geometry("1300x1000")
        Label(self.public_screen, text="Total Number of Vehicles available for purchase", bg="#ADD8E6").pack()
        Label(self.public_screen, text=self.pp_service.vehicle_available_for_purchase()).pack()
        Label(self.public_screen, text="Total Number of Vehicles parts order pending", bg="#ADD8E6").pack()
        Label(self.public_screen, text=self.total_vehicles_part_pending()).pack()
        self.v = IntVar()
        filters = [
            ("Vehicle Type", 1),
            ("Manufacturer", 2),
            ("Model year", 3),
            ("Color", 4),
            ("Keyword", 5),
            ("Vin", 6),
            ("Sold Vehicles", 7),
            ("Unsold Vehicles", 8),
            ("All Vehicles", 9)
        ]
        Label(self.public_screen, text="""Choose the filter to filter Vehicles""", justify=LEFT, padx=20).pack()
        for val, fil in enumerate(filters):
            Radiobutton(self.public_screen, text=fil[0], padx=20, justify=LEFT, variable=self.v, command=self.show_choice,
                        value=val).pack()
        SearchBox(self.public_screen, command=self.list_public_vehicles, command_arguments=(),
                  placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)
        self.view_vehicle_page = self.public_screen

    def show_vehicle_detail_page(self, event):
        rows = self.table.sdem.get_selected_rows(get_cells=True)
        record = self.table.records[rows[0]]
        root = Tk()
        root.geometry("1300x1000")
        root.configure(background="#e2e8f0")
        root.title("Vehicle Details")
        vin = Label(root, text="VIN:", bg="#e2e8f0")
        vin_dat = Label(root, text=record[0], bg="#e2e8f0")
        v_type = Label(root, text="Vehicle Type:", bg="#e2e8f0")
        v_type_dat = Label(root, text=record[1], bg="#e2e8f0")
        v_model_year = Label(root, text="Vehicle Model Year:", bg="#e2e8f0")
        v_model_year_dat = Label(root, text=record[2], bg="#e2e8f0")
        v_model = Label(root, text="Vehicle Model:", bg="#e2e8f0")
        v_model_dat = Label(root, text=record[3], bg="#e2e8f0")
        v_odometer = Label(root, text="Vehicle Odometer:", bg="#e2e8f0")
        v_odometer_dat = Label(root, text=record[4], bg="#e2e8f0")
        v_selling_price = Label(root, text="Selling Price:", bg="#e2e8f0")
        v_selling_price_dat = Label(root, text=record[5], bg="#e2e8f0")
        v_mfg = Label(root, text="Manufacturer:", bg="#e2e8f0")
        v_mfg_dat = Label(root, text=record[6], bg="#e2e8f0")
        v_color = Label(root, text="Color(s):", bg="#e2e8f0")
        v_color_dat = Label(root, text=record[7], bg="#e2e8f0")
        v_desc = Label(root, text="Description", bg="#e2e8f0")
        v_desc_dat = Label(root, text=self.dao.get_vehicle_description(record[0])[0], bg="#e2e8f0")
        v_cost = Label(root, text="Cost", bg="#e2e8f0")
        v_cost_dat = Label(root, text=self.dao.get_vehicle_cost(record[0])[0][0], bg="#e2e8f0")
        v_parts_cost = Label(root, text="Parts Cost", bg="#e2e8f0")
        v_parts_cost_dat = Label(root, text=self.dao.get_parts_cost(record[0]), bg="#e2e8f0")

        parts_details = Label(root, text="Vehicle Parts Details\n", bg="#e2e8f0",font = "Helvetica 10 bold")
        parts_details_dat = Label(root, text=self.get_parts_details_for_vehicle(record[0]), bg="#e2e8f0", font = "Helvetica 10 bold")
        vin.grid(row=1, column=0)
        vin_dat.grid(row=1, column=1)
        v_model_year.grid(row=3, column=0)
        v_model_year_dat.grid(row=3, column=1)
        v_type.grid(row=5, column=0)
        v_type_dat.grid(row=5, column=1)
        v_model.grid(row=7, column=0)
        v_model_dat.grid(row=7, column=1)
        v_odometer.grid(row=9, column=0)
        v_odometer_dat.grid(row=9, column=1)
        v_selling_price.grid(row=11, column=0)
        v_selling_price_dat.grid(row=11, column=1)
        v_mfg.grid(row=13, column=0)
        v_mfg_dat.grid(row=13, column=1)
        v_color.grid(row=15, column=0)
        v_color_dat.grid(row=15, column=1)
        v_desc.grid(row=17, column=0)
        v_desc_dat.grid(row=17, column=1)
        v_cost.grid(row=19, column=0)
        v_cost_dat.grid(row=19, column=1)
        v_parts_cost.grid(row=21, column=0)
        v_parts_cost_dat.grid(row=21, column=1)
        parts_details.grid(row=25, column=1)
        parts_details_dat.grid(row=28, column=1)
        root.mainloop()

    def show_vehicle_detail_page_manager(self, event):
        rows = self.table.sdem.get_selected_rows(get_cells=True)
        record = self.table.records[rows[0]]
        root = Tk()
        root.geometry("800x600")
        root.configure(background="#e2e8f0")
        root.title("##Vehicle Details##")
        vin = Label(root, text="VIN:", bg="#e2e8f0")
        vin_dat = Label(root, text=record[0], bg="#e2e8f0")
        v_type = Label(root, text="Vehicle Type:", bg="#e2e8f0")
        v_type_dat = Label(root, text=record[1], bg="#e2e8f0")
        v_model_year = Label(root, text="Vehicle Model Year:", bg="#e2e8f0")
        v_model_year_dat = Label(root, text=record[2], bg="#e2e8f0")
        v_model = Label(root, text="Vehicle Model:", bg="#e2e8f0")
        v_model_dat = Label(root, text=record[3], bg="#e2e8f0")
        v_odometer = Label(root, text="Vehicle Odometer:", bg="#e2e8f0")
        v_odometer_dat = Label(root, text=record[4], bg="#e2e8f0")
        v_selling_price = Label(root, text="Selling Price:", bg="#e2e8f0")
        v_selling_price_dat = Label(root, text=record[5], bg="#e2e8f0")
        v_mfg = Label(root, text="Manufacturer:", bg="#e2e8f0")
        v_mfg_dat = Label(root, text=record[6], bg="#e2e8f0")
        v_color = Label(root, text="Color(s):", bg="#e2e8f0")
        v_color_dat = Label(root, text=record[7], bg="#e2e8f0")
        v_desc = Label(root, text="Description", bg="#e2e8f0")
        v_desc_dat = Label(root, text=self.dao.get_vehicle_description(record[0])[0], bg="#e2e8f0")
        v_seller_Name = Label(root, text="Seller Name:", bg="#e2e8f0")
        v_Seller_Emailid = Label(root, text="Seller Email:", bg="#e2e8f0")
        Seller_info =  self.dao.get_seller_info(record[0])
        v_seller_name = Label(root, text=Seller_info[0][0], bg="#e2e8f0")
        v_seller_emailid = Label(root, text=Seller_info[0][1], bg="#e2e8f0")
        v_seller_Phone = Label(root, text="Seller Phone:", bg="#e2e8f0")
        v_seller_phone = Label(root, text=Seller_info[0][2], bg="#e2e8f0")
        v_seller_Street= Label(root, text="Seller Street:", bg="#e2e8f0")
        v_seller_street = Label(root, text=Seller_info[0][3], bg="#e2e8f0")
        v_seller_Postalcode = Label(root, text="Seller Postal Code:", bg="#e2e8f0")
        v_seller_postalcode = Label(root, text=Seller_info[0][4], bg="#e2e8f0")
        v_seller_City = Label(root, text="Seller City:", bg="#e2e8f0")
        v_seller_city = Label(root, text=Seller_info[0][5], bg="#e2e8f0")
        v_seller_State = Label(root, text="Seller State:", bg="#e2e8f0")
        v_seller_state = Label(root, text=Seller_info[0][6], bg="#e2e8f0")
        v_purchase_Price = Label(root, text="Purchase Price:", bg="#e2e8f0")
        v_purchase_price = Label(root, text=Seller_info[0][7], bg="#e2e8f0")
        v_purchase_Date = Label(root, text="Purchase Date:", bg="#e2e8f0")
        v_purchase_date = Label(root, text=Seller_info[0][8], bg="#e2e8f0")
        v_Buyer = Label(root, text="Buyer name:", bg="#e2e8f0")
        v_buyer = Label(root, text=Seller_info[0][9], bg="#e2e8f0")
        if(Seller_info[0][10] != 0):
            v_business_Title = Label(root, text="Business Title:", bg="#e2e8f0")
            v_business_title = Label(root, text=Seller_info[0][10], bg="#e2e8f0")

        Loan_details = self.dao.get_loan_details(record[0])
        if (len(Loan_details) > 0):
            v_loan_Term = Label(root, text="Loan Term:", bg="#e2e8f0")
            v_loan_term = Label(root, text=Loan_details[0][3], bg="#e2e8f0")
            v_interest_Rate = Label(root, text="Interest Rate:", bg="#e2e8f0")
            v_interest_rate = Label(root, text=Loan_details[0][4], bg="#e2e8f0")
            v_down_Payment = Label(root, text="Down Payemnt:", bg="#e2e8f0")
            v_down_payment = Label(root, text=Loan_details[0][5], bg="#e2e8f0")
            v_month_Payment = Label(root, text="Month Payment:", bg="#e2e8f0")
            v_month_payment = Label(root, text=Loan_details[0][6], bg="#e2e8f0")
            v_start_Month = Label(root, text="Start Month:", bg="#e2e8f0")
            v_start_month = Label(root, text=Loan_details[0][7], bg="#e2e8f0")

        v_parts_cost = Label(root, text="Parts Cost", bg="#e2e8f0")
        v_parts_cost_dat = Label(root, text=self.dao.get_parts_cost(record[0]), bg="#e2e8f0")
        parts_details = Label(root, text="Vehicle Parts Details\n", bg="#e2e8f0", font="Helvetica 10 bold")
        parts_details_dat = Label(root, text=self.get_parts_details_for_vehicle(record[0]), bg="#e2e8f0",
                                  font="Helvetica 10 bold")

        sell_info = self.dao.get_sell_info(record[0])
        if (len(sell_info) > 0):
            v_sell_Info = Label(root, text="Vehicle Sales Details\n", bg="#e2e8f0", font="Helvetica 10 bold")
            v_sell_info = Label(root, text=self.get_vehicle_sell_info(sell_info), bg="#e2e8f0",
                                  font="Helvetica 10 bold")

        vin.grid(row=1, column=0)
        vin_dat.grid(row=1, column=1)
        v_model_year.grid(row=3, column=0)
        v_model_year_dat.grid(row=3, column=1)
        v_type.grid(row=5, column=0)
        v_type_dat.grid(row=5, column=1)
        v_model.grid(row=7, column=0)
        v_model_dat.grid(row=7, column=1)
        v_odometer.grid(row=9, column=0)
        v_odometer_dat.grid(row=9, column=1)
        v_selling_price.grid(row=11, column=0)
        v_selling_price_dat.grid(row=11, column=1)
        v_mfg.grid(row=13, column=0)
        v_mfg_dat.grid(row=13, column=1)
        v_color.grid(row=15, column=0)
        v_color_dat.grid(row=15, column=1)
        v_desc.grid(row=17, column=0)
        v_desc_dat.grid(row=17, column=1)
        v_seller_Name.grid(row=18, column=0)
        v_seller_name.grid(row=18, column=1)
        v_Seller_Emailid.grid(row=19, column=0)
        v_seller_emailid.grid(row=19, column=1)
        v_seller_Phone.grid(row=20, column=0)
        v_seller_phone.grid(row=20, column=1)
        v_seller_Street.grid(row=21, column=0)
        v_seller_street.grid(row=21, column=1)
        v_seller_Postalcode.grid(row=22, column=0)
        v_seller_postalcode.grid(row=22, column=1)
        v_seller_City.grid(row=23, column=0)
        v_seller_city.grid(row=23, column=1)
        v_seller_State.grid(row=24, column=0)
        v_seller_state.grid(row=24, column=1)
        v_purchase_Price.grid(row=25, column=0)
        v_purchase_price.grid(row=25, column=1)
        v_purchase_Date.grid(row=26, column=0)
        v_purchase_date.grid(row=26, column=1)
        v_Buyer.grid(row=27, column=0)
        v_buyer.grid(row=27, column=1)
        if (Seller_info[0][10] != 0):
            v_business_Title.grid(row=28, column=0)
            v_business_title.grid(row=28, column=1)
        if (len(Loan_details) > 0):
            v_loan_Term.grid(row=29, column=0)
            v_loan_term.grid(row=29, column=1)
            v_interest_Rate.grid(row=30, column=0)
            v_interest_rate.grid(row=30, column=1)
            v_down_Payment.grid(row=31, column=0)
            v_down_payment.grid(row=31, column=1)
            v_month_Payment.grid(row=32, column=0)
            v_month_payment.grid(row=32, column=1)
            v_start_Month.grid(row=33, column=0)
            v_start_month.grid(row=33, column=1)


        v_parts_cost.grid(row=34, column=0)
        v_parts_cost_dat.grid(row=34, column=1)
        parts_details.grid(row=35, column=0)
        parts_details_dat.grid(row=35, column=1)


        if (len(sell_info) > 0):
            v_sell_Info.grid(row=36, column=0)
            v_sell_info.grid(row=36, column=1)
        root.mainloop()

    def list_public_vehicles(self, filter_text, arguments):
        options = {0: "get_vehicles_model_type",
                   1: "get_vehicles_manufacturer",
                   2: "get_vehicles_model_year",
                   3: "get_vehicle_color",
                   4: "get_vehicle_any_keyword",
                   5: "get_vehicle_vin",
                   6: "get_vehicle_sold",
                   7: "get_vehicle_unsold",
                   8: "get_vehicle_all"}
        self.records = getattr(self, options.get(self.v.get()))(filter_text)
        if len(self.records) > 0:
            if self.table is not None:
                self.table.sdem.destroy()
            self.table = TableSheet(self.records,
                                    ["vin", "vehicle type", "model year", "model", "Odometer", "sales price",
                                     "manufacturer", "color"], self.public_screen)
            if self.usertype == const.CLERK:
                self.table.sdem.bind("<Double-Button-1>", self.show_vehicle_detail_page)
            if self.usertype == const.MANAGER or self.usertype == const.BURDELL:
                self.table.sdem.bind("<Double-Button-1>", self.show_vehicle_detail_page_manager)
            if self.message is not None:
                self.message.destroy()
                self.message = None
        else:
            if self.message is None:
                self.message = Label(self.public_screen, text="Sorry, it looks like we don’t have that in stock!",
                                     bg="white")
                self.message.pack()

    def show_choice(self):
        pass

    def get_vehicles_model_type(self, vehicle_type):
        records = self.dao.list_vehicles_vehicle_type(vehicle_type)
        records = self.filter_clerk_view_vehicle(records)
        return records

    def get_vehicles_manufacturer(self, mfg_name):
        records = self.dao.list_vehicles_mfg_name(mfg_name)
        records = self.filter_clerk_view_vehicle(records)
        return records

    def get_vehicles_model_year(self, model_year):
        records = self.dao.list_vehicle_model_year(model_year)
        records = self.filter_clerk_view_vehicle(records)
        return records

    def get_vehicle_color(self, color):
        records = self.dao.list_vehicle_color(color)
        records = self.filter_clerk_view_vehicle(records)
        return records

    def get_vehicle_any_keyword(self, keyword):
        records = self.dao.list_vehicle_any_keyword(keyword)
        records = self.filter_clerk_view_vehicle(records)
        return records

    def get_vehicle_vin(self, vin):
        records = self.dao.list_vehicle_vin(vin)
        records = self.filter_clerk_view_vehicle(records)
        return records
    
    def get_vehicle_sold(self, text):
        return self.dao.list_vehicle_sold()

    def get_vehicle_unsold(self, text):
        return self.dao.list_vehicle_unsold()

    def get_vehicle_all(self, text):
        return self.dao.list_vehicle_all()

    def total_vehicles_part_pending(self):
        records = self.dao.list_public_vehicles()
        new_records = []
        for record in records:
            if self.dao.if_any_orders_pending(record[0]):
               new_records.append(record)
        return len(new_records)

    def filter_clerk_view_vehicle(self, records):
        vin_sell_list = self.dao.get_vins_in_sell()
        vin_sell_list = list(vin_sell_list)
        filtered_records = []
        for record in records:
            if record[0] not in vin_sell_list:
                filtered_records.append(record)
        temp = []
        for record in filtered_records:
            temp.append(list(record))
        for record in temp:
            temp[temp.index(record)][5] = self.dao.get_selling_price_of_vehicle(record[0])
        filtered_records = []
        for record in temp:
            filtered_records.append(tuple(record))
        return filtered_records

    def get_parts_details_for_vehicle(self, vin):
        res = self.dao.get_parts_details_for_vehicle(vin)
        if len(res) == 0:
            return "No parts order placed for this Vehicle"
        orders = [entry[0] for entry in res]
        final_res = ""
        for order in list(set(orders)):
            order_str = order + ": \n"
            for entry in res:
                if order == entry[0]:
                    part_str = "Part ID: " + entry[1] + " status: " + entry[2] + " Cost" + str(
                        entry[3]) + "Part Desc: " + entry[4] + " Vendor: " + entry[5] + "\n"
                    order_str += part_str
            order_str += "\n"
            final_res += order_str
        return final_res