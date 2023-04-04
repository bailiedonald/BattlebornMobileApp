from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from twilio.rest import Client
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

#Donny Databsae Setup
app.config['SECRET_KEY'] = 'Super Secret Password'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Add this line to disable track modifications

# local hard code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://battlebornmobile_user:cnaZi2wlEj9GSs8MxWKOuaQWquvhfwD7@dpg-cghhue02qv23kcr6c6a0-a.oregon-postgres.render.com/battlebornmobile'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# postgresql://battlebornmobile_user:cnaZi2wlEj9GSs8MxWKOuaQWquvhfwD7@dpg-cghhue02qv23kcr6c6a0-a.oregon-postgres.render.com/battlebornmobile




app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'
app.config['SECURITY_ROLES'] = {'admin': 'Administrator', 'staff': 'Staff', 'user': 'User'}

#Email verification Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'spencer@alsetdsgd.com'
app.config['MAIL_PASSWORD'] = 'Spring22'


#Davis Push Notifications Setup
# Twilio credentials
account_sid = 'AC003773b4742a681273555f869fe8c6d1'
auth_token = '0b57f20b3db3982301d34480e5af5077'

# Initialize the Twilio client
client = Client(account_sid, auth_token)



db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])



login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from battlebornmobile import views





