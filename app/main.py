
from PySide6.QtWidgets import QApplication
import sys
from .views import MainWindow
from .database import Database
from decouple import config

def main():
    db = Database()
    db.start_connection(config('DB_NAME'))
    app = QApplication(sys.argv)
    window = MainWindow()
    window.init_db(db)
    window.setup_ui()
    # window.switch_stacked_page('authenticated')
  
    window.show()
    sys.exit(app.exec())

