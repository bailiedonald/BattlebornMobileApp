from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField, DateTimeField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from battlebornmobile.models import User, Pet, Appointment
from flask_login import current_user
import random, string



class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    reset_password = StringField('Password Sent in Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')



class PetForm(FlaskForm):
    id = StringField()
    pet_name = StringField("Pet Name", validators=[DataRequired()])
    pet_dob = DateField("Pet Birthday", validators=[DataRequired()])
    pet_species = StringField("Pet Species", validators=[DataRequired()])
    pet_breed = StringField("Pet Breed", validators=[DataRequired()])
    pet_color = StringField("Pet Color", validators=[DataRequired()])
    pet_height = StringField("Pet Hieght")
    pet_weight = StringField("Pet Weight")
    submit = SubmitField('Add Pet')

class AppointmentForm(FlaskForm):
    id = IntegerField('User ID')
    pet_name = SelectField('Pet', coerce=int, validators=[DataRequired()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    service = StringField('Service')
    weekday = StringField('Weekday', validators=[DataRequired()])
    timeSlot = StringField('Time Slot', validators=[DataRequired()])
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Make Appointment')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all pets for the current user
        pets = Pet.query.filter_by(owner_id=current_user.id).all()
        # Create a list of tuples with the pet ID and name
        pet_choices = [(pet.id, pet.pet_name) for pet in pets]
        # Add an option for no pet selected
        pet_choices.insert(0, (0, 'Select a pet'))
        # Set the pet field's choices
        self.pet_name.choices = pet_choices

    def validate_firstName(self, firstName):
        user = User.query.filter_by(firstName=firstName.data).first()
        if not user:
            raise ValidationError('User does not exist.')
    
    def validate_lastName(self, lastName):
        user = User.query.filter_by(lastName=lastName.data).first()
        if not user:
            raise ValidationError('User does not exist.')



class RecordsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])  
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Submit")


class UpdateProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    firstName = StringField("First Name", validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=30)])
    phoneNumber = StringField("Phone Number", validators=[Length(max=20)])
    streetNumber = StringField("Street Number")
    city = StringField("City")
    state = StringField("State")
    zipcode = StringField("Zipcode")
    submit = SubmitField("Update")

class UpdateProfilePictureForm(FlaskForm):
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
