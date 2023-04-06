from flask import render_template, url_for, flash, redirect, request
from battlebornmobile import app, db, bcrypt, mail, client
from battlebornmobile.forms import SignUpForm, LoginForm, PetForm, AppointmentForm, ResetPasswordForm
from battlebornmobile.models import User, Pet, Appointment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
import random, string

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

#SignUp Page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():

        # Update the user's account information to indicate that the email address is not yet verified
        # You can use a database or other storage mechanism to track this information
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
        db.session.add(user)
        db.session.commit()

        flash('Please check your email to verify your new account')
        return render_template('confirmEmail.html')

    return render_template('signup.html', title='Sign Up', form=form)

#Verify Email Page
@app.route('/verify_email/<string:username>', methods=['GET'])
def verify_email(username):
    user = User.query.filter_by(username=username).first_or_404()
    user.active = True
    db.session.commit()
    flash('Your email has been confirmed! You can now login.', 'success')
    return redirect(url_for('login'))
    # if form.validate_on_submit():
    #     # Process the user's sign-up information and generate a verification token
    #     email = form.email.data
    #     username = form.username.data

    #     # Send the verification email to the user's email address
    #     msg = Message('Verify your email address', sender='spencer@alsetdsgd.com', recipients=[email])
    #     msg.body = render_template('verification_email.txt', username=form.username.data)
    #     mail.send(msg)

    #     # Update the user's account information to indicate that the email address is not yet verified
    #     # You can use a database or other storage mechanism to track this information
    #     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user = User(username=form.username.data, email=email, password=hashed_password, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
    #     db.session.add(user)
    #     db.session.commit()

    #     flash('Please check your email to verify your new account')
    #     return render_template('confirmEmail.html')

    # return render_template('signup.html', title='Sign Up', form=form)


#Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
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


#Forgot password
@app.route('/password/forgot', methods=['GET', 'POST'])
def password_forgot():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # generate a new password and update user's password
            new_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
            user.password = new_password
            db.session.commit()

            # send email with password reset instructions
            token = user.get_reset_token()
            msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
{url_for('password_change', token=token, _external=True)}

Your new temporary password is: {new_password}

If you did not make this request then simply ignore this email and no changes will be made.
'''
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('There is no account with that email. You must register first.', 'warning')
    return render_template('password_forgot.html')

#Change password 
@app.route('/password/change', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.current_password.data):
            user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('The current password is incorrect.', 'danger')
    else:
        flash('The form was not valid.', 'danger')
        print(form.errors)

    return render_template('reset_password.html', title='Reset Password', form=form)


#Main Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Query all pets linked to the current user
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    # Query all appoinments linked to the current user
    appointments = Appointment.query.filter_by(owner_id=current_user.id).filter_by(cancelled=False).all()

    return render_template("dashboard.html", pets=pets, appointments=appointments)


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

#Appointment Request Page
@app.route("/appointment/request", methods=['GET', 'POST'])
@login_required
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(owner_id=current_user.id, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, pet_name=form.pet_name.data, service=form.service.data,  weekday=form.weekday.data, timeSlot=form.timeSlot.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)

        # Add Appointment to the Appointment Database
        db.session.add(appointment)
        db.session.commit()
        
        flash('Your request has been received!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('appointment_request.html', title='MakeAppointment', form=form)

#Appointment Edit Page
@app.route("/appointment/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    form = AppointmentForm(obj=appointment)

    if form.validate_on_submit():
        # Update the appointment with the form data
        appointment.pet_name = form.pet_name.data
        appointment.service = form.service.data
        appointment.weekday = form.weekday.data
        appointment.timeSlot=form.timeSlot.data
        db.session.commit()

        flash("Appointment updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("appointment_edit.html", form=form)


#Appointment Cancel Route
@app.route("/appointment/cancel/<int:id>", methods=["GET", "POST"])
@login_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    # Check if the user is the owner of the appointment
    if appointment.owner != current_user:
        flash("You don't have permission to cancel this appointment", "danger")
        return redirect(url_for("dashboard"))

    form = AppointmentForm(obj=appointment)

    if form.validate_on_submit():
        # Update the appointment with the form data
        appointment.cancelled = True

        db.session.commit()

        flash("Appointment cancelled successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("appointment_cancel.html", appointment=appointment, form=form)


# All Unscheduled Appointments
@app.route('/appointments/unscheduled')
@login_required
def unscheduled_appointments():
    appointments = Appointment.query.filter_by(scheduled=False).all()
    return render_template('appointment_unscheduled.html', appointments=appointments)


# Schedule Each Appointment
@app.route('/appointments/schedule/<int:id>', methods=['POST'])
@login_required
def schedule_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.scheduled = True
    appointment.dateScheduled = request.form.get('dateScheduled')
    appointment.timeScheduled = request.form.get('timeScheduled')
    
    #Update An Appointment in the Appointment Database
    db.session.add(appointment)
    db.session.commit()
    flash('Appointment scheduled successfully!', 'success')
    return redirect(url_for('scheduler'))

#Confirm appointment
@app.route('/appointment/confirm')
# @login_required
def confirm_appointment():
    return render_template("appointment_confirm.html")

#All Appointments
@app.route('/appointments')
# @login_required
def appointments():
    return render_template("appointments.html")

#Scheduler
@app.route('/staff/scheduler')
@login_required
def scheduler():
    appointments = Appointment.query.filter_by(scheduled=False).all()

    return render_template("scheduler.html", appointments=appointments)

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

#Admin User Access Table
@app.route('/admin/useraccess')
@login_required
def userAccess():
    admin = current_user.AdminAccess
    if admin:
        search_query = request.args.get('q')
        if search_query:
            users = User.query.filter(User.lastName.contains(search_query)).all()
        else:
            users = User.query.all()
        return render_template('userAccess.html', users=users, search_query=search_query)
    else:
        flash("Access Denied: Admin Only")
        return render_template("dashboard.html")

#Admin Edit User Access Table
@app.route('/admin/useraccess/<int:user_id>', methods=['POST'])
@login_required
def updateAccess(user_id):
    admin = current_user.AdminAccess
    if admin == True:
        user = User.query.get_or_404(user_id)
        user.active = bool(request.form.get('active'))
        user.StaffAccess = bool(request.form.get('staff_access'))
        user.AdminAccess = bool(request.form.get('admin_access'))
        db.session.commit()
        flash('User access updated successfully.')
        return redirect(url_for('userAccess'))
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
@app.route('/sms/send', methods=['GET', 'POST'])
def smsSend():
    if request.method == 'POST':
        phone_number = request.form.get('phoneNumber')
        message = 'Hello, your appointment has been scheduled.'
        try:
            message = client.messages.create(
                body=message,
                from_='+17752405149',  
                to=phone_number
            )
            flash('Notification sent successfully.', 'success')
            return redirect(url_for('dashboard'))
        except:
            flash('Failed to send notification', 'error')
            return redirect(url_for('dashboard'))
    else:
        return 'Method not allowed', 405



# Example view function that sends a SMS message
@app.route('/sendtext', methods=['GET', 'POST'])
def send_sms():
    message = client.messages.create(
        messaging_service_sid='MGdc049f1edc574951803c83a97cd37602',
        body='Good Bye, World!',
        from_='+17752405149',
        to='+17753763523')
    flash('Notification sent successfully.', 'success')

    return render_template("dashboardadmin.html"), 'SMS sent!'

