from datetime import datetime
from battlebornmobile import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    CustomerID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    FirstName = db.Column(db.String(30), nullable=True)
    LastName = db.Column(db.String(30), nullable=True)
    DOB = db.Column(db.Integer, nullable=True)
    PhoneNumber = db.Column(db.Integer)
    can_view_records = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self):
        return f"User('{self.CustomerID}','{self.username}', '{self.email}', '{self.image_file}')"


class Pet(db.Model, UserMixin):
    PetID = db.Column(db.Integer, primary_key=True)
    PetName = db.Column(db.String(30), nullable=False)
    PetSpecies = db.Column(db.String(20), nullable=False)
    PetBreed = db.Column(db.String(50))
    PetHeight = db.Column(db.Integer)
    PetWeight = db.Column(db.Integer)

    def __repr__(self):
        return f"Pet('{self.PetID}', '{self.PetName}', '{self.PetSpecies}', '{self.PetBreed}','{self.PetHeight}','{self.PetWeight}')"

# class Records(db.Model, UserMixin):
#     RecordID = db.Column(db.Integer, primary_key=True)
#     RecordType = db.Column(db.String(25), nullable=False)
#     DateEntered = db.Column(db.Date, nullable=False)

#     def __repr__(self):
#         return f"Records('{self.RecordID}', '{self.RecordType}', '{self.DateEntered}')"

# class Service(db.Model, UserMixin):
#     ServiceID = db.Column(db.Integer, primary_key=True)
#     ServiceType = db.Column(db.String(25), nullable=False)
#     ServiceDatePerformed = db.Column(db.Date, nullable=False)
#     ServiceCost = db.Column(db.Integer, nullable=False)
#     ServicePaymentSatus = db.Column(db.Boolean, nullable=False)

#     def __repr__(self):
#         return f"Service('{self.ServiceID}', '{self.ServiceType}', '{self.ServiceDatePerformed}', '{self.ServiceCost}','{self.ServicePaymentSatus}')"


# class InsuranceProviders(db.Model, UserMixin):
#     InsuranceID = db.Column(db.Integer, primary_key=True)
#     CompanyName = db.Column(db.String(25), nullable=False)

#     def __repr__(self):
#         return f"InsuranceProviders('{self.InsuranceID}', '{self.CompanyName}')"    