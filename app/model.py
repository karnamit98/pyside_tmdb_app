from email.quoprimime import header_check
from PySide6.QtCore import Qt 
from PySide6.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation
import bcrypt

class UserModel:
    def __init__(self):
        self.model = self.create_model()
        
    @staticmethod
    def create_model():
        """Create and setup model"""
        model = QSqlTableModel()
        model.setTable('users')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()      #loads the table
        header_fields = ("id", "Name", "Email", "Password")
        # print(header_fields)
        for column, header in enumerate(header_fields):
            model.setHeaderData(column, Qt.Horizontal, header)
        return model
     
    def refresh_model(self):
        self.model.select()
        
    def add_user(self, data):
        rows = self.model.rowCount()
        print('add_user',rows)
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            # print('column:',column,', field:',field)
            #hash password
            if column==2:
                field = bcrypt.hashpw(bytes(field, encoding='utf-8'), bcrypt.gensalt()).decode()
            self.model.setData(self.model.index(rows, column+1), field)
        self.model.submitAll()
        self.model.select()
        
    def delete_user(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
        
    def clearUsers(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        
    
class TodoModel:
    def __init__(self):
        self.model = self.create_model()
        
    @staticmethod
    def create_model():
        """Create and setup model"""
        model = QSqlRelationalTableModel()
        model.setTable('todos')
        model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
        model.setRelation(1, QSqlRelation("users", "id", "name"))
        model.select()      #loads the table
        header_fields = ("id", "User", "Title", "Description", "Status", "Created At")
        # print(header_fields)
        for column, header in enumerate(header_fields):
            model.setHeaderData(column, Qt.Horizontal, header)
        return model
        
    def refresh_model(self):
        self.model.select()
        
    def add_todo(self, data):
        rows = self.model.rowCount()
        # print('add_todo',rows)
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            print('column:',column,', field:',field)
            self.model.setData(self.model.index(rows, column+1), field)
        self.model.submitAll()
        self.model.select()
        
    def delete_todo(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
        
    # def clearTodos(self):
    #     self.model.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
    #     self.model.removeRows(0, self.model.rowCount())
    #     self.model.submitAll()
    #     self.model.setEditStrategy(QSqlRelationalTableModel.OnFieldChange)
    #     self.model.select()