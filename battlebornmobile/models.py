from datetime import datetime
from battlebornmobile import db, login_manager
from flask_login import UserMixin
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


roles_users = db.Table('roles_users',
            db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
            db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
            extend_existing=True)



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

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
    active = db.Column(db.Boolean, default=True, nullable=False)
    StaffAccess = db.Column(db.Boolean, default=False, nullable=False)
    AdminAccess = db.Column(db.Boolean, default=False, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    pets = db.relationship('Pet', backref= 'owner')
    appointments = db.relationship('Appointment', backref= 'owner')

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
    pet_pic = db.Column(db.String(20), nullable=False, default='animals.jpeg')
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


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    scheduled = db.Column(db.Boolean, nullable=False)
    cancelled = db.Column(db.Boolean, nullable=False)
    #Link to Pet Owner in user Database
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
# firstName 
# lastName
# email
# phoneNumber
# pet_name
# pet_dob
# pet_species
# pet_breed
# streetNumber
# city
# state
# zipcode

    def __repr__(self):
        return f"Pet('{self.id}', '{self.scheduled}', '{self.cancelled}', '{self.owner_id}')"
