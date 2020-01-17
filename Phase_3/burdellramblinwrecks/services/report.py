from model.dao import Dao
from ui.sheet import CustomizedSheet
from ui.table import Table
from tkinter import *
class Report:
    __instance = None

    def __init__(self, window):
        self.dao = Dao().get_instance()
        self.root = window

    def report_screen(self,title,records, header, rows=None):
        app = CustomizedSheet(records, header, title, rows=rows)
        app.mainloop()

    def seller_history_report(self):
        records = self.dao.seller_history_report()
        header = ['Name', 'Total Number of Vehicles Sold','Average Purchase Price','Average Number of Parts', 'Average Cost of Parts']
        row=0
        rows=[]
        for record in records:
            if record[3] >= 5 or record[4] >= 500:
                rows.append(row)
            row += 1
        self.report_screen('Seller History Report', records, header, rows=rows)


    def average_time_in_inventory_report(self):
        records = self.dao.average_time_in_inventory_report()
        header = ['Vehicle Type', 'Average Days in Inventory']
        self.report_screen('Average Time in Inventory Report', records, header)

    def price_per_condition_report(self):
        records = self.dao.price_per_condition_report()
        header = ['vehicle_type', 'Fair', 'Good', 'Very Good', 'Excellent']
        self.report_screen('Price Per Condition Report', records, header)

    def parts_statistics_report(self):
        records = self.dao.parts_statistics_report()
        header = ['Vendor Name', 'Number of Parts', 'Total Cost of Parts']
        self.report_screen('Parts Statistics Report', records, header)

    def monthly_loan_income_report(self):
        records = self.dao.monthly_loan_income_report()
        header = ['Start Month', 'Monthly Payment', 'Burdell share']
        self.report_screen('Monthly Loan Income Report', records, header)

    def drilldown(self, text, public_screen):
        date_to_search = text.get()
        records = self.dao.monthly_Sales_report_drilldown(date_to_search)
        header = ['Name', 'Number of Vehicles Sold', 'Total Sales']
        self.report_screen(' Monthly Sales Specific Report', records, header)

    def monthly_sales_report(self):
        records = self.dao.monthly_sales_report_summary()
        header = ['Date', 'Number of Vehicles Sold', 'Total Sales Income', 'Total Net Income']
        public_screen = Toplevel(self.root)
        public_screen.geometry("1300x1000")
        table = Table(public_screen, ['Date', 'Number of Vehicles Sold', 'Total Sales Income', 'Total Net Income'], column_minwidths=[None, None, None, None])
        table.pack(padx=50, pady=50)
        table.set_data(records)
        w = Label(public_screen, text="Enter Date (In YYYY-MM Format):")
        w.pack()
        text = StringVar()
        e = Entry(public_screen, textvariable=text)
        e.pack()
        showButton = Button(public_screen, text='Search', command=lambda: self.drilldown(text, public_screen))
        showButton.pack()
