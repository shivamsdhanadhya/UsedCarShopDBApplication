import math
import const
from tkinter import *
from model.dao import Dao
from ui.searchbox import SearchBox
from ui.table_sheet import TableSheet
from datetime import datetime
class AddVehicleService:
    def __init__(self, window):
        self.dao = Dao().get_instance()
        self.seller_uid = None
        self.vehicle_type = None
        self.cost = None
        self.model_name = None
        self.model_year = None
        self.manu_id = None
        self.milage = None
        self.desc = None
        self.color = None
        self.message = None
        self.root = window
        self.buy_date = None
        self.condition = None

    def is_valid_buy_date(self, buy_date):
        var = buy_date.split("-")
        today_var = datetime.today().strftime('%Y-%m-%d').split("-")
        return datetime(int(var[0]), int(var[1]), int(var[2])) > datetime(int(today_var[0]), int(today_var[1]),
                                                                          int(today_var[2]))

    def insert(self, root):
        #TODO: Error handling is to be provided here
        #TODO: Some provision to close the window automatically after Sumbit button is pressed
        #TODO: handle error cases where some of the fileds are
        if int(self.model_year.get()) > datetime.today().year:
            self.popup_window("DATE ERROR", "Model Year should be less than current year")
            return
        if self.is_valid_buy_date(str(self.buy_date.get())):
            self.popup_window("DATE ERROR", "Purchase Date must be today or any day before today .....")
            return
        vehicle_val = (self.vin.get(), self.vehicle_type.get(), float(self.cost.get()),
                       self.model_name.get(), int(self.model_year.get()), int(self.manu_id.get()),
                       int(self.milage.get()), self.desc.get())
        self.dao.insert_vehicle(vehicle_val)

        buy_val = (self.vin.get(), self.seller_uid.get(), const.CURRENT_USER,
                   float(self.cost.get()), self.buy_date.get(), self.condition.get())
        self.dao.insert_buy(buy_val)

        color_list = str(self.color.get()).split(",")
        for color in color_list:
            vehicle_color_val = (str(self.vin.get()), color)
            #self.dao.insert_vehicle_color(self.vin.get(), self.color.get())
            self.dao.insert_vehicle_color(vehicle_color_val)
        root.destroy()

    def insert_individual_customer(self, screen):
        cust_id = self.dao.count_all_customers()
        customer = (str(cust_id+1),self.email.get(),self.phone_number.get(),self.street.get(),
                         self.postal_code.get(),self.city.get(),self.state.get())
        individual = (str(cust_id+1), self.dln.get(),self.first_name.get(),self.last_name.get())
        self.dao.insert_individual_customer(customer,individual)
        screen.destroy()

    def insert_business_customer(self, screen, record):
        cust_id = self.dao.count_all_customers()
        customer = (str(cust_id + 1), record[0].get(), record[1].get(), record[2].get(),
                    record[3].get(), record[4].get(), record[5].get())
        business = (str(cust_id + 1), record[6].get(), record[7].get(), record[8].get(),record[9].get(), record[10].get())
        self.dao.insert_business_customer(customer,business)
        screen.destroy()

    def list_customers(self,filter_text,arguments):
        if self.v.get()==0:
            columns = ["Customer id", "Tax Id","Business Name","Contact First Name","Contact Last Name","Contact Title"]
            records = self.dao.list_customers_taxId(filter_text)
        else:
            columns = ["Customer Id","Driver License Number","First Name","Last Name"]
            records = self.dao.list_customers_license(filter_text)
        if len(records)>0:
            TableSheet(records,columns,arguments[0])
            if self.message is not None:
                self.message.destroy()
                self.message = None
        else:
            if self.message is None:
                self.message = Label(arguments[0],text="No customer found")
                self.message.pack()

    def add_business_customer(self):
        root = Tk()
        root.configure(background='white')
        root.title("Add Customer Form")
        root.geometry("500x350")
        heading = Label(root, text="Add Business Customer", bg="white")
        tax_id_no = Label(root, text="Tax Id number", bg="white")
        email = Label(root, text="email", bg="white")
        business_name = Label(root, text="business name", bg="white")
        contact_person_first_name = Label(root, text="CP first name ", bg="white")
        contact_person_last_name = Label(root, text="CP last name ", bg="white")
        phone_number = Label(root, text="phone number", bg="white")
        street = Label(root, text="street", bg="white")
        city = Label(root, text="city", bg="white")
        state = Label(root, text="state", bg="white")
        postal_code = Label(root, text="postal code", bg="white")
        cp_title = Label(root, text="contact person Title", bg="white")

        heading.grid(row=0, column=1)
        tax_id_no.grid(row=1, column=0)
        email.grid(row=2, column=0)
        business_name.grid(row=3, column=0)
        contact_person_first_name.grid(row=4, column=0)
        contact_person_last_name.grid(row=5,column=0)
        phone_number.grid(row=6, column=0)
        street.grid(row=7, column=0)
        city.grid(row=8, column=0)
        state.grid(row=9, column=0)
        postal_code.grid(row=10, column=0)
        cp_title.grid(row=11, column=0)
        # text entry box
        tax_id_no = Entry(root)
        email = Entry(root)
        business_name = Entry(root)
        contact_person_first_name = Entry(root)
        contact_person_last_name = Entry(root)
        phone_number = Entry(root)
        street = Entry(root)
        city = Entry(root)
        state = Entry(root)
        postal_code = Entry(root)
        cp_title = Entry(root)

        # grid for inputs
        tax_id_no.grid(row=1, column=1, ipadx="100")
        email.grid(row=2, column=1, ipadx="100")
        business_name.grid(row=3, column=1, ipadx="100")
        contact_person_first_name.grid(row=4, column=1, ipadx="100")
        contact_person_last_name.grid(row=5, column=1, ipadx="100")
        phone_number.grid(row=6, column=1, ipadx="100")
        street.grid(row=7, column=1, ipadx="100")
        city.grid(row=8, column=1, ipadx="100")
        state.grid(row=9, column=1, ipadx="100")
        postal_code.grid(row=10, column=1, ipadx="100")
        cp_title.grid(row=11, column=1, ipadx="100")
        record = (email,phone_number,street,postal_code,city,state,tax_id_no,business_name,contact_person_first_name,contact_person_last_name,cp_title)
        # create a Submit Button and place into the root window
        submit = Button(root, text="Submit", fg="Black", bg="Red", command=lambda m=root,r=record:self.insert_business_customer(m,r))
        submit.grid(row=13, column=1)


    def add_individual_customer(self):
        root = Tk()
        root.configure(background='white')
        root.title("Add Customer Form")
        root.geometry("500x350")
        heading = Label(root, text="Add Individual Customer", bg="white")
        self.dln = Label(root, text="driver license number", bg="white")
        self.email = Label(root, text="email", bg="white")
        self.first_name = Label(root, text="firstname", bg="white")
        self.last_name = Label(root, text="lastname", bg="white")
        self.phone_number = Label(root, text="phone number", bg="white")
        self.street = Label(root, text="street", bg="white")
        self.city = Label(root, text="city", bg="white")
        self.state = Label(root, text="state", bg="white")
        self.postal_code = Label(root, text="postal code", bg="white")

        heading.grid(row=0, column=1)
        self.dln.grid(row=1, column=0)
        self.email.grid(row=2, column=0)
        self.first_name.grid(row=3, column=0)
        self.last_name.grid(row=4, column=0)
        self.phone_number.grid(row=5, column=0)
        self.street.grid(row=6, column=0)
        self.city.grid(row=7, column=0)
        self.state.grid(row=8, column=0)
        self.postal_code.grid(row=9, column=0)

        # text entry box
        self.dln = Entry(root)
        self.email = Entry(root)
        self.first_name = Entry(root)
        self.last_name = Entry(root)
        self.phone_number = Entry(root)
        self.street = Entry(root)
        self.city = Entry(root)
        self.state = Entry(root)
        self.postal_code = Entry(root)

        # grid for inputs
        self.dln.grid(row=1, column=1, ipadx="100")
        self.email.grid(row=2, column=1, ipadx="100")
        self.first_name.grid(row=3, column=1, ipadx="100")
        self.last_name.grid(row=4, column=1, ipadx="100")
        self.phone_number.grid(row=5, column=1, ipadx="100")
        self.street.grid(row=6, column=1, ipadx="100")
        self.city.grid(row=7, column=1, ipadx="100")
        self.state.grid(row=8, column=1, ipadx="100")
        self.postal_code.grid(row=9, column=1, ipadx="100")
        # create a Submit Button and place into the root window
        submit = Button(root, text="Submit", fg="Black", bg="Red", command=lambda m=root:self.insert_individual_customer(m))
        submit.grid(row=11, column=1)

    def lookup_customer_info(self):
        root = Toplevel()
        root.configure(background='white')
        root.title("lookup or add customer")
        root.geometry("500x350")
        add_individual_customer = Button(root, text="Add Individual Customer", fg="Black", bg="Red", command=self.add_individual_customer)
        add_individual_customer.pack()
        add_business_customer = Button(root, text="Add Business Customer", fg="Black", bg="Red",
                                         command=self.add_business_customer)
        add_business_customer.pack()
        Label(root, text="""Choose the customer type to search on""", justify=LEFT, padx=20).pack()
        self.v = IntVar()
        filters = [
            ("Business Customer", 1),
            ("Individual Customer", 2)]
        for val, fil in enumerate(filters):
            Radiobutton(root, text=fil[0], padx=20, justify=LEFT, variable=self.v, command=self.show_choice,
                        value=val).pack()
        SearchBox(root, command = self.list_customers, command_arguments=(root,),
                  placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(pady=6, padx=3)

    def show_choice(self):
        pass

    def show_add_vehicle_form(self):

        root = Tk()
        root.configure(background='#e2e8f0')
        root.title("Add Vehicle")
        root.geometry("500x400")

        heading = Label(root, text="Add Vehicle Form", bg="#e2e8f0")
        self.seller_uid = Label(root, text="Seller UID", bg="#e2e8f0")
        self.vin = Label(root, text="VIN", bg="#e2e8f0")
        self.vehicle_type = Label(root, text="Vehicle Type", bg="#e2e8f0")
        self.cost = Label(root, text="Cost", bg="#e2e8f0")
        self.model_name = Label(root, text="Model Name", bg="#e2e8f0")
        self.model_year = Label(root, text="Model Year", bg="#e2e8f0")
        self.manu_id = Label(root, text="Manufacturer ID", bg="#e2e8f0")
        self.milage = Label(root, text="Odometer", bg="#e2e8f0")
        self.color = Label(root, text="Color(s)", bg="#e2e8f0")
        self.desc = Label(root, text="Description", bg="#e2e8f0")
        self.condition = Label(root, text="Vehicle Condition", bg="#e2e8f0")
        self.buy_date = Label(root, text="Buy Date", bg="#e2e8f0")

        #grid
        heading.grid(row=0, column=1)
        self.seller_uid.grid(row=1, column=0)
        self.vin.grid(row=2, column=0)
        self.vehicle_type.grid(row=3, column=0)
        self.cost.grid(row=4, column=0)
        self.model_name.grid(row=5, column=0)
        self.model_year.grid(row=6, column=0)
        self.manu_id.grid(row=7, column=0)
        self.milage.grid(row=8, column=0)
        self.color.grid(row=9, column=0)
        self.desc.grid(row=10, column=0)
        self.condition.grid(row=11, column=0)
        self.buy_date.grid(row=12, column=0)

        #text entry box
        self.seller_uid = Entry(root)
        self.vin = Entry(root)
        self.vehicle_type = Entry(root)
        self.cost = Entry(root)
        self.model_name = Entry(root)
        self.model_year = Entry(root)
        self.manu_id = Entry(root)
        self.milage = Entry(root)
        self.color = Entry(root)
        self.desc = Entry(root)
        self.condition = Entry(root)
        self.buy_date = Entry(root)

        #grid for inputs
        self.seller_uid.grid(row=1, column=1, ipadx="100")
        self.vin.grid(row=2, column=1, ipadx="100")
        self.vehicle_type.grid(row=3, column=1, ipadx="100")
        self.cost.grid(row=4, column=1, ipadx="100")
        self.model_name.grid(row=5, column=1, ipadx="100")
        self.model_year.grid(row=6, column=1, ipadx="100")
        self.manu_id.grid(row=7, column=1, ipadx="100")
        self.milage.grid(row=8, column=1, ipadx="100")
        self.color.grid(row=9, column=1, ipadx="100")
        self.desc.grid(row=10, column=1, ipadx="100")
        self.condition.grid(row=11, column=1, ipadx="100")
        self.buy_date.grid(row=12, column=1, ipadx="100")

        # create a Submit Button and place into the root window
        submit = Button(root, text="Submit", fg="Black", bg="#ADD8E6", command=lambda w=root: self.insert(root))
        submit.grid(row=14, column=1)
        lookup_customer = Button(root, text="Search Customer", fg="Black", bg="#ADD8E6", command=self.lookup_customer_info)
        lookup_customer.grid(row=15, column=1)
        # start the GUI
        root.mainloop()

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