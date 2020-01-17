from model.dao import Dao
class PublicPageService:

    def __init__(self):
        self.dao = Dao().get_instance()


    def list_vehicles(self):
        return self.dao.list_public_vehicles()

    def filter_vehicles(self, records):
        vin_sell_list = self.dao.get_vins_in_sell()
        vin_sell_list = list(vin_sell_list)
        filtered_records = []
        for record in records:
            if record[0] not in vin_sell_list and self.dao.if_all_orders_completed(record[0]):
                filtered_records.append(record)
        new_records = []
        for record in filtered_records:
            new_records.append(list(record))
        for record in new_records:
            new_records[new_records.index(record)][5] = self.dao.get_selling_price_of_vehicle(record[0])
        filtered_records = []
        for record in new_records:
            filtered_records.append(tuple(record))
        return filtered_records

    def list_vehicles_vehicle_type(self, vehicle_type):
        records = self.dao.list_vehicles_vehicle_type(vehicle_type)
        records = self.filter_vehicles(records)
        return records

    def list_vehicle_mfg_name(self, mfg_name):
        records = self.dao.list_vehicles_mfg_name(mfg_name)
        records = self.filter_vehicles(records)
        return records

    def list_vehicle_model_year(self, model_year):
        records = self.dao.list_vehicle_model_year(model_year)
        records = self.filter_vehicles(records)
        return records

    def list_vehicle_color(self,color):
        records = self.dao.list_vehicle_color(color)
        records = self.filter_vehicles(records)
        return records

    def list_vehicle_any_keyword(self, keyword):
        records = self.dao.list_vehicle_any_keyword(keyword)
        records = self.filter_vehicles(records)
        return records

    def vehicle_available_for_purchase(self):
        records = self.list_vehicles()
        records = self.filter_vehicles(records)
        return len(records)

    def list_vehicle_vin(self,vin):
        records = self.dao.list_vehicle_vin(vin)
        records = self.filter_vehicles(records)
        return records