from flask import render_template, url_for, flash, redirect, request
from battlebornmobile import app, db, bcrypt
from battlebornmobile.forms import SignUpForm, LoginForm, PetForm
from battlebornmobile.models import User, Pet
from flask_login import login_user, current_user, logout_user, login_required


#index Page
@app.route('/')
def index():
    return render_template("index.html")

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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

#Add Pet
@app.route("/pet/add", methods=['GET', 'POST'])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        pet = Pet(pet_name=form.pet_name.data, pet_dob=form.pet_dob.data, pet_species=form.pet_species.data, pet_breed=form.pet_breed.data, pet_color=form.pet_color.data, pet_height=form.pet_height.data, pet_weight=form.pet_weight.data)
        #Clearing the form
        form.pet_name.data = ' '
        form.pet_dob.data = ' '
        form.pet_species.data = ' '
        form.pet_breed.data = ' '
        form.pet_color.data = ' '
        form.pet_height.data = ' '
        form.pet_weight.data = ' '
        
        #Add Pet to Pet Database
        db.session.add(pet)
        db.session.commit()
        flash('Your pet has been added!', 'success')
    return render_template("add_pet.html", form=form)
       
        


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

#Logout Page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


#Appointment Request Page
@app.route("/appointment")
@login_required
def appointment():
    return render_template('appointment.html', title='AppointmentRequest')


#Admin Dashboard
@app.route('/admin/dashboard')
@login_required
def admindashboard():
    admin = current_user.AdminAccess
    if admin == True:
        return render_template("dashboardadmin.html")
    else:
        flash ("Access Denied Admin Only.")
        return render_template("dashboard.html")


#Main Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
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
def scheduler():
    return render_template("scheduler.html", appointmnet_requests = appointmnet_requests)

#Customer List
@app.route('/staff/records')
def records():
    return render_template("records.html")

#Confirm Appointments
@app.route('/staff/appointments')
def confirmappointments():
    return render_template("confirmappointment.html")


