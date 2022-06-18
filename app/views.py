from email.charset import QP
from tkinter import dialog, messagebox
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTabWidget,
    QLabel,
    QComboBox,
    QStackedLayout,
    QTreeView,
    QGridLayout,
)
import webbrowser
from PySide6.QtGui import QIcon, QPixmap
from decouple import config
import bcrypt
import datetime
from app.model import TodoModel, UserModel
from .tmdb import TMDB
from functools import partial
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setup_ui()
        self.resetUserData()
        self.tmdb = TMDB()

    def init_db(self, db):
        self.db = db

    def resetUserData(self):
        self.userData = {"id": 1, "name": "Guest",
                         "email": "guest@example.com", "password": "test"}

    def setup_ui(self):
        """Main window's GUI setup"""
        # my_pixmap = QPixmap(":/naruto.png")
        my_icon = QIcon('naruto.png')
        self.setWindowIcon(my_icon)
        self.setWindowTitle(config('APP_NAME'))
        self.resize(800, 600)
        self.centralWidget = QWidget()
        self.centralWidget.setStyleSheet(
            "QWidget { background-color: black;color:white }")
        self.setCentralWidget(self.centralWidget)
        # self.layout = QVBoxLayout()
        # self.centralWidget.setLayout(self.layout)
        self.centralWidget.setLayout(self.init_stacked_layout())

        # self.layout.addWidget(self.init_user_table(),1)
        # self.layout.addWidget(self.init_btn_reset_db())

    def init_stacked_layout(self):
        # Create and connect the combo box to switch between pages
        # self.pageCombo = QComboBox()
        self.stackedPages = ["login_register", "authenticated"]

        # Create the stacked layout
        self.stackedLayout = QStackedLayout()

        # Create and add Login Register Page Layout
        self.loginRegisterPage = QWidget()
        self.loginRegisterPage.setLayout(self.init_login_register_layout())
        self.stackedLayout.addWidget(self.loginRegisterPage)

        # Create and add CRUD Layout
        self.authenticatedPage = QWidget()
        self.authenticatedPage.setLayout(self.init_authenticated_layout())
        self.stackedLayout.addWidget(self.authenticatedPage)
        return self.stackedLayout

    def switch_stacked_page(self, page):
        # print('stack switch',page)
        index = self.stackedPages.index(page)
        self.stackedLayout.setCurrentIndex(index)

    def init_login_register_layout(self):
        # Create a top-level layout
        tabLayout = QVBoxLayout()
        self.setLayout(tabLayout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.login_tab(), "Login")
        # tabs.setStyleSheet("QTabWidget::pane { background-color: red;color:white;border:1.5px solid black; }")
        tabs.setStyleSheet("""
                           QTabWidget::pane { background-color: red;color:white;border:1.5px solid black;padding:20px 20px; } 
                           QTabBar::tab { background-color: black;color:white; }
                           QTabBar::tab:selected { background-color: black;color:red;border-color:red;font-weight:bold;text-decoration:underline; }
                           """)
        tabs.addTab(self.register_tab(), "Register")
        tabLayout.addWidget(tabs)
        return tabLayout

    def login_tab(self):
        loginTab = QWidget()
        formLayout = QFormLayout()
        loginHeader = QLabel('LOGIN')
        loginHeader.setStyleSheet("""
                                  QLabel{
                                      font-size:30px;
                                     font-weight:bold;
                                      
                                  }
                                  """)
        loginHeader.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(loginHeader)
        self.loginErrorField = QLabel('')
        self.loginErrorField.setStyleSheet("""
                                   QLabel{
                                     color:red
                                   }
                                   """)
        formLayout.addWidget(self.loginErrorField)
        self.loginEmail = QLineEdit()
        self.loginPassword = QLineEdit()
        formLayout.addRow("Email:", self.loginEmail)
        formLayout.addRow("Password:", self.loginPassword)
        self.btnLogin = QPushButton('LOGIN')
        self.btnLogin.clicked.connect(self.action_login)
        self.btnLogin.setStyleSheet("""
                               QPushButton{
                                   background-color:#1089ff;
                                   color:white
                               }
                               QPushButton:hover{
                                   background-color:green;
                               }
                               """)
        formLayout.addWidget(self.btnLogin)
        loginTab.setLayout(formLayout)
        return loginTab

    def register_tab(self):
        registerTab = QWidget()
        formLayout = QFormLayout()
        registerHeader = QLabel('REGISTER')
        registerHeader.setStyleSheet("""
                                  QLabel{
                                      font-size:30px;
                                     font-weight:bold;
                                      
                                  }
                                  """)
        registerHeader.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(registerHeader)
        self.registerErrorField = QLabel('')
        self.registerErrorField.setStyleSheet("""
                                   QLabel{
                                     color:red
                                   }
                                   """)
        formLayout.addWidget(self.registerErrorField)
        self.regName = QLineEdit()
        self.regEmail = QLineEdit()
        self.regPassword = QLineEdit()
        self.regConfirmPassword = QLineEdit()
        formLayout.addRow("Name:", self.regName)
        formLayout.addRow("Email:", self.regEmail)
        formLayout.addRow("Password:", self.regPassword)
        formLayout.addRow("Confirm Password:", self.regConfirmPassword)
        self.btnRegister = QPushButton('Register')
        self.btnRegister.clicked.connect(self.action_register)
        self.btnRegister.setStyleSheet("""
                               QPushButton{
                                   background-color:#1089ff;
                                   color:white
                               }
                               QPushButton:hover{
                                   background-color:green;
                               }
                               """)
        formLayout.addWidget(self.btnRegister)
        registerTab.setLayout(formLayout)
        return registerTab

    def action_login(self):
        email = self.loginEmail.text()
        password = self.loginPassword.text()
        validationErrors = ""
        validationErrors += "Email cannot field be Empty! \n" if email == "" else ''
        validationErrors += "Password cannot field be Empty! \n" if password == "" else ''
        if validationErrors != "":
            self.loginErrorField.setText(validationErrors)
            return False
        # self.loginErrorField.setText('')
        # Attempt login
        res = self.db.attempt_login(email, password)
        if res['status'] == "error":
            self.loginErrorField.setText(res['message'])
            return False
        # LOGIN SUCCESS
        messageBox = QMessageBox.information(None, config(
            "APP_NAME"), f"'{email}' Login In Success! ", QMessageBox.Ok, QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            pass
        self.userData = res['data']
        # print(res['data'])
        self.switch_stacked_page('authenticated')
        self.refreshAuthenticatedLabels()

    def refreshAuthenticatedLabels(self):
        self.welcomeLabel.setText(
            "Welcome, "+self.userData['name']+" ("+self.userData['email']+")")

    def action_register(self):
        name = self.regName.text()
        email = self.regEmail.text()
        password = self.regPassword.text()
        confirmPassword = self.regConfirmPassword.text()
        validationErrors = ""
        validationErrors += "Name cannot field be Empty! \n" if name == "" else ''
        validationErrors += "Email cannot field be Empty! \n" if email == "" else ''
        validationErrors += "Password cannot field be Empty! \n" if password == "" else ''
        validationErrors += "Confirm password field cannot be Empty! \n" if confirmPassword == "" else ''
        validationErrors += "Password and confirm password did not match! \n" if password != confirmPassword else ''
        existing_emails = self.db.get_existing_emails()
        validationErrors += "Email already exists! \n" if email in existing_emails else ''
        if validationErrors != "":
            self.registerErrorField.setText(validationErrors)
            return False
        self.registerErrorField.setText("")
        self.db.create_user([(name, email, password), ])
        QMessageBox.information(None, config(
            "APP_NAME"), f"USER '{email}' created successfully! ",)
        self.userModel.refresh_model()
        self.regName.setText('')
        self.regEmail.setText('')
        self.regPassword.setText('')
        self.regConfirmPassword.setText('')
        return True

    def init_authenticated_layout(self):
        self.authenticatedLayout = QVBoxLayout()
        self.authenticatedLayout.addLayout(self.init_authenticated_header())

        container = QHBoxLayout()
        self.authenticatedStackedPages = ["todos", "users", "movies","watch_movies","youtube"]
        buttons = QVBoxLayout()

        btnTodoLink = QPushButton("Todos")
        btnTodoLink.setStyleSheet(
            """QPushButton{margin-top:20px;padding:0 20px;background-color:#371B58;color:white}QPushButton:hover{background-color:#14C38E}""")
        btnTodoLink.clicked.connect(
            lambda: self.authenticatedStackedLayout.setCurrentIndex(0))
        buttons.addWidget(btnTodoLink)
        btnUsersLink = QPushButton("Users")
        btnUsersLink.setStyleSheet(
            """QPushButton{padding:0 20px;background-color:#371B58;color:white}QPushButton:hover{background-color:#14C38E}""")
        btnUsersLink.clicked.connect(
            lambda: self.authenticatedStackedLayout.setCurrentIndex(1))
        buttons.addWidget(btnUsersLink)
        btnMoviesLink = QPushButton("Movies")
        btnMoviesLink.setStyleSheet(
            """QPushButton{padding:0 20px;background-color:#371B58;color:white}QPushButton:hover{background-color:#14C38E}""")
        btnMoviesLink.clicked.connect(
            lambda: self.authenticatedStackedLayout.setCurrentIndex(2))
        buttons.addWidget(btnMoviesLink)
        self.btnWatchMoviesLink = QPushButton("Watch Movies")
        self.btnWatchMoviesLink.setStyleSheet(
            """QPushButton{padding:0 20px;background-color:#371B58;color:white}QPushButton:hover{background-color:#14C38E}""")
        self.btnWatchMoviesLink.clicked.connect(
            lambda: self.authenticatedStackedLayout.setCurrentIndex(3))
        buttons.addWidget(self.btnWatchMoviesLink) 
        self.btnYoutubeLink = QPushButton("Youtube")
        self.btnYoutubeLink.setStyleSheet(
            """QPushButton{padding:0 20px;background-color:#371B58;color:white}QPushButton:hover{background-color:#14C38E}""")
        self.btnYoutubeLink.clicked.connect(
            lambda: self.authenticatedStackedLayout.setCurrentIndex(4))
        buttons.addWidget(self.btnYoutubeLink)


        buttons.addStretch()
        container.addLayout(buttons)

        # Create the stacked layout
        self.authenticatedStackedLayout = QStackedLayout()
        # todos table tree view
        self.todosPage = QWidget()
        self.todosPage.setLayout(self.init_todo_page_layout())
        self.authenticatedStackedLayout.addWidget(self.todosPage)
        # User table view
        self.usersPage = QWidget()
        self.usersPage.setLayout(self.init_user_page_layout())
        self.authenticatedStackedLayout.addWidget(self.usersPage)
        # Movies view
        self.moviesPage = QWidget()
        self.moviesPage.setLayout(self.init_movie_page_layout())
        self.authenticatedStackedLayout.addWidget(self.moviesPage)
        # Watch Movies view
        self.watchMoviesPage = QWidget()
        self.watchMoviesPage.setLayout(self.init_watch_movie_page_layout())
        self.authenticatedStackedLayout.addWidget(self.watchMoviesPage)
        # Youtube view
        self.youtubePage = QWidget()
        self.youtubePage.setLayout(self.init_youtube_page_layout())
        self.authenticatedStackedLayout.addWidget(self.youtubePage)
        container.addLayout(self.authenticatedStackedLayout)
        
        # return self.authenticatedStackedLayout
        self.authenticatedLayout.addLayout(container)
        return self.authenticatedLayout

        # self.authenticatedLayout.addLayout(self.init_user_page_layout())
        # return self.authenticatedLayout
    def init_watch_movie_page_layout(self,):
        # self.watchMovieLayout = QVBoxLayout()
        self.watchMoviePage = QWidget()
        # self.movieTab.setStyleSheet("QTabWidget::pane { background-color: red;color:white;border:1.5px solid black; }")
        self.watchMoviePage.setStyleSheet("""
                           QWidget: { background-color: #655D8A;color:white;border:1.5px solid black;padding:20px 20px; } 
                            """)
        vBox = QVBoxLayout()
        hBox = QHBoxLayout()
        
        self.watchMovieTitle = QLabel('Movie Title')
        self.watchMovieTitle.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow;padding:2px}")
        hBox.addWidget(self.watchMovieTitle,1)
        
        self.btnWatchInBrowser = QPushButton('Open In Browser')
        self.btnWatchInBrowser.setStyleSheet("QPushButton{background:#57CC99}QPushButton:hover{background:#3E00FF}")
        self.watchMovieUrl = ""
        self.btnWatchInBrowser.clicked.connect( self.open_browser )
        hBox.addWidget(self.btnWatchInBrowser)
        
        vBox.addLayout(hBox)
        self.watchMovieWidget = QWebEngineView()
        # self.watchMovieWidget.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        # self.watchMovieWidget.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # self.watchMovieWidget.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        # self.watchMovieWidget.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        # self.watchMovieWidget.settings().setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)
        # self.watchMovieWidget.settings().setUnknownUrlSchemePolicy(QWebEngineSettings.AllowAllUnknownUrlSchemes)
        self.watchMovieWidget.setStyleSheet("QWebEngineView{background:#3E2C41}")
        vBox.addWidget(self.watchMovieWidget,1)
        
        return vBox
    
    def open_browser(self):
        url =  self.watchMovieUrl
        webbrowser.open(url=url)
    
    def init_youtube_page_layout(self):
        # self.watchMoviePage = QWidget()
        # # self.movieTab.setStyleSheet("QTabWidget::pane { background-color: red;color:white;border:1.5px solid black; }")
        # self.watchMoviePage.setStyleSheet("""
        #                    QWidget: { background-color: #655D8A;color:white;border:1.5px solid black;padding:20px 20px; } 
        #                     """)
        vBox = QVBoxLayout()
        self.youtubeTitle = QLabel('Youtube')
        self.youtubeTitle.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow;padding:2px}")
        vBox.addWidget(self.youtubeTitle)
        self.youtubeWidget = QWebEngineView()
        self.youtubeWidget.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        self.youtubeWidget.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.youtubeWidget.page().fullScreenRequested.connect(lambda request: request.accept())
        self.youtubeWidget.load(QUrl("https://www.youtube.com/"))
        self.youtubeWidget.setStyleSheet("QWebEngineView{background:#3E2C41}")
        vBox.addWidget(self.youtubeWidget,1)
        
        return vBox
        

    def init_movie_page_layout(self):
        #MOVIE PAGE
        self.moviePageLayout = QVBoxLayout()
        
        lb = QLabel("MOVIES")
        lb.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow;background:#413F42;padding:2px}")
        self.moviePageLayout.addWidget(lb)

        self.movieTab = QTabWidget()
        self.movieTab.addTab(self.movie_list_tab(), "Browse")
        # self.movieTab.setStyleSheet("QTabWidget::pane { background-color: red;color:white;border:1.5px solid black; }")
        self.movieTab.setStyleSheet("""
                           QTabWidget::pane { background-color: #655D8A;color:white;border:1.5px solid black;padding:20px 20px; } 
                           QTabBar::tab { background-color: black;color:white; }
                           QTabBar::tab:selected { background-color: black;color:red;border-color:red;font-weight:bold;text-decoration:underline; }
                           """)
        self.movieTab.addTab(self.movie_search_tab(), "Search")
        self.moviePageLayout.addWidget(self.movieTab)

        return self.moviePageLayout
    
    def movie_list_tab(self):
        self.browseMovieWidget = QWidget()
        vBox = QVBoxLayout()
        lb = QLabel('Popular Movies')
        lb.setStyleSheet("QLabel{margin-left:5px;font-size:20px;font-weight:bold;color:#85F4FF}")
        vBox.addWidget(lb)
        # vBox.addStretch()
        movies = self.tmdb.fetch_popular_movies()
        if movies['status'] == 200:
            hBox = QHBoxLayout()
            self.browseMovies = movies
            # str(movies['data']['total_pages'])
            txt = "Showing "+str(len(movies['data']['results']))+" movies! Page "+str(movies['data']['page'])+" of 500 pages!"
            self.browseMovieInfoHeader = QLabel(txt)
            self.browseMovieInfoHeader.setStyleSheet("QLabel{margin-left:6px;color:#ECB365}")
            hBox.addWidget(self.browseMovieInfoHeader,1)
            hBox.addStretch()
           
            btnChangePage = QPushButton("Go To")
            btnChangePage.setStyleSheet("QPushButton{background:#516BEB;color:white;padding:5px}")
            btnChangePage.clicked.connect(self.change_browse_movie_page)
            self.pageInput = QLineEdit()
            self.pageInput.setPlaceholderText(" Page ")
            self.pageInput.setStyleSheet("QLineEdit{background:#FFF9F9;color:black;padding:3px}")
            hBox.addWidget(btnChangePage)
            hBox.addWidget(self.pageInput)
            vBox.addLayout(hBox)
            self.browseMovieGridContainer = QWidget()
            self.browseMovieGridContainer.setLayout(self.browse_movie_grid(movies['data']['results']))
            vBox.addWidget(self.browseMovieGridContainer,1)
        else:
            vBox.addWidget(QLabel("Failed to fetch Movies!"))
        self.browseMovieWidget.setLayout(vBox)
        return self.browseMovieWidget
    
    def change_browse_movie_page(self):
        page = self.pageInput.text()
        try:
            page = int(page)
            # maxPage = int(self.browseMovies['data']['total_pages'])
            if page<1: # or page>500:
                QMessageBox.critical(self, "Input Error", "Invalid Page Provided!")
                return False
            # print(page, maxPage, "fetching ..")
            self.browseMovies = movies = self.tmdb.fetch_popular_movies(page)
            txt = "Showing "+str(len(movies['data']['results']))+" of 10,000 movies! Page "+str(movies['data']['page'])+" of 500 pages!"
            self.browseMovieInfoHeader.setText(txt)
            totalMovies = len(self.browseMovies['data']['results'])
            i=0
            """
            for i in range(self.browseMovieGrid.count()):
                if i >= totalMovies:
                    break
                movie = self.browseMovies['data']['results'][i]
                card = self.browseMovieGrid.itemAt(i)
                # print(card, card.widget().layout() )
                try:
                    for j in range(card.widget().layout().count()):
                        item = card.widget().layout().itemAt(j).widget()
                        if type(item) == QLabel:
                            # print(item.text(),item.accessibleName())
                            if item.accessibleName() == "title":
                                item.setText(movie['title']  if 'title' in movie else '-')
                            if item.accessibleName() == "release_date":
                                item.setText(f"Release: {movie['release_date'] if 'release_date' in movie else ' - '}")
                            if item.accessibleName() == "rate":
                                item.setText(f"Rating: {movie['vote_average'] if 'vote_average' in movie else '-'}/10 ({movie['vote_count'] if 'vote_count' in movie else '-'})")
                except Exception as ex:
                    print('Failed to update movies!')  
            """
            if self.browseMovieGrid.count() > 0:
                for i in reversed(range(self.browseMovieGrid.count())):
                    # print('i: ',i)
                    self.browseMovieGrid.itemAt(i).widget().setParent(None)
            self.init_movie_grid(self.browseMovieGrid,movies['data']['results'])  
               
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Input Error", f"Invalid Format for Page Number or page does not exist!")
    
    def browse_movie_grid(self,data):
        self.browseMovieGrid = QGridLayout()  
    
        self.init_movie_grid(self.browseMovieGrid,data)
        return self.browseMovieGrid
    
    def init_movie_grid(self,grid,data):
        num_data = len(data)
        cols = 4 if num_data % 2==0 else 3
        rows = num_data // cols 
        # print(rows, cols)
        positions = [(i, j) for i in range(rows) for j in range(cols)]
        for position,movie in zip(positions, data):
            # print(position, movie['title'])
            card = QWidget()
            # border:1px solid #FFAB4C;
            # url("+self.tmdb.get_backdrop_path_url(movie['backdrop_path'])+")
            card.setStyleSheet("""
                               QWidget{border:1px solid #FFAB4C;padding:1px;}
                               QLabel{border:0}
                               """)
            
            # pm = QPixmap(self.tmdb.get_backdrop_path_url(movie['backdrop_path']))
            
            box = QVBoxLayout()
            title = QLabel(movie['title']  if 'title' in movie else '-')
            # title.setPixmap(pm)
            title.setStyleSheet("QLabel{margin:0px;font-size:15px;color:#69DADB;font-weight:bold}")
            title.setAccessibleName("title")
            box.addWidget(title)
            
            hb = QHBoxLayout()
            vb = QVBoxLayout()
            
            release_date = QLabel(f"Release: {movie['release_date'] if 'release_date' in movie else ' - '}")
            release_date.setStyleSheet("QLabel{margin:0px;font-size:10px;color:#EEEBDD}")
            release_date.setAccessibleName("release_date")
            rate = QLabel(f"Rating: {movie['vote_average'] if 'vote_average' in movie else '-'}/10 ({movie['vote_count'] if 'vote_count' in movie else '-'})")
            rate.setStyleSheet("QLabel{margin:0px;font-size:10px;color:#C8E3D4}")
            rate.setAccessibleName("rate")
            vb.addWidget(release_date)
            vb.addWidget(rate)
            hb.addLayout(vb)
            
            btnWatch = QPushButton("Watch")
            btnWatch.setStyleSheet("QPushButton{background:#368B85;color:white;padding:2px;padding:3px}QPushButton:hover{background:#000;}")
            # btnWatch.clicked.connect(lambda:self.watch_movie(movie['id']))
            # btnWatch.clicked.connect(lambda _,b=movie['id']: self.watch_movie(movieId=b))
            btnWatch.clicked.connect(partial(self.watch_movie, movie['id'], movie['title']))
            hb.addWidget(btnWatch)
            
            # box.addWidget(release_date)
            # box.addWidget(rate)
            box.addLayout(hb)
            
            card.setLayout(box)
            grid.addWidget(card,*position)
            
    def watch_movie(self,movieId,movieTitle="Movie Title"):
        self.watchMovieUrl = self.tmdb.get_stream_url(movieId=movieId)
        print("WATCHING MOVIE ID:", self.watchMovieUrl)
        self.watchMovieTitle.setText(f"Watch Movie: {movieTitle}")
        self.watchMovieWidget.load(QUrl( self.watchMovieUrl))
        self.btnWatchMoviesLink.click()
        # self.watchBrowser = WatchMovieDialog(self)
        # print(self.tmdb.get_stream_url(movieId=movieId))
        # self.watchBrowser.load(self.tmdb.get_stream_url(movieId=movieId))
        # self.watchBrowser.exec()
          
    def delete_grid_widget(self, grid, index):
        item = grid.itemAt(index)
        if item is not None:
            widget = item.widget()
            if widget is not None:
                grid.removeWidget(widget)
                widget.deleteLater()
    
    def movie_search_tab(self):
        self.searchMovieWidget = QWidget()
        vBox = QVBoxLayout()
        
        lb = QLabel('Search Movies')
        lb.setStyleSheet("QLabel{margin-left:5px;font-size:20px;font-weight:bold;color:#85F4FF}")
        
        hInnerBox1 = QHBoxLayout()
        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Movie Title, Keyword,...")
        self.searchInput.setStyleSheet("QLineEdit{padding:3px 5px;background:white;color:black}")
        self.btnSearchMovie = QPushButton("Search Movie")
        self.btnSearchMovie.setStyleSheet("QPushButton{background-color:#2EB086;padding:5px}")
        self.btnSearchMovie.clicked.connect(lambda:self.search_movie(True))
        hInnerBox1.addWidget(self.searchInput,1)
        hInnerBox1.addWidget(self.btnSearchMovie)
        
        vBox.addWidget(lb)
        vBox.addLayout(hInnerBox1)
        
        self.searchHeader = QLabel(f'Search results for "{self.searchInput.text()}" !')
        self.searchHeader.setStyleSheet("QLabel{margin-left:6px;color:#ECB365}")
        vBox.addWidget(self.searchHeader)
        
        hBox = QHBoxLayout()
        self.searchMovieInfoHeader = QLabel("")
        self.searchMovieInfoHeader.setStyleSheet("QLabel{margin-left:6px;color:#ECB365}")
        hBox.addWidget(self.searchMovieInfoHeader,1)
        hBox.addStretch()
        
        btnChangePage = QPushButton("Go To")
        btnChangePage.setStyleSheet("QPushButton{background:#516BEB;color:white;padding:5px}")
        btnChangePage.clicked.connect(lambda:self.search_movie(False))
        self.pageInputSearch = QLineEdit()
        self.pageInputSearch.setPlaceholderText(" Page ")
        self.pageInputSearch.setStyleSheet("QLineEdit{background:#FFF9F9;color:black;padding:3px}")
        hBox.addWidget(btnChangePage)
        hBox.addWidget(self.pageInputSearch)
        vBox.addLayout(hBox)
        self.searchMovieGridContainer = QWidget()
        self.searchMovieGridContainer.setLayout(self.search_movie_grid({}))
        vBox.addWidget(self.searchMovieGridContainer,1)
        
        self.searchMovieWidget.setLayout(vBox)
        return self.searchMovieWidget
    
    def search_movie(self,search=False):
         # vBox.addStretch()
        keyword = self.searchInput.text()
        page = self.pageInputSearch.text() if not search else 1
        self.searchHeader.setText(f'Search results for "{keyword}" !')
        try:
            page = int(page)
            if page<1:
                QMessageBox.critical(self, "Input Error", "Invalid Page Provided!")
                return False
            # print(page, maxPage, "fetching ..")
            self.searchMovies = movies = self.tmdb.search_movies(keyword,page)
            txt = f"Showing {len(movies['data']['results'])} of {movies['data']['total_results']} movies! Page {movies['data']['page']} of {movies['data']['total_pages']} pages!"
            self.searchMovieInfoHeader.setText(txt)
            totalMovies = len(self.searchMovies['data']['results'])
            if self.searchMovieGrid.count() > 0:
                for i in reversed(range(self.searchMovieGrid.count())):
                    # print('i: ',i)
                    self.searchMovieGrid.itemAt(i).widget().setParent(None)
            self.init_movie_grid(self.searchMovieGrid,movies['data']['results'])
            """
            if i >= totalMovies:
                break
            movie = self.browseMovies['data']['results'][i]
            card = self.searchMovieGrid.itemAt(i)
            # print(card, card.widget().layout() )
            try:
                for j in range(card.widget().layout().count()):
                    item = card.widget().layout().itemAt(j).widget()
                    if type(item) == QLabel:
                        # print(item.text(),item.accessibleName())
                        if item.accessibleName() == "title":
                            item.setText(movie['title'])
                        if item.accessibleName() == "release_date":
                            item.setText(movie['release_date'])
                        if item.accessibleName() == "rate":
                            item.setText(str(movie['vote_average'])+"/10 ("+str(movie['vote_count'])+")")
            except Exception as ex:
                print('Failed to update movies!')  
            """   
        except Exception as ex:
            # print(ex)
            message = f"Invalid Format for Page Number! {ex}" if not search else f"Search Failed! {ex} "
            QMessageBox.critical(self, "Input Error", message)
     
    def search_movie_grid(self,data):
        self.searchMovieGrid = QGridLayout()  
        
        
        # self.searchMovieGrid.addWidget(QLabel("SEARCH"))
        return self.searchMovieGrid
   
    def init_todo_page_layout(self):
        # Todo Crud Layout
        self.btnAddTodo = QPushButton("Add Todo")
        self.btnAddTodo.setStyleSheet(
            "QPushButton{background-color:green;color:white;font-weight:bold}QPushButton:hover{background-color:blue}")
        self.btnAddTodo.clicked.connect(self.add_todo_form)
        self.btnDeleteTodo = QPushButton("Delete")
        self.btnDeleteTodo.setStyleSheet(
            "QPushButton{background-color:red;color:white;font-weight:bold}QPushButton:hover{background-color:blue}")
        self.btnDeleteTodo.clicked.connect(self.delete_todo)
        # self.clearAllButton = QPushButton("Clear All")
        todoCrudLayout = QHBoxLayout()
        todoCrudLayout.addWidget(self.btnAddTodo)
        # btn = QPushButton('test')
        # todoCrudLayout.addWidget(btn)
        # btn.clicked.connect(lambda:print(self.userData))
        todoCrudLayout.addStretch()
        todoCrudLayout.addWidget(self.btnDeleteTodo)
        self.todoPageLayout = QVBoxLayout()
        lb = QLabel("TODOS")
        lb.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow;background:#413F42;padding:2px}")
        self.todoPageLayout.addWidget(lb)
        self.todoPageLayout.addWidget(self.init_todo_view(), 1)
        self.todoPageLayout.addLayout(todoCrudLayout)
        return self.todoPageLayout

    def init_user_page_layout(self):
        # User Crud Layout
        self.btnAddUser = QPushButton("Add User")
        self.btnAddUser.setStyleSheet(
            "QPushButton{background-color:green;color:white;font-weight:bold}QPushButton:hover{background-color:blue}")
        self.btnAddUser.clicked.connect(self.add_user_form)
        self.btnDeleteUser = QPushButton("Delete")
        self.btnDeleteUser.setStyleSheet(
            "QPushButton{background-color:red;color:white;font-weight:bold}QPushButton:hover{background-color:blue}")
        self.btnDeleteUser.clicked.connect(self.delete_user)
        # self.clearAllButton = QPushButton("Clear All")
        userCrudLayout = QHBoxLayout()
        userCrudLayout.addWidget(self.btnAddUser)
        userCrudLayout.addStretch()
        userCrudLayout.addWidget(self.btnDeleteUser)
        # userCrudLayout.addWidget(self.clearAllButton)
        self.userTableLayout = QVBoxLayout()
        # self.userTableLayout.addWidget(self.init_btn_reset_db())
        lb = QLabel("USERS")
        lb.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow;background:#413F42;padding:2px}")
        self.userTableLayout.addWidget(lb)
        self.userTableLayout.addWidget(self.init_user_table(), 1)
        self.userTableLayout.addLayout(userCrudLayout)
        return self.userTableLayout

    def add_user_form(self):
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.userModel.add_user(dialog.data)
            # self.userTable.resizeColumnsToContents()

    def delete_user(self):
        row = self.userTable.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Are you sure to delete the selected user?",
            QMessageBox.Ok, QMessageBox.Cancel
        )
        if messageBox == QMessageBox.Ok:
            self.userModel.delete_user(row)
            if not self.db.check_user_exists(self.userData['id']):
                QMessageBox.critical(
                    self, "Authentication Failed!", "You have been deleted from the system!")
                self.resetUserData()
                self.stackedLayout.setCurrentIndex(
                    self.stackedPages.index("login_register"))

    def add_todo_form(self):
        dialog = AddTodoDialog(self)
        dialog.setCurrentUser(self.userData)
        if dialog.exec() == QDialog.Accepted:
            self.todoModel.add_todo(dialog.data)
            # self.todoTreeView.resizeColumnToContents()

    def delete_todo(self):
        row = self.todoTreeView.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Are you sure to delete the selected todo?",
            QMessageBox.Ok, QMessageBox.Cancel
        )
        if messageBox == QMessageBox.Ok:
            self.todoModel.delete_todo(row)

    def init_user_table(self):
        """Create the table view widget"""
        self.userModel = UserModel()
        self.userTable = QTreeView()
        self.userTable.setAlternatingRowColors(True)
        self.userTable.setStyleSheet("""QTreeView {padding:2px;alternate-background-color: #4D77FF;background-color:#1B1A17;border:3px solid white; }
                                     QHeaderView::section{alternate-background-color: yellow;background-color:#4D4C7D; border-radius:14px;}
                                     QHeaderView{padding-left:20px;background-color:#4D4C7D}
                                     QTreeView::item {alternate-background-color: #4D77FF;padding:2px;background:#000}
                                     QTreeView::selected {background:#019267;color:white}
                                     """)
        self.userTable.setModel(self.userModel.model)
        # self.userTable.hideColumn(0)  #Hide ID column
        self.userTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.userTable.setSelectionMode(QAbstractItemView.ExtendedSelection)
        return self.userTable

    def init_authenticated_header(self):
        header = QHBoxLayout()
        self.welcomeLabel = QLabel(
            "Welcome, "+self.userData['name']+" ("+self.userData['email']+")")
        self.welcomeLabel.setStyleSheet(
            "QLabel{font-weight:bold;color:yellow}")
        header.addWidget(self.welcomeLabel, 1)
        self.btnLogout = QPushButton("LOG OUT")
        self.btnLogout.setStyleSheet("""QPushButton {background-color:red;color:white;font-weight:bold;} 
                                     QPushButton:hover{background-color:#1089ff;} """)
        self.btnLogout.clicked.connect(lambda: self.stackedLayout.setCurrentIndex(
            self.stackedPages.index("login_register")))
        header.addWidget(self.btnLogout)
        return header

    def init_todo_view(self):
        self.todoModel = TodoModel()
        self.todoTreeView = QTreeView()
        self.todoTreeView.setStyleSheet("""QTreeView {padding:2px;alternate-background-color: #4D77FF;background-color:#1B1A17;border:3px solid white; }
                                     QHeaderView::section{alternate-background-color: yellow;background-color:#4D4C7D; border-radius:14px;}
                                     QHeaderView{padding-left:20px;background-color:#4D4C7D}
                                     QTreeView::item {alternate-background-color: #4D77FF;padding:2px 12px;background:#000}
                                     QTreeView::selected {background:#019267;color:white}
                                     """)
        self.todoTreeView.setModel(self.todoModel.model)
        self.todoTreeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.todoTreeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        return self.todoTreeView

    def init_btn_reset_db(self):
        self.btnResetDb = QPushButton()
        self.btnResetDb.setText("Reset Database")
        self.btnResetDb.clicked.connect(self.action_reset_db)
        return self.btnResetDb

    def action_reset_db(self):
        self.db.seed_user()
        self.userModel.refresh_model()
        # self.userModel.model.select()


class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add new user")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setup_ui()

    def setup_ui(self):
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        self.passwordField = QLineEdit()
        self.passwordField.setObjectName("Password")
        # self.confirmPasswordField = QLineEdit()
        # self.confirmPasswordField.setObjectName("Confirm Password")

        layout = QFormLayout()
        layout.addRow("Name: ", self.nameField)
        layout.addRow("Email: ", self.emailField)
        layout.addRow("Password: ", self.passwordField)
        # layout.addRow("Confirm Password: ",self.confirmPasswordField)

        self.layout.addLayout(layout)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        self.data = []
        for field in (self.nameField, self.emailField, self.passwordField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Validation Error",
                    f"{field.objectName()} cannot be empty!"
                )
                self.data = None
                return
            self.data.append(field.text())

        if not self.data:
            return
        super().accept()


class AddTodoDialog(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add new todo")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setup_ui()

    def setCurrentUser(self, data):
        self.userData = data

    def setup_ui(self):
        self.titleField = QLineEdit()
        self.titleField.setObjectName("Title")
        self.descriptionField = QLineEdit()
        self.descriptionField.setObjectName("Description")

        layout = QFormLayout()
        layout.addRow("Title: ", self.titleField)
        layout.addRow("Description: ", self.descriptionField)

        self.layout.addLayout(layout)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        self.data = []
        for field in (self.titleField, self.descriptionField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Validation Error",
                    f"{field.objectName()} cannot be empty!"
                )
                self.data = None
                return
            self.data.append(field.text())
        self.data.insert(0, self.userData['id'])
        self.data.append('pending')
        self.data.append(str(datetime.datetime.now()))
        # print(self.data)
        # return
        if not self.data:
            return
        super().accept()


class WatchMovieDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Watch Movie")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)
        
    def load(self,url):
        self.browser.load(QUrl(url))