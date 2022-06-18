
from PySide6.QtWidgets import QMessageBox
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from decouple import config
import bcrypt

class Database:
    def __init__(self):
        pass 
    
    def start_connection(self, dbName="db.sqlite3"):
        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName(dbName)
        
        if not self.conn.open():
            QMessageBox.critical(
                None,
                config("APP_NAME"),
                f"Database Connection Error: {self.conn.lastError().text()}",
            )
            return False 
        self.create_user_table()
        self.create_todo_table()
        return True 
    
    def close_connection(self):
        self.conn.close()
        
    def get_tables_list(self):
        return QSqlDatabase.database().tables()
    
    def check_table_exists(self, tableName):
        return tableName in self.get_tables_list()
    
    def get_existing_emails(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT email from users
            """
        )
        emails = []
        while query.next():
            emails.append(query.value('email'))
        # print('EMAILS: ',emails)
        return emails

    def get_user_ids(self):
        query = QSqlQuery()
        query.exec(
            "SELECT id from users"
        )
        ids = []
        while query.next():
            ids.append(query.value('id'))
        return ids
    
    def check_user_exists(self, user_id):
        return user_id in self.get_user_ids()
    
    def attempt_login(self,email,password):
        userData = {}
        query = QSqlQuery()
        query.exec("SELECT id,name,email,password FROM users WHERE email='"+email+"'")
        if not query.next():
            return {"status":"error","message":"Invalid Email!","data":{}}
        else:
            userData['id'] = query.value('id')
            userData['name'] = query.value('name')
            userData['email'] = query.value('email')
            userData['password'] = query.value('password')
        loginCheck = False 
        try:
            loginCheck = bcrypt.checkpw(password.encode('utf-8'), userData['password'].encode('utf-8'))
        except Exception as ex:
            return {"status":"error","message":"Wrong Password!","data":{}}
        if not loginCheck:
            return {"status":"error","message":"Wrong Password!","data":{}}
        return  {"status":"success","message":"Login Successfull!","data":userData}
    
    def create_user_table(self):
        query = QSqlQuery()
        if not self.check_table_exists('users'):
            return query.exec(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password text NOT NULL
                )
                """
            )
        return False
    
    def create_todo_table(self):
        query = QSqlQuery()
        if not self.check_table_exists('todos'):
            return query.exec(
                """
                CREATE TABLE todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description VARCHAR(100) UNIQUE NOT NULL,
                    status string NOT NULL,
                    created_at DATE,
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON DELETE CASCADE
                )
                """
            )
            
    def seed_todo(self):
        query = QSqlQuery()
        return query.exec("""INSERT INTO todos (user_id, title, description, status, created_at) 
                   VALUES (1,'test todo','blah blah','not_completed','2022-01-20')""") 
    
    def seed_user(self):
        pw = b"password"
        data = [
            ("Clark Kent", "clark@gmail.com", bcrypt.hashpw(pw, bcrypt.gensalt())),
            ("Bruce Wayne", "bruce@gmail.com", bcrypt.hashpw(pw, bcrypt.gensalt())),
            ("Barry Allen", "barry@gmail.com", bcrypt.hashpw(pw, bcrypt.gensalt())),
            ("Tony Stark", "tony@gmail.com", bcrypt.hashpw(pw, bcrypt.gensalt())),
            ("Peter Parker", "peter@gmail.com", bcrypt.hashpw(pw, bcrypt.gensalt()))
        ]
        query = QSqlQuery()
        query.prepare(
            """
               INSERT INTO users (
                   name, email,  password
               ) 
               VALUES (?,?,?)
            """
        )
        #Insert sample data
        for name, email, hashed_password in data:
            query.addBindValue(name)
            query.addBindValue(email)
            query.addBindValue(hashed_password.decode('utf-8'))
            query.exec()
       
       
    def create_user(self,data):
        query = QSqlQuery()
        query.prepare(
            """
               INSERT INTO users (
                   name, email,  password
               ) 
               VALUES (?,?,?)
            """
        )
        #Insert sample data
        for name, email, password in data:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query.addBindValue(name)
            query.addBindValue(email)
            query.addBindValue(hashed_password.decode('utf-8'))
            query.exec()
"""
if bcrypt.checkpw(b"password", "$afdsfs....".encode('utf-8')):
    print('matched')
else:
    print('not matched!')
"""