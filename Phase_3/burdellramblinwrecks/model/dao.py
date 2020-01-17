import const
import mysql.connector
from mysql.connector import Error

class Dao:

    __instance = None
    def __init__(self):
        self.connection = self.establish_connection()

    def get_instance(self):
        if self.__instance is None:
            self.__instance = Dao()
        return self.__instance

    @staticmethod
    def establish_connection():
        try:
            return mysql.connector.connect(host='10.221.197.238',
                                    database='test_demo_burdell',
                                    user='team60',
                                    password='Omscs@team60',
                                    auth_plugin='caching_sha2_password', port=12345)

        except Error as e:
            print("Error while connecting to the database", e)

    def get_temp_data(self):
        cursor = self.connection.cursor()
        cursor.execute("Select * from Vehicle")
        records = cursor.fetchall()
        return records

    def check_if_valid_user(self, username, password):
        cursor = self.connection.cursor()
        query = "Select username,pass_word from PriviledgedUser where username=%s and pass_word=%s;"
        arguments = (username,password)
        cursor.execute(query,arguments)
        records = cursor.fetchall()
        return records


    def get_user_type(self, username, password):
        cursor = self.connection.cursor()
        query = "Select priviledge_user_type from PriviledgedUser where username=%s and pass_word=%s;"
        arguments = (username, password)
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def list_public_vehicles(self):
        cursor = self.connection.cursor()
        cursor.execute("select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name "
                       "from Vehicle v inner join Manufacturer m "
                       "on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id order by vin;")
        records = cursor.fetchall()
        return records

    def fetch_vehicle_color(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select color from VehicleColor where FK_vin_vehicle=%s;"
        cursor.execute(query,arguments)
        records = cursor.fetchall()
        return records

    def add_vehicle_color(self, records):
        new_records = []
        for record in records:
            colors = self.fetch_vehicle_color(record[0])
            temp_colors = []
            for col in colors:
                temp_colors.append(str(col[0]))
            col_str = ','.join(temp_colors)
            record = record + (col_str,)
            new_records.append(record)
        return new_records

    def list_vehicles_vehicle_type(self, vehicle_type):
        cursor = self.connection.cursor()
        arguments = (vehicle_type,)
        query = "select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name from Vehicle v " \
                "inner join Manufacturer m on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id " \
                "where locate(%s, v.vehicle_type)>0 order by vin;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records

    def list_vehicles_mfg_name(self, mfg_name):
        cursor = self.connection.cursor()
        arguments = (mfg_name,)
        query = "select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name from Vehicle v " \
                "inner join Manufacturer m on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id " \
                "where locate(%s, m.Manufacturer_name)>0 order by vin;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records

    def list_vehicle_model_year(self, model_year):
        cursor = self.connection.cursor()
        arguments = (model_year,)
        query = "select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name from Vehicle v " \
                "inner join Manufacturer m on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id " \
                "where locate(%s, v.model_year)>0 order by vin;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records

    def list_vehicle_color(self, color):
        new_records = []
        records = self.list_public_vehicles()
        records = self.add_vehicle_color(records)
        for record in records:
            if str(record[len(record)-1]).find(color)>=0:
                new_records.append(record)
        return new_records

    def list_vehicle_any_keyword(self, keyword):
        cursor = self.connection.cursor()
        arguments = (keyword,keyword,keyword,keyword)
        query = "select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name from Vehicle v " \
                "inner join Manufacturer m on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id " \
                "where locate(%s, m.Manufacturer_name)>0 OR locate(%s, v.model_year)>0 OR " \
                "locate(%s, v.model_name)>0 OR locate(%s, v.description)>0 order by vin;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records

    def list_vehicle_vin(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select vin,vehicle_type,model_year,model_name,mileage,cost, m.Manufacturer_name from Vehicle v " \
                "inner join Manufacturer m on v.Fk_manufacturer_manufacturerid = m.Manufacturer_id " \
                "where locate(%s, v.vin)>0 order by vin;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records


    def list_vehicle_sold(self):
        cursor = self.connection.cursor()
        query = "select vin,vehicle_type,model_year,model_name,mileage, cost, " \
                "Manufacturer_name, group_concat(color separator ',') as color from ((Vehicle inner join Manufacturer) " \
                "inner join VehicleColor) inner join Sell where Sell.FK_vin_vehicle=Vehicle.vin and " \
                "Vehicle.vin=VehicleColor.FK_vin_vehicle and Vehicle.Fk_manufacturer_manufacturerid=Manufacturer.manufacturer_id  " \
                "group by vin order by vin asc;"
        cursor.execute(query)
        records = cursor.fetchall()
        records = self.add_vehicle_color(records)
        return records

    def list_vehicle_unsold(self):
        cursor = self.connection.cursor()
        query = "select vin,vehicle_type,model_year,model_name,mileage, cost, Manufacturer_name, " \
                "group_concat(color separator ',') as color from (Vehicle inner join Manufacturer) inner join " \
                "VehicleColor where Vehicle.vin=VehicleColor.FK_vin_vehicle and " \
                "Vehicle.Fk_manufacturer_manufacturerid=Manufacturer.manufacturer_id and vin not in " \
                "(select FK_vin_vehicle from Sell) group by vin order by vin asc;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def list_vehicle_all(self):
        cursor = self.connection.cursor()
        query = "select vin,vehicle_type,model_year,model_name,mileage, cost, Manufacturer_name, " \
                "group_concat(color separator ',') as color from (Vehicle inner join Manufacturer) inner join VehicleColor " \
                "where Vehicle.vin=VehicleColor.FK_vin_vehicle and Vehicle.Fk_manufacturer_manufacturerid=Manufacturer.manufacturer_id " \
                "group by vin order by vin asc;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def list_customers_taxId(self, filter_text):
        cursor = self.connection.cursor()
        arguments = (filter_text,)
        query = "select * from Business where locate(%s,taxIDNumber);"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def list_customers_license(self, filter_text):
        cursor = self.connection.cursor()
        arguments = (filter_text,)
        query = "select * from Individual where locate(%s, driverLicenseNumber);"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def count_all_customers(self):
        cursor = self.connection.cursor()
        query = "select max(customerID) from Customer;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records[0][0]

    def insert_individual_customer(self, cust_vals, ind_vals):
        cursor = self.connection.cursor()
        query = "insert into Customer values (%s,%s, %s, %s, %s, %s, %s);"
        cursor.execute(query,cust_vals)
        self.connection.commit()
        cursor = self.connection.cursor()
        query = "insert into Individual values (%s,%s,%s,%s);"
        cursor.execute(query,ind_vals)
        self.connection.commit()

    def insert_business_customer(self,cust_vals,buss_vals):
        cursor = self.connection.cursor()
        query = "insert into Customer values (%s,%s, %s, %s, %s, %s, %s);"
        cursor.execute(query, cust_vals)
        self.connection.commit()
        cursor = self.connection.cursor()
        query = "insert into Business values (%s, %s, %s, %s, %s, %s);"
        cursor.execute(query, buss_vals)
        self.connection.commit()

    def insert_vehicle(self, vals):
        cursor = self.connection.cursor()
        arguments = vals
        query = "INSERT INTO Vehicle (vin, vehicle_type, cost, model_name, model_year, "\
                 "Fk_manufacturer_manufacturerid, mileage, description) "\
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, arguments)
        self.connection.commit()

    def insert_vehicle_color(self, vals):
        cursor = self.connection.cursor()
        arguments = vals
        query = "INSERT INTO VehicleColor (FK_vin_vehicle, color) VALUES (%s, %s)"
        res = cursor.execute(query, arguments)
        self.connection.commit()

    def get_vehicle_cost(self, vin):
        cursor = self.connection.cursor()
        query = "select cost From Vehicle where vin = %s;"
        args = (vin,)
        cursor.execute(query,args)
        records = cursor.fetchall()
        return records

    def get_selling_price_of_vehicle(self, vin):
        records = self.get_vehicle_cost(vin)
        cost = records[0][0]
        cost = cost * 1.25
        order_ids = self.get_orders_for_vehicle(vin)
        parts_cost = 0
        if len(order_ids) > 0:
            parts_cost = self.get_parts_cost_given_order_id(order_ids)
            parts_cost = parts_cost * 1.1
        return cost + parts_cost

    def get_parts_cost_given_order_id(self, order_ids):
        ids = list(order_ids)
        cursor = self.connection.cursor()
        query = "select Contains.Fk_contains_orderID, sum(cost) from Part,Contains where Part.partNumber = Contains.Fk_contains_partnumber group by Contains.Fk_contains_orderID;"
        cursor.execute(query)
        records = cursor.fetchall()
        cost = 0
        for record in records:
            if record[0] in ids:
                cost += record[1]
        return cost

    def get_part_status_for_order(self, order_id):
        cursor = self.connection.cursor()
        args = (order_id,)
        query = "select Contains.Fk_contains_partnumber, Contains.PartStatus from Contains where Fk_contains_orderID =%s;"
        cursor.execute(query, args)
        records = cursor.fetchall()
        return records

    def if_all_orders_completed(self, vin):
        any_order_pending = False
        order_ids = self.get_orders_for_vehicle(vin)
        for order in order_ids:
            parts = self.get_part_status_for_order(order)
            for part in parts:
                if part[1] != "installed":
                    any_order_pending = True
        return not any_order_pending

    def get_orders_for_vehicle(self, vin):
        cursor = self.connection.cursor()
        args = (vin,)
        query = "select orderID from PartOrder where FK_vin_part_order =%s;"
        cursor.execute(query,args)
        records = cursor.fetchall()
        order_list = []
        for r in records:
            order_list.append(r[0])
        return order_list

    def seller_history_report(self):
        cursor = self.connection.cursor()
        cursor.execute("select Name, count(vehicles) as total_number_of_vehicles, avg(purchase_price) as "
                       "average_purchase_price ,ceil(avg(number_of_parts)) as average_number_of_parts, "
                       "(sum(cost)/count(vehicles)) as average_cost_of_parts from (select Buy.FK_vin_vehicle as vehicles, "
                       "Buy.FK_customer_id_customer as cid, coalesce(sum(cost),0) as cost, purchase_price, "
                       "count(Fk_contains_partnumber) as total_parts, count(orderID) as number_of_parts, "
                       "concat(coalesce(Individual.first_name, ''), coalesce(Business.first_name, '')) as Name  "
                       "from ((Buy left join ((PartOrder inner join Contains on PartOrder.orderID=Contains.Fk_contains_orderID) "
                       "inner join Part on Contains.Fk_contains_partnumber=Part.partNumber) on Buy.FK_vin_vehicle=FK_vin_part_order) "
                       "left join Individual on Individual.FK_individual_customer_id=FK_customer_id_customer) left join "
                       "Business on Business.FK_business_customer_id=FK_customer_id_customer  group by  Buy.FK_vin_vehicle, "
                       "FK_vin_part_order, FK_customer_id_customer, Individual.first_name, Business.first_name) as T group by "
                       "cid, Name order by total_number_of_vehicles desc, average_purchase_price asc;")
        records = cursor.fetchall()
        return records

    def average_time_in_inventory_report(self):
        cursor = self.connection.cursor()
        cursor.execute("select vehicle_type, coalesce(floor(avg(datediff(sales_date, purchase_date))), 'N/A') "
                       "as average_time from Vehicle left join (Buy left  join Sell "
                       "on Buy.FK_vin_vehicle=Sell.FK_vin_vehicle) on Vehicle.vin=Buy.FK_vin_vehicle  "
                       "group by vehicle_type;")
        records = cursor.fetchall()
        return records

    def price_per_condition_report(self):
        cursor = self.connection.cursor()
        cursor.execute("select vehicle_type, coalesce(avg(case when vehicle_condition = 'Fair' "
                       "then purchase_price end), '$0') as Fair, coalesce(avg(case when vehicle_condition = 'Good' "
                       "then purchase_price End), '$0') as Good, coalesce(avg(case when vehicle_condition = 'Very Good' "
                       "then purchase_price End), '$0') as Very_Good, coalesce(avg(case "
                       "when vehicle_condition = 'Excellent' then purchase_price End), '$0') as Excellent from  Vehicle "
                       "left join (Buy left join Sell on Buy.FK_vin_vehicle=Sell.FK_vin_vehicle) "
                       "on Vehicle.vin = Buy.FK_vin_vehicle group by vehicle_type;")
        records = cursor.fetchall()
        return records

    def parts_statistics_report(self):
        cursor = self.connection.cursor()
        cursor.execute("select vendorName, count(*) as NumberOfParts, sum(cost) from ((PartOrder inner join Contains) "
                       "inner join Part) inner join Vendor where PartOrder.orderID = Contains.Fk_contains_orderID and "
                       "PartOrder.FK_vendor_name_part_order=Vendor.vendorName and Contains.Fk_contains_partnumber=Part.partNumber "
                       "group by vendorName;")
        records = cursor.fetchall()
        return records

    def monthly_loan_income_report(self):
        cursor = self.connection.cursor()
        cursor.execute("select start_month, sum(month_payment), sum((month_payment/100)) as Burdell_Share from "
                       "Loan where date_add(concat(start_month, '-',day(curdate())), INTERVAL "
                       "loanterm MONTH) >= date_add(curdate(), INTERVAL -12 MONTH) and start_month < date_add(curdate(), "
                       "INTERVAL -1 MONTH) group by start_month order by start_month ASC;")
        records = cursor.fetchall()
        return records

    def monthly_sales_report_summary(self):
        cursor = self.connection.cursor()
        cursor.execute("select date_format(sales_date, '%Y-%m') as date, count(*) as number_of_vehicles_sold, "
                       "sum(sales_price) as total_sales_income, total_net_income from "
                       "(select  Sell.FK_vin_vehicle, sales_date, sales_price, ((sum(sales_price) - "
                       "sum(purchase_price)) - sum(coalesce(cost, 0))) as total_net_income from (((Sell left join Buy on "
                       "Sell.FK_vin_vehicle=Buy.FK_vin_vehicle) left join PartOrder on PartOrder.FK_vin_part_order=Sell.FK_vin_vehicle) "
                       "left join Contains on PartOrder.orderID=Contains.Fk_contains_orderID) left join Part "
                       "on Contains.Fk_contains_partnumber=Part.partNumber group by FK_vin_vehicle) as T group by date "
                       "order by date desc;")
        records = cursor.fetchall()
        return records

    def monthly_Sales_report_drilldown(self, date):
        cursor = self.connection.cursor()
        query = "select concat(first_name, last_name) as Name, count(FK_vin_vehicle) as Total_Vehicles_Sold, " \
                "sum(sales_price) as total_sales from Sell inner join PriviledgedUser where " \
                "Sell.FK_username_privileged_user_sell=PriviledgedUser.username and date_format(sales_date, '%Y-%m')= '" + date + "' " \
                "group by name order by Total_Vehicles_Sold desc, total_sales desc;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def get_vendor_names(self):
        cursor = self.connection.cursor()
        query = "select vendorName, street, city, state, postal_code, phone_number from Vendor;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records;

    def get_previous_part_orders_by_user(self):
        cursor = self.connection.cursor()
        query = "select PartOrder.FK_vin_part_order,PartOrder.orderID, Contains.Fk_contains_partnumber, Part.cost,  Contains.PartStatus, Part.description " \
                "from ((PartOrder inner join Contains) inner join Part) inner join Vendor " \
                "where PartOrder.orderID = Contains.Fk_contains_orderID and PartOrder.FK_vendor_name_part_order=Vendor.vendorName " \
                "and Contains.Fk_contains_partnumber=Part.partNumber;"
        cursor.execute(query)
        records = cursor.fetchall()
        return records;

    def insert_vendor(self, vals):
        cursor = self.connection.cursor()
        query = "INSERT INTO Vendor (vendorName, street, city, state, postal_code, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
        arguments = vals
        res = cursor.execute(query, arguments)
        self.connection.commit()

    def get_part_info(self, vals):
        cursor = self.connection.cursor()
        query = "select PartOrder.FK_vin_part_order, Part.cost, Part.description, Contains.PartStatus " \
                "from ((PartOrder inner join Contains) inner join Part) inner join Vendor " \
                "where PartOrder.orderID = Contains.Fk_contains_orderID " \
                "and PartOrder.FK_vendor_name_part_order=Vendor.vendorName " \
                "and Contains.Fk_contains_partnumber=Part.partNumber " \
                "and Contains.Fk_contains_orderID=%s and Contains.Fk_contains_partnumber=%s"
        arguments = vals
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records;

    def update_part_status(self, status, order_id, part_id):
        cursor = self.connection.cursor()
        query = "UPDATE Contains SET PartStatus=%s WHERE Fk_contains_orderID=%s and Fk_contains_partnumber=%s"
        arguments = (status, order_id, part_id)
        cursor.execute(query, arguments)
        self.connection.commit()

    def get_vehicle_list_for_curr_user(self):
        cursor = self.connection.cursor()
        query = "select FK_vin_vehicle from Buy where FK_username_privileged_user_buy=%s"
        arguments = (const.CURRENT_USER,)
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records;

    def get_parts_associated_with_order(self, order_id):
        cursor = self.connection.cursor()
        query = "select Fk_contains_partnumber from Contains where Fk_contains_orderID=%s"
        arguments = (order_id,)
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records;

    def get_latest_order_ids_for_vin(self, vin):
        cursor = self.connection.cursor()
        query = "select PartOrder.FK_vin_part_order,PartOrder.orderID " \
                "from ((PartOrder inner join Contains) inner join Part) inner join Vendor where PartOrder.orderID = Contains.Fk_contains_orderID" \
                " and PartOrder.FK_vendor_name_part_order=Vendor.vendorName and Contains.Fk_contains_partnumber=Part.partNumber " \
                "and PartOrder.FK_vin_part_order=%s"
        arguments = (vin,)
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def insert_part(self, vals):
        cursor = self.connection.cursor()
        query = "INSERT INTO Part (partNumber, cost, description) values (%s, %s, %s)"
        arguments = vals
        res = cursor.execute(query, arguments)
        self.connection.commit()

    def insert_part_order(self, vals):
        cursor = self.connection.cursor()
        query = "INSERT INTO PartOrder (FK_vin_part_order, FK_vendor_name_part_order, FK_user_name_part_order, orderID) values (%s, %s, %s, %s)"
        arguments = vals
        res = cursor.execute(query, arguments)
        self.connection.commit()

    def insert_contains(self, vals):
        cursor = self.connection.cursor()
        query = "INSERT INTO Contains (Fk_contains_orderID, Fk_contains_partnumber, PartStatus) values (%s, %s, %s)"
        arguments = vals
        res = cursor.execute(query, arguments)
        self.connection.commit()

    def get_vins_in_sell(self):
        cursor = self.connection.cursor()
        query = "Select * from Sell"
        cursor.execute(query)
        records = cursor.fetchall()
        vin_list = []
        for record in records:
            vin_list.append(record[0])
        vin_list = list(set(vin_list))
        return vin_list

    def if_any_orders_pending(self, vin):
        any_order_pending = False
        order_ids = self.get_orders_for_vehicle(vin)
        for order in order_ids:
            parts = self.get_part_status_for_order(order)
            for part in parts:
                if part[1] == "received" or part[1] == "ordered":
                    any_order_pending = True
        return any_order_pending

    def get_parts_cost(self,vin):
        order_ids = self.get_orders_for_vehicle(vin)
        cost = self.get_parts_cost_given_order_id(order_ids)
        return cost

    def insert_into_sell(self, args):
        cursor = self.connection.cursor()
        arguments = (args[2],int(args[1].get()),float(args[4]),args[0].get(),args[3],)
        query = "INSERT INTO Sell (FK_vin_vehicle, FK_customer_id_customer, sales_price, sales_date, " \
                "FK_username_privileged_user_sell) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, arguments)
        self.connection.commit()

    def insert_into_loan(self, args):
        cursor = self.connection.cursor()
        arguments = args
        query = "INSERT INTO Loan (FK_vin_loan, FK_username_priveledged_user, loanterm, interest_rate, " \
                "down_payment,month_payment,start_month) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query, arguments)
        self.connection.commit()

    def insert_buy(self, vals):
        cursor = self.connection.cursor()
        arguments = vals
        query = "INSERT INTO Buy (FK_vin_vehicle, FK_customer_id_customer, FK_username_privileged_user_buy," \
                " purchase_price, purchase_date, vehicle_condition) " \
                "VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, arguments)
        self.connection.commit()

    def get_vehicle_description(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "Select description from Vehicle where vin=%s;"
        cursor.execute(query,arguments)
        records = cursor.fetchall()
        return records[0]

    def get_seller_info(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select concat(coalesce(Individual.first_name, ''), coalesce(Business.first_name, '')), " \
                "email_address, phone_number, street, postal_code, city, state, purchase_price,purchase_date, " \
                "FK_username_privileged_user_buy, concat(coalesce(contact_title, '0')) from ((Buy inner join Customer) " \
                "left join Individual on Individual.FK_individual_customer_id=Customer.customerID) left join Business " \
                "on Business.FK_business_customer_id=Customer.customerID where " \
                "Buy.FK_customer_id_customer=Customer.customerID  and FK_vin_vehicle=%s;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def get_loan_details(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select * from Loan where FK_vin_loan=%s;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def get_sell_info(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select sales_price, sales_date, concat(pname, plname), concat(coalesce(Iname, ''), coalesce(Bname, '')) " \
                "from (select sales_price, sales_date, PriviledgedUser.first_name as pname, PriviledgedUser.last_name " \
                "as plname, concat(Individual.first_name, ' ', Individual.last_name) as Iname, " \
                "concat(Business.first_name, ' ', Business.last_name) as Bname  from ((Sell inner join PriviledgedUser) " \
                "left join Individual on Sell.FK_customer_id_customer=Individual.FK_individual_customer_id) left join " \
                "Business on Sell.FK_customer_id_customer=Business.FK_business_customer_id where " \
                "FK_username_privileged_user_sell=PriviledgedUser.username and FK_vin_vehicle=%s) as T;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records


    def get_parts_details_for_vehicle(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select PartOrder.orderID, Contains.Fk_contains_partnumber, Contains.PartStatus, Part.cost, Part.description, Vendor.vendorName from ((PartOrder inner join Contains) inner join Part) inner join Vendor where PartOrder.orderID = Contains.Fk_contains_orderID and PartOrder.FK_vendor_name_part_order=Vendor.vendorName and Contains.Fk_contains_partnumber=Part.partNumber and PartOrder.FK_vin_part_order=%s;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def get_buy_date_for_vin(self, vin):
        cursor = self.connection.cursor()
        arguments = (vin,)
        query = "select purchase_date from Buy where FK_vin_vehicle =%s;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records[0][0]

    def get_part_ids(self):
        cursor = self.connection.cursor()
        query = "select partNumber from Part;"
        cursor.execute(query)
        records = cursor.fetchall()
        return list(records)


    def get_part_details_for_part(self, part_no):
        cursor = self.connection.cursor()
        arguments = (part_no,)
        query = "select description, cost from Part where partNumber=%s;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records[0]

    def get_all_vehicle_parts(self,filter_text):
        cursor = self.connection.cursor()
        arguments = (filter_text, filter_text, filter_text)
        query = "select * from Part where locate(%s,partNumber)>0 OR locate(%s,cost)>0 OR locate(%s,description)>0;"
        cursor.execute(query, arguments)
        records = cursor.fetchall()
        return records

    def get_all_vendor_names(self):
        cursor = self.connection.cursor()
        query = "select vendorName from Vendor;"
        cursor.execute(query)
        records = cursor.fetchall()
        name_list = []
        for record in records:
            name_list.append(record[0])
        return name_list