# Team Memebers Contributiing to this page: 
# Donald Bailie - 
# Davis DeSarle -
# Grant Kite -
# Spencer Carter -

import random, string, os, re
from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField, DateTimeField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from battlebornmobile.models import User, Pet, Appointment
from flask_login import current_user
from sqlalchemy import or_


#SignUpForm
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    auth_code = StringField('auth_code', validators=[Length(max=6)])
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


#AuthCodeForm
class AuthCodeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    auth_code = StringField('Authentication Code', validators=[DataRequired()])
    submit = SubmitField('Submit')


# LoginForm
class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter(or_(User.username == self.username_or_email.data.lower(), User.email == self.username_or_email.data.lower())).first()
        if not user:
            self.username_or_email.errors.append('Invalid username or email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True


#ResetPasswordForm
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    temp_password = PasswordField('Current Password', validators=[validators.DataRequired()])
    new_password = PasswordField('New Password', validators=[validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[validators.DataRequired()])
    submit = SubmitField('Reset Password')


#PetForm
class PetForm(FlaskForm):
    pet_name = StringField("Pet Name", validators=[DataRequired()])
    pet_dob = DateField("Pet Birthday", validators=[DataRequired()])
    pet_species = StringField("Pet Species", validators=[DataRequired()])
    pet_breed = StringField("Pet Breed", validators=[DataRequired()])
    pet_color = StringField("Pet Color", validators=[DataRequired()])
    pet_height = StringField("Pet Height")
    pet_weight = StringField("Pet Weight")
    pet_pic = FileField("Pet Picture", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    pet_record = FileField("Pet Record", validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Add Pet')


#AppointmentForm
class AppointmentForm(FlaskForm):
    id = IntegerField('User ID')
    pet_name = SelectField('Pet', coerce=str, validators=[DataRequired()]) 
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    service = StringField('Service')
    cost = IntegerField('Cost')
    weekday = StringField('Weekday', validators=[DataRequired()])
    timeSlot = StringField('Time Slot', validators=[DataRequired()])
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Request Appointment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all pets for the current user
        pets = Pet.query.filter_by(owner_id=current_user.id).all()
        # Create a list of tuples with the pet name and ID
        pet_choices = [(pet.pet_name, pet.pet_name) for pet in pets]  # Change the list comprehension
        # Add an option for no pet selected
        pet_choices.insert(0, ('', 'Select a pet'))  # Change the ID value to an empty string
        # Set the pet field's choices
        self.pet_name.choices = pet_choices

    def validate_pet_name(self, pet_name):
        pet = Pet.query.filter_by(pet_name=pet_name.data, owner_id=current_user.id).first()
        if not pet:
            raise ValidationError('Pet does not exist.')


#RecordsForm
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


#SearchForm
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


#UpdateProfileForm
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

#GenerateReportsForm
class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    table_name = StringField('Table Name', validators=[DataRequired()])
    columns = StringField('Columns', validators=[DataRequired()])
    filters = StringField('Filters')
    order_by = StringField('Order By')
    submit = SubmitField('Generate Report')


#UpdateProfilePictureForm
class UpdateProfilePictureForm(FlaskForm):
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])


#VerificationCodeInoDayForm
class VerificationCodeInoDayForm(FlaskForm):
    phoneNumber = StringField("Phone Number", validators=[Length(max=20)])


#VerificationCodeActualForm
class VerificationCodeActualForm(FlaskForm):
    phoneNumber = StringField("Phone Number", validators=[Length(max=20)])
    auth_code = StringField('verification-code', validators=[Length(max=6)])