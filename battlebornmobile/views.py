from flask import render_template, url_for, flash, redirect, request
from battlebornmobile import app, db, bcrypt
from battlebornmobile.forms import SignUpForm, LoginForm, PetForm, AppointmentForm
from battlebornmobile.models import User, Pet, Appointment
from flask_login import login_user, current_user, logout_user, login_required
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required
from datetime import datetime
from twilio.rest import Client
from flask_mail import Mail, Message
import secrets
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build



#index Page
@app.route('/')
def index():
    return render_template("index.html",title='Home')

#About Us Page
@app.route('/about')
def about():
    return render_template("about.html")

#Services
@app.route('/services')
def services():
    return render_template("services.html")

#Contact
@app.route('/contact')
def contact():
    return render_template("contact.html")

#Layout
@app.route('/layout')
def layout():
    return render_template("layout.html")

#Sign Up Page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
        db.session.add(user)
        db.session.commit()
        flash('Please check your email to verify your new account')
        return render_template('confirmEmail.html')
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/signup/spencer', methods=['GET', 'POST'])
def signupspencer():
    if request.method == 'POST':
        # Process the user's sign-up information and generate a verification token
        email = request.form['email']
        token = secrets.token_urlsafe(16)

        # Send the verification email to the user's email address
        msg = Message('Verify your email address', sender='spencer@alsetdsgd.com', recipients=[email])
        msg.body = render_template('verification_email.txt', token=token)
        mail.send(msg)

        # Update the user's account information to indicate that the email address is not yet verified
        # You can use a database or other storage mechanism to track this information
        user = {'email': email, 'token': token, 'active': False}

        return render_template('confirmEmail.html'), 'Thank you for signing up! Please check your email to verify your email address.'

    return render_template('signupS.html')

@app.route('/verify/<token>')
def verify(token):
    # Retrieve the user's account information based on the token provided in the link
    # You can use a database or other storage mechanism to retrieve this information
    user = {'email': 'user@example.com', 'token': 'AbCdEf123456', 'active': False}

    # Compare the token in the link to the one generated earlier
    if token == user['token']:
        # Update the user's account information to indicate that the email address is now verified
        user['active'] = True

        return render_template('login.html'), 'Your account has been created! You are now able to log in'

    return 'Invalid verification link.'

#Confirm Email Page
@app.route('/signup/Confirmation')
def confirmemail():
    return render_template("confirmEmail.html")

#signupS Page
@app.route('/signupS')
def signupS():
    return render_template("signupS.html")

#Add Pet Page
@app.route("/pet/add", methods=['GET', 'POST'])
@login_required
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        pet = Pet(pet_name=form.pet_name.data, pet_dob=form.pet_dob.data, pet_species=form.pet_species.data, pet_breed=form.pet_breed.data, pet_color=form.pet_color.data, pet_height=form.pet_height.data, pet_weight=form.pet_weight.data, owner_id=current_user.id)
        # Add Pet to Pet Database
        db.session.add(pet)
        db.session.commit()
        
        flash('Your pet has been added!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_pet.html', form=form)

#Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#Main Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Query all pets linked to the current user
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    # Query all appoinments linked to the current user
    appointments = Appointment.query.filter_by(owner_id=current_user.id).all()

    return render_template("dashboard.html", pets=pets, appointments=appointments)

#Logout Page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

#Appointment Request Page
@app.route("/appointment/request", methods=['GET', 'POST'])
@login_required
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, pet_name=form.pet_name.data, service=form.service.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)

        # Add Pet to Pet Database
        db.session.add(appointment)
        db.session.commit()
        
        flash('Your request has been received!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('appointment_request.html', title='MakeAppointment', form=form)

#Admin Dashboard
@app.route('/admin/dashboard')
@login_required
# @roles_required('admin')
def admindashboard():
    admin = current_user.AdminAccess
    if admin == True:
        return render_template("dashboardadmin.html")
    else:
        flash ("Access Denied Admin Only.")
        return render_template("dashboard.html")


#Staff Dashboard
@app.route('/staff/dashboard')
@login_required
def staffdashboard():
    staff = current_user.StaffAccess
    if staff == True:
        return render_template("dashboardstaff.html")
    else:
        flash ("Access Denied Staff Only.")
        return render_template("dashboard.html")



appointmnet_requests = [
    {
        'customer': 'Hagrid',
        'service': 'Neutering and Vaccines',
        'pet_name': 'Fluffy',
        'date_requested': 'December 20, 2022'
    },
    {
        'customer': 'Harry',
        'service': 'Wings clipped',
        'pet_name': 'Hedwig',
        'date_requested': 'December 15, 2018'
    },
    {
        'customer': 'Ron',
        'service': 'Rabbies Vacine',
        'pet_name': 'Scabbers',
        'date_requested': 'December 17, 2022'
    }

]

#Scheduler
@app.route('/staff/scheduler')
@login_required
def scheduler():
    return render_template("scheduler.html", appointmnet_requests = appointmnet_requests)

#Staff View Customer Records
@app.route('/staff/records', methods={"GET", "POST"})
@login_required
def records():
    users = User.query.all()
    return render_template('records.html', users=users)

#Staff Search Customer Records
@app.route('/staff/records/search')
@login_required
def search():
    search_query = request.args.get('q')
    if search_query:
        users = User.query.filter(User.lastName.contains(search_query)).all()
    else:
        users = User.query.all()
    return render_template('recordsSearch.html', users=users, search_query=search_query)


#Confirm Appointments
@app.route('/staff/appointments')
@login_required
def confirmappointments():
    return render_template("confirmappointment.html")

#Update User Page
@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.email = request.form['email']
        db.session.commit()
        return render_template('dashboard.html', user=user)
    else:
        return render_template('update.html', user=user)

#Calendar Page
@app.route('/calendar')
@login_required
def calendar():
    return render_template("calendar.html")



#SMS Notification Page
@app.route('/sms-notification', methods=['POST'])
def sms_notification():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404
    phone_number = user.phone_number
    message = 'Hello, your appointment has been scheduled.'
    try:
        message = client.messages.create(
            body=message,
            from_='+17752405149',  
            to=phone_number
        )
        return 'Notification sent successfully.'
    except:
        return 'Failed to send notification', 500




#Send SMS Notifcation for Appointment Confirmation
@app.route('/send_notification', methods=['GET', 'POST'])
def send_notification():
    if request.method == 'POST':
        user_id = request.form['user_id']
        # Do something with the user_id, such as send a notification
        return 'Notification sent to user {}'.format(user_id)
    else:
        return render_template('send_notification_form.html')


# Initialize the Twilio client
account_sid = 'your_account_sid_here'
auth_token = 'your_auth_token_here'
client = Client(account_sid, auth_token)

