
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
                                    database='burdell',
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
