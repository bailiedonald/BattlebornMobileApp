from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from twilio.rest import Client
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)

#Donny Databsae Setup
app.config['SECRET_KEY'] = 'Super Secret Password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/battleborn'
app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'
app.config['SECURITY_ROLES'] = {'admin': 'Administrator', 'staff': 'Staff', 'user': 'User'}

#Spencer email verification Setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'spencer@alsetdsgd.com'
app.config['MAIL_PASSWORD'] = 'Spring22'


#Davis Push Notifications Setup
TWILIO_ACCOUNT_SID='AC003773b4742a681273555f869fe8c6d1'
TWILIO_AUTH_TOKEN='O6406c4546b69b0c05ddd4904ca160eb4'
# Twilio credentials
account_sid = 'YOUR_ACCOUNT_SID'
auth_token = 'YOUR_AUTH_TOKEN'

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





