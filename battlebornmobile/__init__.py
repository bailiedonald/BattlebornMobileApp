from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required
from twilio.rest import Client







app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/battleborn'
app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'
app.config['SECURITY_ROLES'] = {'admin': 'Administrator', 'staff': 'Staff', 'user': 'User'}
TWILIO_ACCOUNT_SID='AC003773b4742a681273555f869fe8c6d1'
TWILIO_AUTH_TOKEN='O6406c4546b69b0c05ddd4904ca160eb4'

db = SQLAlchemy(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

    
from battlebornmobile import views


#for testing
def create_app(config_name):
    app = Flask(__name__)
    SECRET_KEY="default_secret_key",
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db',
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
        
    # rest of the function
    # ...

    return app




