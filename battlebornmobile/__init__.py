from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required
from twilio.rest import Client
import os





app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/battleborn'
app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'
app.config['SECURITY_ROLES'] = {'admin': 'Administrator', 'staff': 'Staff', 'user': 'User'}

db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize the Twilio client with account SID and auth token 
account_sid = os.environ['AC003773b4742a681273555f869fe8c6d1']
auth_token = os.environ['TWILIO6406c4546b69b0c05ddd4904ca160eb4_AUTH_TOKEN']
client = Client(account_sid, auth_token)


from battlebornmobile import views