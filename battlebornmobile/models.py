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
    password = db.Column(db.String(60), nullable=False)
    firstName = db.Column(db.String(30), nullable=True)
    lastName = db.Column(db.String(30), nullable=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    streetNumber = db.Column(db.String(50))
    city = db.Column(db.String(25))
    state = db.Column(db.String(15))
    zipcode = db.Column(db.String(5))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    StaffAccess = db.Column(db.Boolean, default=False, nullable=False)
    AdminAccess = db.Column(db.Boolean, default=False, nullable=False)
    pets = db.relationship('Pet', backref= 'owner')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}','{self.firstName}', '{self.lastName}', '{self.phoneNumber}', '{self.streetNumber}', '{self.city}', '{self.state}', '{self.zipcode}', '{self.image_file}')"


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



# class InsuranceProviders(db.Model, UserMixin):
#     InsuranceID = db.Column(db.Integer, primary_key=True)
#     CompanyName = db.Column(db.String(25), nullable=False)

#     def __repr__(self):
#         return f"InsuranceProviders('{self.InsuranceID}', '{self.CompanyName}')"    


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    scheduled = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        return f"Appointment('{self.id}', '{self.scheduled}')"  


