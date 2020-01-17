from model.dao import Dao
class LoginService:

    def __init__(self):
        self.dao = Dao().get_instance()

    def login(self, username, password):
        if self.authenticate_user(username, password):
            return True
        else:
            return False

    def authenticate_user(self,username,password):
        records = self.dao.check_if_valid_user(username,password)
        if len(records)==0:
            return False
        else:
            return True