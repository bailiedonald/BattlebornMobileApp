from datetime import datetime
from battlebornmobile import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    FirstName = db.Column(db.String(30), nullable=True)
    LastName = db.Column(db.String(30), nullable=True)
    PhoneNumber = db.Column(db.Integer, nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    StaffAccess = db.Column(db.Boolean, default=False, nullable=False)
    AdminAccess = db.Column(db.Boolean, default=False, nullable=False)

# User Can Have Many Posts 
	pets = db.relationship('Pets', backref='ownerer')

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}')"


class Pets(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    petname = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=True)
    petspecies = db.Column(db.String(20), nullable=False)
    petbreed = db.Column(db.String(50))
    petheight = db.Column(db.Integer)
    petweight = db.Column(db.Integer)
    Vaccine = db.Column(db.DateTime, default=datetime.utcnow)
# Foreign Key To Link Users (refer to primary key of the user)
    Owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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


class Appointment(db.Model, UserMixin):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Appointment('{self.AppointmentID}', '{self.Status}')"  



# # Create a Blog Post model
# class Posts(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	title = db.Column(db.String(255))
# 	content = db.Column(db.Text)
# 	#author = db.Column(db.String(255))
# 	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
# 	slug = db.Column(db.String(255))
# 	# Foreign Key To Link Users (refer to primary key of the user)
# 	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# # Create Model
# class Users(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(20), nullable=False, unique=True)
# 	name = db.Column(db.String(200), nullable=False)
# 	email = db.Column(db.String(120), nullable=False, unique=True)
# 	favorite_color = db.Column(db.String(120))
# 	about_author = db.Column(db.Text(), nullable=True)
# 	date_added = db.Column(db.DateTime, default=datetime.utcnow)
# 	profile_pic = db.Column(db.String(), nullable=True)

# 	# Do some password stuff!
# 	password_hash = db.Column(db.String(128))
# 	# User Can Have Many Posts 
# 	posts = db.relationship('Posts', backref='poster')


# 	@property
# 	def password(self):
# 		raise AttributeError('password is not a readable attribute!')

# 	@password.setter
# 	def password(self, password):
# 		self.password_hash = generate_password_hash(password)

# 	def verify_password(self, password):
# 		return check_password_hash(self.password_hash, password)

# 	# Create A String
# 	def __repr__(self):
# 		return '<Name %r>' % self.name