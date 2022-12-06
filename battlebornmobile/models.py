from datetime import datetime
from battlebornmobile import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Customer(db.Model, UserMixin):
    CustomerID = db.Column(db.Integer, primary_key=True)
    CustomerFirstName = db.Column(db.String(30), nullable=False)
    CustomerLastName = db.Column(db.String(30), nullable=False)
    CustomerDOB = db.Column(db.Integer, nullable=False)
    CustomerEmail = db.Column(db.String(120))
    CustomerPhoneNumber = db.Column(db.Integer)

    def __repr__(self):
        return f"Customer('{self.CustomerID}', '{self.CustomerLastName}', '{self.CustomerFirstName}''{self.CustomerDOB}','{self.CustomerEmail}','{self.CustomerPhoneNumber}')"

class CustomerLogin(db.Model, UserMixin):
    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"CustomerLogin('{self.username}', '{self.email}', '{self.image_file}')"


class Staff(db.Model, UserMixin):
    StaffID = db.Column(db.Integer, primary_key=True)
    StaffFirstName = db.Column(db.String(30), nullable=False)
    StaffLastName = db.Column(db.String(30), nullable=False)
    StaffDOB = db.Column(db.Integer, nullable=False)
    StaffEmail = db.Column(db.String(120))
    StaffPhoneNumber = db.Column(db.Integer)

    def __repr__(self):
        return f"Staff('{self.StaffID}', '{self.StaffLastName}', '{self.StaffFirstName}''{self.StaffDOB}','{self.StaffEmail}','{self.StaffPhoneNumber}')"              


class StaffLogin(db.Model, UserMixin):
    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"StaffLogin('{self.username}', '{self.email}', '{self.image_file}')"


class Pet(db.Model, UserMixin):
    PetID = db.Column(db.Integer, primary_key=True)
    PetName = db.Column(db.String(30), nullable=False)
    PetSpecies = db.Column(db.String(20), nullable=False)
    PetBreed = db.Column(db.String(50))
    PetHeight = db.Column(db.Integer)
    PetWeight = db.Column(db.Integer)

    def __repr__(self):
        return f"Pet('{self.PetID}', '{self.PetName}', '{self.PetSpecies}', '{self.PetBreed}','{self.PetHeight}','{self.PetWeight}')"

class Records(db.Model, UserMixin):
    RecordID = db.Column(db.Integer, primary_key=True)
    RecordType = db.Column(db.String(25), nullable=False)
    DateEntered = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Records('{self.RecordID}', '{self.RecordType}', '{self.DateEntered}')"

class Service(db.Model, UserMixin):
    ServiceID = db.Column(db.Integer, primary_key=True)
    ServiceType = db.Column(db.String(25), nullable=False)
    ServiceDatePerformed = db.Column(db.Date, nullable=False)
    ServiceCost = db.Column(db.Money, nullable=False)
    ServicePaymentSatus = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Service('{self.ServiceID}', '{self.ServiceType}', '{self.ServiceDatePerformed}', '{self.ServiceCost}','{self.ServicePaymentSatus}')"


class InsuranceProviders(db.Model, UserMixin):
    InsuranceID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"InsuranceProviders('{self.InsuranceID}', '{self.CompanyName}')"    