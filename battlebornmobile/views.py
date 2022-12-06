from flask import render_template, url_for, flash, redirect, request
from battlebornmobile import app, db, bcrypt
from battlebornmobile.forms import SignUpForm, LoginForm, StaffLoginForm
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

#User Profile
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

#Services
@app.route('/services')
def services():
    return render_template("services.html")

#Services
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
        user = CustomerLogin(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

#Customer Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = CustomerLogin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#Logout Page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

#Account Page
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


#Appointment Request Page
@app.route("/appointment")
@login_required
def appointment():
    return render_template('appointment.html', title='AppointmentRequest')


# #Staff Sign Up Page
# @app.route("/staff/signup", methods=['GET', 'POST'])
# def staffsignup():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = StaffSignUpForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = StaffLogin(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('stafflogin'))
#     return render_template('staffsignup.html', title='Sign Up', form=form)

# #Staff Login Page
# @app.route("/staff/login", methods=['GET', 'POST'])
# def stafflogin():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = StaffLoginForm()
#     if form.validate_on_submit():
#         user = StaffLogin.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('staffdashboard'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('stafflogin.html', title='Login', form=form)


#Staff Dashboard
@app.route('/staff/staffdashboard')
def staffdashboard():
    return render_template("staffdashboard.html")

#Scheduler
@app.route('/staff/scheduler')
def scheduler():
    return render_template("scheduler.html")

#Customer List
@app.route('/staff/customerlist')
def customerlist():
    return render_template("customerlist.html")