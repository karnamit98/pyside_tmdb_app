### PySide6 GUI Application

#### About Me
>Amit Karn 
>Software Developer
>amit.karn98@gmail.com | +977-9816810976
>[Website](https://amitkarn.com.np) | [Linkedin](https://www.linkedin.com/in/amit-karn-69a48b205/)

#### Instructions
>Copy .env.example to .env => cp .env.example .env
 
>Install the requirements => pip install -r requirements.txt 

>Run the driver file => python driver.py


#### Key Features
```
SQlite3 Database
User and Todos table
Basic Authentication (Register and Login)
Browse, search and watch movies througn TMDB API
Youtube WebView
```
#### Requirements.txt
```
autopep8==1.6.0
bcrypt==3.2.2
certifi==2022.6.15
cffi==1.15.0
charset-normalizer==2.0.12
idna==3.3
Pillow==9.1.1
pycodestyle==2.8.0
pycparser==2.21
PySide6==6.3.0
PySide6-Addons==6.3.0
PySide6-Essentials==6.3.0
python-decouple==3.6
requests==2.28.0
shiboken6==6.3.0
toml==0.10.2
urllib3==1.26.9
```


>Executable file made with [cx_Freeze](https://marcelotduarte.github.io/cx_Freeze/)

#### Browse Movie (With Pagination)
![](/doc_images/browseMovie.PNG)
#### Search Movie (Search with any related keyword and pagination)
![](/doc_images/searchMovie.PNG)
#### Watch Movie (In App or open in default browser)
![](/doc_images/watchMovie.PNG)
#### Youtube Web browser View
![](/doc_images/youtube.PNG)

#### User Crud (Add, delete and editable table rows)
![](/doc_images/userCrud.PNG)
#### Todo Crud (Add, delete and editable table rows)
![](/doc_images/todoCrud.PNG)
#### Register Page (With Validations for null, duplicate email, etc)
![](/doc_images/register.PNG)
![](/doc_images/registerValidation.PNG)
#### Login Page (Validations for email exists and correct password(bcrypt hashed))
![](/doc_images/login.PNG)
![](/doc_images/loginValidation.PNG)
##### Login Success
![](/doc_images/loginSuccess.PNG)





