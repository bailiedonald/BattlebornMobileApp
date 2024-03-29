# Team Memebers Contributiing to this page: 
# Donald Bailie - 
# Davis DeSarle -
# Grant Kite -
# Spencer Carter -

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from twilio.rest import Client
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

#Secret Key Setup
app.config['SECRET_KEY'] = 'Super Secret Password'

#Databse Setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Add this line to disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://battlebornmobile_user:cnaZi2wlEj9GSs8MxWKOuaQWquvhfwD7@dpg-cghhue02qv23kcr6c6a0-a.oregon-postgres.render.com/battlebornmobile'

#Email verification Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '*******'
app.config['MAIL_PASSWORD'] = '*******'
app.config['MAIL_DEFAULT_SENDER'] = ('Battle Born Mobile', '***********S')


#Twilio credentials
Account_Sid = os.environ.get("ACCOUNT_SID")
Auth_Token = os.environ.get("AUTH_TOKEN")
verify_service_id = os.environ.get("TWILIO_VERIFY_SERVICE_ID")
my_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")

#Account_Sid = "your_account_sid"
#Auth_Token = "your_auth_token"
#verify_service_id = "your_verify_service_id"
#my_phone_number = "your_phone_number"


#Initialize the Twilio client
client = Client(Account_Sid, Auth_Token)


db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Login manager loader function
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from battlebornmobile import views



# # For Deploying to Render

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from twilio.rest import Client
# from flask_mail import Mail
# from itsdangerous import URLSafeTimedSerializer
# import os


# app = Flask(__name__)

# #Secret Key Setup
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# #Databse Setup
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Add this line to disable track modifications
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# #Email verification Setup
# app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
# app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
# app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
# app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# # Twilio credentials
# Account_Sid = os.environ.get('Account_Sid')
# Auth_Token = os.environ.get('Auth_Token')
# verify_service_id = os.environ.get("TWILIO_VERIFY_SERVICE_ID")
# my_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")


# # Initialize the Twilio client
# client = Client(Account_Sid, Auth_Token)

# db = SQLAlchemy(app)
# mail = Mail(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# # Login manager loader function
# @login_manager.user_loader
# def load_user(user_id):
#     return users.get(user_id)

# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

# from battlebornmobile import views







