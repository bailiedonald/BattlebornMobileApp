from datetime import datetime
from battlebornmobile import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# class Permissons(db.model)
#     id = db.Column(db.Integer, primary_key=True)
#     slug = db.column(db.String(50)
#     description = db.Column(db.String(250))

#     def __repr__(self):
#         return f"Permissons('{self.id}')"  




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    FirstName = db.Column(db.String(30), nullable=True)
    LastName = db.Column(db.String(30), nullable=True)
    PhoneNumber = db.Column(db.Integer)
    Address = db.Column(db.String(250))
    StaffAccess = db.Column(db.Boolean, default=False, nullable=False)
    AdminAccess = db.Column(db.Boolean, default=False, nullable=False)
    pets = db.relationship('Pet', backref= 'owner')


    
    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}')"


class Pet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(30), nullable=False)
    pet_dob = db.Column(db.String(30), nullable=False)
    pet_species = db.Column(db.String(20), nullable=False)
    pet_breed = db.Column(db.String(20))
    pet_color = db.Column(db.String(10))
    pet_height = db.Column(db.String(10))
    pet_weight = db.Column(db.String(10))
    pet_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    #Link to Pet Owner in user Database
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f"Pet('{self.id}', '{self.pet_name}', '{self.pet_dob}', '{self.Ppet_species}', '{self.pet_breed}', '{self.pet_color}','{self.pet_height}','{self.pet_weight}')"

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


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Appointment('{self.AppointmentID}', '{self.Status}')"  


