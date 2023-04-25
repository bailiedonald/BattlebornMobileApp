import os, random, string
from datetime import datetime
from battlebornmobile import db, login_manager, mail, app
from flask_login import UserMixin
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User Database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    temp_password = db.Column(db.String(60), nullable=True)
    auth_code = db.Column(db.String(60), nullable=True)
    firstName = db.Column(db.String(30), nullable=True)
    lastName = db.Column(db.String(30), nullable=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    streetNumber = db.Column(db.String(50))
    city = db.Column(db.String(25))
    state = db.Column(db.String(15))
    zipcode = db.Column(db.String(5))
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    active = db.Column(db.Boolean, default=False, nullable=False)
    StaffAccess = db.Column(db.Boolean, default=False, nullable=False)
    AdminAccess = db.Column(db.Boolean, default=False, nullable=False)
    pets = db.relationship('Pet', backref= 'owner')
    appointments = db.relationship('Appointment', backref= 'owner')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}','{self.firstName}', '{self.lastName}', '{self.phoneNumber}', '{self.streetNumber}', '{self.city}', '{self.state}', '{self.zipcode}', '{self.image_file}')"
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Pet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(50), nullable=False)
    pet_dob = db.Column(db.String(30), nullable=False)
    pet_species = db.Column(db.String(50), nullable=False)
    pet_breed = db.Column(db.String(50))
    pet_color = db.Column(db.String(50))
    pet_height = db.Column(db.String(100))
    pet_weight = db.Column(db.String(1000))
    pet_pic = db.Column(db.String(255), nullable=False, default='animals.jpeg')
    # Link to Pet Owner in user Database
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # PDF record filename
    pdf_record = db.Column(db.String(255))

    # Add this to the Pet model
    appointments = db.relationship('Appointment', backref='pet', lazy=True)

    def __repr__(self):
        return f"Pet('{self.id}', '{self.pet_name}', '{self.pet_dob}', '{self.pet_species}', '{self.pet_breed}', '{self.pet_color}','{self.pet_height}','{self.pet_weight}')"


class Appointment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=True)
    lastName = db.Column(db.String(30), nullable=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    pet_name = db.Column(db.String(30))
    service =db.Column(db.String(250))
    streetNumber = db.Column(db.String(50))
    city = db.Column(db.String(25))
    state = db.Column(db.String(15))
    zipcode = db.Column(db.String(5))
    weekday = db.Column(db.String(10))
    timeSlot = db.Column(db.String(20))
    dateSheduled = db.Column(db.String(30))
    timeSheduled = db.Column(db.String(20))
    scheduled = db.Column(db.Boolean, default=False, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    cancelled = db.Column(db.Boolean, default=False, nullable=False)
    #Link to Pet Owner in user Database
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    #def convert_to_iso_format(self, date_string, time_string):
        # Convert the date string to a datetime object
     #   date = datetime.strptime(date_string, "%Y-%m-%d")

        # Convert the time string to a datetime object
      #  time = datetime.strptime(time_string, "%H:%M:%S")

        # Combine the date and time objects into a datetime object
       # date_time = datetime.combine(date, time)

        # Convert the datetime object to an ISO-formatted string
        #iso_string = date_time.isoformat()

        #return iso_string
    
    def __repr__(self):
        return f"Pet('{self.id}', '{self.scheduled}', '{self.cancelled}', '{self.owner_id}')"
