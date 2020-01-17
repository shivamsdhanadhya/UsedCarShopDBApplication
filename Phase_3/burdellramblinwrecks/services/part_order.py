from tkinter import *

from model.dao import Dao


def get_vehicle_part_freq_dict(prev_orders):
    vehicle_list = [i[0] for i in prev_orders]
    vehicle_set= set(vehicle_list)
    vehicle_part_ordered_freq = {}
    for vehicle in vehicle_set:
        vehicle_part_ordered_freq.update({vehicle:vehicle_list.count(vehicle)})
    return vehicle_part_ordered_freq

def get_desc_for_vehicle_part(prev_orders, vehicle, part_no):
    vehicle_specific_part_desc = [entry[-1] for entry in prev_orders if entry[0]==vehicle]
    return vehicle_specific_part_desc[part_no-1]

def get_vehicle_part_to_desc_map(prev_orders):
    vehicle_part_dict = get_vehicle_part_freq_dict(prev_orders)
    parent_dict = {}
    for vehicle in vehicle_part_dict.keys():
        freq = vehicle_part_dict[vehicle]
        for part_no in range(1, freq + 1):
            desc = get_desc_for_vehicle_part(prev_orders, vehicle, part_no)
            parent_dict.update({vehicle + "-" + "{:02d}".format(part_no): desc})
    return parent_dict

class PartOrderService:
    def __init__(self):
        self.dao = Dao().get_instance()
        # Part Order related vars
        self.order_uid = None
        self.parts = None
        self.vendor_name = None
        self.street = None
        self.city = None
        self.state = None
        self.postal_code = None
        self.phone_number = None
        # Assistant vars
        self.prev_orders = None
        self.vendor_info = None
        self.next_part_flag = False
        self.submit_part = None
        self.update_part_status_button = None
        self.variable_status = None
        self.order_number = None
        self.part_number = None
        self.update_order_button = None
        self.go_to_this_part = None
        self.part_number_drop_down = None

        # Single Part Add related
        self.insert_single_part_parent = set()
        self.single_part_vin = None
        self.single_part_cost = None
        self.single_part_desc = None
        self.single_part_part_no = None
        self.single_part_order_number = None

    def show_part_order_form(self):
        # create a GUI window
        root = Tk()

        # set the background colour of GUI window
        root.configure(background='#e2e8f0')

        # set the title of GUI window
        root.title("Part Order Form")

        # set the configuration of GUI window
        root.geometry("1200x"
                      "800")

        # create a Form label
        heading1 = Label(root, text="Update Status for Parts Ordered", bg="#33A2FF", width=30)
        heading2 = Label(root, text="Place New Order", bg="#33A2FF", width=30)
        heading3 = Label(root, text="Latest Order IDs for Vehicle Related to You...", bg="#33A2FF", width=100)
        heading4 = Label(root, text="Vendor Info Assistant", bg="#33A2FF", width=100)

        # create a Name label
        self.order_uid = Label(root, text="Order UID", bg="#e2e8f0")
        self.parts = Label(root, text="Number of Parts", bg="#e2e8f0")
        self.vendor_name = Label(root, text="Vendor Name", bg="#e2e8f0")
        self.street = Label(root, text="Vendor Address Street", bg="#e2e8f0")
        self.city = Label(root, text="Vendor Address City", bg="#e2e8f0")
        self.state = Label(root, text="Vendor Address State", bg="#e2e8f0")
        self.postal_code = Label(root, text="Vendor Address Pincode", bg="#e2e8f0")
        self.phone_number = Label(root, text="Phone Number", bg="#e2e8f0")

        # Assistant Info
        vendors = self.dao.get_vendor_names()
        vendors = [vendor[0].ljust(15, ' ') + "   " + vendor[1] + ", " + vendor[2] + ", " + vendor[3] + ", " + str(vendor[4]) + ", " + str(vendor[5]) for vendor in vendors]
        vendors = ("\n").join([i for i in vendors])
        self.vendor_info = Label(root, text=vendors, bg="#e2e8f0")
        prev_orders = self.dao.get_previous_part_orders_by_user()
        user_specific_ordr_uids = set()
        order_uids = list(set([ entry[1] for entry in prev_orders]))
        associated_vehicle_with_user = self.dao.get_vehicle_list_for_curr_user()

        if len(associated_vehicle_with_user)==0:
            self.prev_orders = Label(root, text="No related Vehicles for this user", bg="#e2e8f0")
        else:
            associated_vehicle_with_user = list(set([entry[0] for entry in associated_vehicle_with_user]))
            for vin in associated_vehicle_with_user:
                for order in order_uids:
                    if vin in order:
                        user_specific_ordr_uids.add(order)
            user_specific_ordr_uids = list(user_specific_ordr_uids)
            for i in range(len(user_specific_ordr_uids)):
                if i %5 == 0 and i != 0:
                    user_specific_ordr_uids[i] = " \n"
            user_specific_ordr_uids = (", ").join(list(user_specific_ordr_uids))
            self.prev_orders = Label(root, text=user_specific_ordr_uids, bg="#e2e8f0", font='Helvetica 6 bold')

        # grid method is used for placing
        # the widgets at respective positions
        # in table like structure.
        heading1.grid(row=0, column=1, sticky=W)
        heading2.grid(row=6, column=1, sticky=W)
        heading3.grid(row=0, column=4)
        heading4.grid(row=6, column=4)
        self.order_uid.grid(row=1, column=0)
        #Label(root, text="", bg="#e2e8f0").grid(row=5, column=0)
        self.parts.grid(row=7, column=0)
        self.vendor_name.grid(row=8, column=0)
        self.street.grid(row=9, column=0)
        self.city.grid(row=10, column=0)
        self.state.grid(row=11, column=0)
        self.postal_code.grid(row=12, column=0)
        self.phone_number.grid(row=13, column=0)
        Label(root, text="             ", bg="#e2e8f0").grid(column=3)

        # Assistant Info
        self.prev_orders.grid(row=1, column=4)
        self.vendor_info.grid(row=7, column=4)

        # create a text entry box
        # for typing the information
        self.order_uid = Entry(root, width=1)
        self.parts = Entry(root, width=3)
        self.vendor_name = Entry(root, width=3)
        self.street = Entry(root, width=3)
        self.city = Entry(root, width=3)
        self.state = Entry(root, width=3)
        self.postal_code = Entry(root, width=3)
        self.phone_number = Entry(root, width=3)

        # grid method is used for placing
        # the widgets at respective positions
        # in table like structure.
        self.order_uid.grid(row=1, column=1, ipadx="100", sticky=W)
        self.parts.grid(row=7, column=1, ipadx="100", sticky=W)
        self.vendor_name.grid(row=8, column=1, ipadx="100", sticky=W)
        self.street.grid(row=9, column=1, ipadx="100", sticky=W)
        self.city.grid(row=10, column=1, ipadx="100", sticky=W)
        self.state.grid(row=11, column=1, ipadx="100", sticky=W)
        self.postal_code.grid(row=12, column=1, ipadx="100", sticky=W)
        self.phone_number.grid(row=13, column=1, ipadx="100", sticky=W)

        # create a Submit Button and place into the root window
        self.update_order_button = Button(root, text="Update Part Status", fg="Black",
                                    bg="#FF8A33", command=self.show_parts_for_order)
        self.update_order_button.grid(row=3, column=1)

        submit = Button(root, text="Order & Add Parts", fg="Black",
                        bg="#FF8A33", command=self.add_parts)
        submit.grid(row=14, column=1)
        root.mainloop()

    def add_parts(self):
        """
            Method which calls single part_form in a loop == number
        """
        valid_input = True
        if not (self.vendor_name.get()):
            self.popup_window("Error", "Enter All the Required Attributes")
            valid_input = False
        if valid_input:
            all_vendors = self.dao.get_all_vendor_names()
            if str(self.vendor_name.get()) in all_vendors:
                pass
            else:
                vendor_details = (str(self.vendor_name.get()), str(self.street.get()),
                                  str(self.city.get()), str(self.state.get()),
                                  int(str(self.postal_code.get())), int(str(self.phone_number.get())))
                self.dao.insert_vendor(vendor_details)
            part_num = int(self.parts.get())
            for i in range(part_num):
                self.part_form(i+1, part_num)
            part_form.destroy()

    def part_form(self, num, tot_num):
        global part_form
        part_form = Tk()
        # set the background colour of GUI window
        part_form.configure(background='#e2e8f0')
        # set the title of GUI window
        part_form.title("Single Part Order Form")
        # set the configuration of GUI window
        part_form.geometry("1000x200")
        Label(part_form, text="VIN").grid(row=0, column=0)
        Label(part_form, text="Cost").grid(row=0, column=1)
        Label(part_form, text="Description").grid(row=0, column=2)
        Label(part_form, text="Part Number").grid(row=0, column=3)
        Label(part_form, text="(Note: Do not enter Cost and Description if Part ID exists in Lookup Parts)").grid(row=2, column=1)

        self.single_part_vin = Entry(part_form, text="")
        self.single_part_vin.grid(row=1, column=0)
        self.single_part_cost = Entry(part_form, text="")
        self.single_part_cost.grid(row=1, column=1)
        self.single_part_desc = Entry(part_form, text="")
        self.single_part_desc.grid(row=1, column=2)
        self.single_part_part_no = Entry(part_form, text="")
        self.single_part_part_no.grid(row=1, column=3)
        self.submit_part = Button(part_form, text="Add Part to Order", fg="Black", bg="#ADD8E6", command=self.update_part_order_parent)
        self.submit_part.grid(row=1, column=4)
        indicator = Button(part_form, text="Part" + str(num) + " of " + str(tot_num), fg="Black", bg="light blue")
        indicator.grid(row=2, column=4)
        indicator.configure(state='disabled')
        part_form.mainloop()

    def get_order_id(self, vin):
        for ordr_id in self.insert_single_part_parent:
            if vin in ordr_id:
                return ordr_id
        res = self.dao.get_latest_order_ids_for_vin(vin)
        if len(res) ==0 :
            return vin + "-001"
        else:
            vin = res[0][0]
            vin_ordr_list = [entry[1] for entry in res]
            vin_ordr_list = list(set(vin_ordr_list))
            order_subsc = max([int(i.split("-")[1]) for i in vin_ordr_list]) + 1
            order_subsc = ('{:03d}'.format(order_subsc))
            id = vin + "-" + str(order_subsc)
            return id

    def update_part_order_parent(self):
        """Calls DB Inserts for Part, PartOrder and Contains"""
        if not (self.single_part_vin.get() and self.single_part_part_no.get()):
            self.popup_window("Error", "Please Enter All the Required Attributes")
        self.next_part_flag = True
        self.submit_part.configure(state='disabled')
        existing_part_ids = [entry[0] for entry in self.dao.get_part_ids()]
        if str(self.single_part_part_no.get()) in existing_part_ids:
            entry = self.dao.get_part_details_for_part(str(self.single_part_part_no.get()))
            self.single_part_desc = entry[0]
            self.single_part_cost = entry[1]
        else:
            part_tmp = (str(self.single_part_part_no.get()), str(self.single_part_cost.get()), str(self.single_part_desc.get()))
            self.dao.insert_part(part_tmp)
        self.single_part_order_number = self.get_order_id(str(self.single_part_vin.get()))
        order_tmp = (str(self.single_part_vin.get()), str(self.vendor_name.get()), None, self.single_part_order_number)
        contains_tmp = (self.single_part_order_number, str(self.single_part_part_no.get()), "ordered")
        if not self.single_part_order_number in list(self.insert_single_part_parent):
            self.insert_single_part_parent.add(self.single_part_order_number)
            self.dao.insert_part_order(order_tmp)
        self.dao.insert_contains(contains_tmp)
        part_form.quit()

    def show_parts_for_order(self):
        """
            This method is auxilary UI method to specify paricular Part from previously mentioned OrderID
        """
        show_parts_for_order_form = Tk()
        show_parts_for_order_form.configure(background='#e2e8f0')
        # set the title of GUI window
        show_parts_for_order_form.title("Select Part For Entered Order")
        # set the configuration of GUI window
        show_parts_for_order_form.geometry("400x100")
        Label(show_parts_for_order_form, text="Select Part").grid(row=1, column=2)
        self.order_number = str(self.order_uid.get())
        PART_OPTIONS = self.dao.get_parts_associated_with_order(self.order_number)
        PART_OPTIONS = [entry[0] for entry in PART_OPTIONS]
        self.part_number_drop_down = StringVar(show_parts_for_order_form)
        self.part_number_drop_down.set(PART_OPTIONS[0])  # default value
        OptionMenu(show_parts_for_order_form, self.part_number_drop_down, *PART_OPTIONS).grid(row=3, column=2)
        self.go_to_this_part = Button(show_parts_for_order_form, text="GO TO THIS PART", fg="Black", bg="Red",
                                                command=self.update_part_status)
        self.go_to_this_part.grid(row=4, column=2)


    def update_part_status(self):
        """
            This is UI related method to show Update Part Status Form
        """
        self.part_number = str(self.part_number_drop_down.get())
        entry = self.dao.get_part_info((self.order_number, self.part_number))[0]
        update_part_form = Tk()
        update_part_form.configure(background='#e2e8f0')
        update_part_form.title("Part Status Update Form")
        update_part_form.geometry("400x100")
        Label(update_part_form, text="VIN").grid(row=0, column=0)
        Label(update_part_form, text="Cost").grid(row=0, column=1)
        Label(update_part_form, text="Description").grid(row=0, column=2)
        Label(update_part_form, text="Status").grid(row=0, column=3)
        curr_status = entry[-1]
        if curr_status == "ordered":
            OPTIONS = ["ordered", "received", "installed"]
        elif curr_status == "received":
            OPTIONS = ["received", "installed"]
        else:
            OPTIONS = ["installed"]
        self.variable_status = StringVar(update_part_form)
        self.variable_status.set(OPTIONS[0])  # default value
        OptionMenu(update_part_form, self.variable_status, *OPTIONS).grid(row=1, column=3)

        part_vin, part_cost, part_desc = entry[0], entry[1], entry[2]
        Label(update_part_form, text=part_vin).grid(row=1, column=0)
        Label(update_part_form, text=part_cost).grid(row=1, column=1)
        Label(update_part_form, text=part_desc).grid(row=1, column=2)

        self.update_part_status_button = Button(update_part_form, text="Update Status", fg="Black", bg="#ADD8E6", command=self.update_part)
        self.update_part_status_button.grid(row=1, column=4)
        if curr_status == "installed":
            self.update_part_status_button.configure(state="disabled")
        update_part_form.mainloop()

    def update_part(self):
        """
            This updates the status of Particular Part calls DAO method
        """
        status = str(self.variable_status.get())
        self.dao.update_part_status(status, self.order_number, self.part_number)
        self.update_part_status_button.configure(state="disabled")

    def insert(self):
        self.next_part_flag = True
        self.submit_part.configure(state='disabled')
        part_form.quit()
        return

    def popup_window(self, title, message):
        global popup_win
        popup_win = Tk()
        popup_win.title(title)
        popup_win.geometry("200x100")
        Label(popup_win, text=message).pack()
        Button(popup_win, text="OK", command=self.delete_popup_window).pack()
        popup_win.mainloop()

    def delete_popup_window(self):
        popup_win.destroy()