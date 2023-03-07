from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from battlebornmobile.models import User, Pet, Appointment
from flask_login import current_user



class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_email = StringField('Confirm Email', validators=[DataRequired(), Email()])
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
    pet_name = StringField('Pet Name')
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number')
    service = StringField('Service')
    weekday = StringField('Weekday')
    timeSlot = SelectField('Time Slot', choices=[('Morning', 'Afternoon')])
    streetNumber = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Make Appointment')


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
