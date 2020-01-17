from tkinter import *

import const
from model.dao import Dao
from services.add_vehicle import AddVehicleService
from services.part_order import PartOrderService
from services.report import Report
from services.sell_vehicle import SellVehicleService
from services.view_vehicle import ViewVehicleService
from services.lookup_parts import LookupParts


class DashboardService:
    def __init__(self, main_screen):
        self.dao = Dao().get_instance()
        self.main_screen = main_screen
        self.utype = None
        self.username = None

    def show_dashboard(self, uname, passwd):
        dashboard_menu = []
        self.username = uname
        utype = self.dao.get_user_type(uname, passwd)
        self.utype = utype[0][0]
        if self.utype == const.CLERK:
            #TODO: Add Vehicle has to have search or add customer options
            dashboard_menu = ["Add Vehicle", "View Vehicles", "Place/Update Part Order", "Lookup Parts"]
            
        elif self.utype == const.SALESPERSON:
            dashboard_menu = ["View and Sell Vehicle"]

        elif self.utype == const.MANAGER:
            dashboard_menu = ["View Vehicle", "Seller History Report", "Average Time in Inverntory Report",
                              "Price Per Condition Report", "Parts Statistics Report", "Monthly Loan Income Report",
                              "Monthly Sales Report"]

        elif self.utype == const.BURDELL:
            dashboard_menu = ["Add Vehicle", "View Vehicle", "Place/Update Part Order", "View Vehicle and Update Sales Info",
                              "Seller History Report", "Average Time in Inverntory Report",
                              "Price Per Condition Report", "Parts Statistics Report", "Monthly Loan Income Report",
                              "Monthly Sales Report"
                              ]
        dashboard_title = "Dashboard for {0}, you are welcome {1}".format(self.utype, uname)
        self.generic_dashboard(dashboard_title, dashboard_menu)

    def populateMethod(self, method, window):
        if method == "Add Vehicle":
            add_vehicle_obj = AddVehicleService(self.main_screen)
            add_vehicle_obj.show_add_vehicle_form()
        if method == "Place/Update Part Order":
            part_order_obj = PartOrderService()
            part_order_obj.show_part_order_form()
        if method == "View Vehicles" and self.utype == const.CLERK:
            view_vehicle_service = ViewVehicleService(self.main_screen, self.utype)
            view_vehicle_service.show_clerk_view_vehicle_page()
        if method == "View and Sell Vehicle" and self.utype == const.SALESPERSON:
            sell_vehicle = SellVehicleService(self.main_screen,self.username)
            sell_vehicle.show_vehicle_for_sale()

        if method == "View Vehicle and Update Sales Info" and self.utype == const.BURDELL:
            sell_vehicle = SellVehicleService(self.main_screen, self.username)
            sell_vehicle.show_vehicle_for_sale()

        if method == "View Vehicle":
            view_vehicle_service = ViewVehicleService(self.main_screen, self.utype)
            view_vehicle_service.show_manager_view_vehicle_page()

        if method == "Lookup Parts":
            lookup_parts = LookupParts(self.main_screen)
            lookup_parts.show_vehicle_parts()

        if method == "Seller History Report":
            Report(self.main_screen).seller_history_report()

        if method == "Average Time in Inverntory Report":
            Report(self.main_screen).average_time_in_inventory_report()

        if method == "Price Per Condition Report":
            Report(self.main_screen).price_per_condition_report()

        if method == "Monthly Loan Income Report":
            Report(self.main_screen).monthly_loan_income_report()

        if method == "Parts Statistics Report":
            Report(self.main_screen).parts_statistics_report()

        if method == "Monthly Sales Report":
            report = Report(self.main_screen)
            report.monthly_sales_report()


    def generic_dashboard(self, title, dashboard_menu):
        window = Tk()
        window.geometry("500x350")
        window.configure(background="#e2e8f0")
        window.title(title)
        for method in dashboard_menu:
            button = Button(window, text=method,
                            command=lambda m=method,w=window: self.populateMethod(m,window), bg="#ADD8E6", width=200)

            button.pack()
        window.mainloop()