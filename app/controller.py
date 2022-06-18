from decouple import config
import bcrypt

class Controller:
    def __init__(self):
        pass
    def init_db(self, db):
        self.db = db
        
    def attempt_login(self, data):
        pass 
    
    def register_user(self, data):
        pass