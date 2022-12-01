from flask import render_template, url_for, flash, redirect
from battlebornmobile import app
from battlebornmobile.forms import RegistrationForm, LoginForm
from battlebornmobile.models import User

#Home Page
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

#Scheduler
@app.route('/scheduler')
def scheduler():
    return render_template("scheduler.html")
    # , appointmnet_requests = appointmnet_requests)

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

#Registration Page
@app.route("/registration", methods=['GET', 'POST'])
def registstration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('regististration.html', title='Register', form=form)

#Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)