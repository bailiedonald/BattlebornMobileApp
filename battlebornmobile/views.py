# Team Memebers Contributiing to this page: 
# Donald Bailie - 
# Davis DeSarle -
# Grant Kite -
# Spencer Carter -

import os, re, random, string, shutil, pdfkit
from flask import Flask, current_app, render_template, make_response, url_for, flash, redirect, jsonify, abort, request, send_file, send_from_directory
from battlebornmobile import app, db, bcrypt, mail, client
from battlebornmobile.forms import SignUpForm, AuthCodeForm, LoginForm, PetForm, AppointmentForm, ResetPasswordForm, UpdateProfileForm, UpdateProfilePictureForm, VerificationCodeActualForm
from battlebornmobile.models import User, Pet, Appointment
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from flask_mail import Mail, Message
from sqlalchemy import or_
from twilio.rest import Client
from werkzeug.utils import secure_filename



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
        # Format the phone number entered by the user
        cleaned_phoneNumber = re.sub('[^0-9]', '', form.phoneNumber.data)
        if cleaned_phoneNumber.startswith('1'):
            cleaned_phoneNumber = '+' + cleaned_phoneNumber
        else:
            cleaned_phoneNumber = '+1' + cleaned_phoneNumber



        # Update the user's account information to indicate that the email address is not yet verified
        # You can use a database or other storage mechanism to track this information
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=cleaned_phoneNumber, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
        
        # generate a new password and update user's password
        auth_code = ''.join(random.choices(string.digits, k=6))
        user.auth_code = auth_code
                
        # # Process the user's sign-up information and generate a verification token
        # email = form.email.data
        # username = form.username.data

        # # Send the verification email to the user's email address
        # msg = Message('Verify your email address', sender=app.config['MAIL_USERNAME'], recipients=[email])
        # msg.body = render_template('verification_email.txt', username=username)
        # mail.send(msg)

        #Add to Database 
        db.session.add(user)
        db.session.commit()

        flash('Please check your email to verify your new account')

        return redirect(url_for('confirm_account'))

    return render_template('signup.html', title='Sign Up', form=form)


#Confirm Account
@app.route('/account/confirm', methods=['GET', 'POST'])
def confirm_account():
    if request.method == 'POST':
        method = request.form.get('method')
        email_or_phone = request.form.get('email_or_phone')
        user = None

        if method == 'email':
            user = User.query.filter_by(email=email_or_phone).first()
        elif method == 'phoneNumber':
            user = User.query.filter_by(phoneNumber=email_or_phone).first()

        if user:
            if method == 'email':
                send_email(user.email, user.auth_code, user.username)
            elif method == 'phoneNumber':
                send_text(user.phoneNumber, user.auth_code)

            flash('An authentication code has been sent to your {}.'.format(method), 'success')
            return redirect(url_for('auth_code'))
        else:
            flash('Invalid email or phone number. Please try again.', 'danger')
            return redirect(url_for('confirm_account'))

    # Add this return statement for the case when the method is 'GET'
    return render_template('confirm_account.html', title='Confirm Account')


# Enter Auth Code route
@app.route('/account/code', methods=['GET', 'POST'])
def auth_code():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = AuthCodeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.auth_code == form.auth_code.data:
            user.active = True
            user.auth_code = None
            db.session.commit()
            login_user(user)
            flash('Your account has been activated!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid authentication code or email. Please try again.', 'danger')

    return render_template('auth_code.html', title='Auth Code', form=form)


# #Verify Account Page
# @app.route('/verify_account', methods=['GET', 'POST'])
# def verify_account():
#     phoneNumber = request.form['phoneNumber']
#     verificationCode = request.form['verificationCode']


# #Verify Email Page
# @app.route('/verify_email/<string:username>', methods=['GET'])
# def verify_email(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     user.active = True
#     db.session.commit()
#     flash('Your email has been confirmed! You can now login.', 'success')
#     return redirect(url_for('login'))


# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(or_(User.username == form.username_or_email.data.lower(), User.email == form.username_or_email.data.lower())).first()
        if user and user.check_password(form.password.data) and user.active:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            admin = current_user.AdminAccess
            staff = current_user.StaffAccess
            if admin:
                return render_template("dashboardadmin.html")
            elif staff and not admin:
                return render_template("dashboardstaff.html")
            else:
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email/username and password.', 'danger')
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
            user.temp_password = new_password
            db.session.commit()

            # send email with password reset instructions
            msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[user.email])
            msg.body = f'''To reset your password, visit the following link:
            {url_for('password_reset', _external=True)}

            Your new temporary password is: {new_password}

            If you did not make this request then simply ignore this email and no changes will be made.
            '''
            mail.send(msg)
            flash('An email has been sent with instructions to reset your password.', 'success')
            return redirect(url_for('login'))
        else:
            flash('There is no account with that email. You must register first.', 'warning')
    return render_template('password_forgot.html')


#Reset password 
@app.route('/password/reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('That is an invalid or not active user.', 'warning')
            return redirect(url_for('password_forgot'))
        if user.temp_password != form.temp_password.data:
            flash('The temporary password is incorrect.', 'danger')
            return redirect(url_for('password_reset'))
        user.temp_password = None
        user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    else:
        flash('The form was not valid.', 'danger')
        print(form.errors)

    return render_template('password_reset.html', title='Reset Password', form=form)


#Main Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Query all pets linked to the current user
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    # Query all appoinments linked to the current user
    appointments = Appointment.query.filter_by(owner_id=current_user.id).filter_by(cancelled=False, completed=False).all()

    return render_template("dashboard.html", pets=pets, appointments=appointments)


# Profile Update
@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
    staff = current_user.StaffAccess
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.phoneNumber = form.phoneNumber.data
        current_user.streetNumber = form.streetNumber.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zipcode = form.zipcode.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        if staff == True:
            return render_template("dashboardstaff.html")
        else:
            flash ("Your New Photo Is Ready")
            return render_template("dashboard.html")
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
        form.phoneNumber.data = current_user.phoneNumber
        form.streetNumber.data = current_user.streetNumber
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zipcode.data = current_user.zipcode
    return render_template('profile_update.html', title='Update User Information', form=form)


#Profile Picture Update
@app.route('/profile/picture/update', methods=['GET', 'POST'])
@login_required
def profile_picture_update():
    form = UpdateProfilePictureForm()
    staff = current_user.StaffAccess
    if form.validate_on_submit():
        # Generate custom filename for the uploaded image file
        _, file_ext = os.path.splitext(form.profile_picture.data.filename)
        filename = secure_filename(current_user.username + 'picture' + file_ext)

        # Save the uploaded image file
        image_path = os.path.join(app.root_path, 'static/profile_pics', filename)
        form.profile_picture.data.save(image_path)

        # Update the user's profile picture in the database
        current_user.image_file = filename
        db.session.commit()

        flash('Your profile picture has been updated!', 'success')
        if staff == True:
            return redirect(url_for('index'))
        else:
            flash ("Your Account Has Been Updated.")
            return render_template("dashboard.html")
    return render_template('profile_picture_update.html', form=form)


#Add Pet Page
@app.route("/pet/add", methods=['GET', 'POST'])
@login_required
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        pet = Pet(pet_name=form.pet_name.data, pet_dob=form.pet_dob.data, pet_species=form.pet_species.data, pet_breed=form.pet_breed.data, pet_color=form.pet_color.data, pet_height=form.pet_height.data, pet_weight=form.pet_weight.data, owner_id=current_user.id)

        # Save pet pic to filesystem
        if form.pet_pic.data:
            pic_filename = secure_filename(current_user.username + '_' + form.pet_name.data + '.' + form.pet_pic.data.filename.split('.')[-1])
            pic_path = os.path.join(app.root_path, 'static/pet_pics', pic_filename)
            form.pet_pic.data.save(pic_path)
            pet.pet_pic = pic_filename
        
        # Save PDF record to filesystem and update pet record field
        if form.pet_record.data:
            pdf_filename = secure_filename(current_user.username + '_' + form.pet_name.data + '.' + form.pet_record.data.filename.split('.')[-1])
            pdf_path = os.path.join(app.root_path, 'static/pet_records', pdf_filename)
            form.pet_record.data.save(pdf_path)
            pet.pdf_record = pdf_filename
        else:
            # Copy default pdf record if no file is uploaded
            default_pdf_path = os.path.join(app.root_path, 'static/pet_records/new_record.pdf')
            filename = f"{current_user.id}_{pet.pet_name}_record.pdf"
            pet.pdf_record = filename
            shutil.copyfile(default_pdf_path, os.path.join(app.root_path, 'static/pet_records', pet.pdf_record))

        # Add Pet to Pet Database
        db.session.add(pet)
        db.session.commit()

        flash('Your pet has been added!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_pet.html', form=form)


#Upload Pet PDF_Record
@app.route('/staff/records/update_pet_record/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def update_pet_record(pet_id):
    # Get the pet object from the database using the pet_id
    pet = Pet.query.filter_by(id=pet_id).first()

    if not pet:
        flash('Pet record not found', 'error')
        return redirect(url_for('customer_records'))

    if request.method == 'POST':
        # Handle the form submission
        if 'pdf_file' not in request.files:
            flash('No PDF file selected', 'error')
            return redirect(request.url)

        file = request.files['pdf_file']

        if not file.filename:
            flash('No PDF file selected', 'error')
            return redirect(request.url)

        # Save the PDF file to the server
        filename = f"{pet.owner_id}_{pet.pet_name}_record.pdf"
        file.save(os.path.join(app.root_path, 'static/pet_records/', filename))

        # Update the pet's PDF record in the database
        pet.pdf_record = filename
        db.session.commit()

        flash('PDF record updated successfully', 'success')
        return redirect(url_for('records'))

    # Render the update pet record form
    return render_template('update_pet_record.html', pet=pet)


#View PDF
@app.route('/view_pdf/<int:id>')
@login_required
def view_pdf(id):
    pet = Pet.query.get_or_404(id)
    pdf_path = os.path.join(app.root_path, 'static/pet_records', pet.pdf_record)
    return send_file(pdf_path, attachment_filename=pet.pdf_record)


#Appointment Request Page
@app.route("/appointment/request", methods=['GET', 'POST'])
@login_required
def appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(owner_id=current_user.id, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, pet_name=form.pet_name.data, service=form.service.data, weekday=form.weekday.data, timeSlot=form.timeSlot.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)

        # Update appointment cost based on service selected
        if appointment.service == "Checkup" or appointment.service == "Spay or Neutering":
            appointment.cost = 50
        elif appointment.service == "Vaccines":
            appointment.cost = 20
        elif appointment.service == "DeWorming":
            appointment.cost = 30
        elif appointment.service == "Dental":
            appointment.cost = 60
        elif appointment.service == "Surgical":
            appointment.cost = 500

        # Add Appointment to the Appointment Database
        db.session.add(appointment)
        db.session.commit()
        
        flash('Your request has been received!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('appointment_request.html', title='MakeAppointment', form=form)


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


# #All Unscheduled Appointments
# @app.route('/appointments/unscheduled')
# @login_required
# def unscheduled_appointments():
#     appointments = Appointment.query.filter_by(scheduled=False).all()
#     return render_template('appointment_unscheduled.html', appointments=appointments)


#Schedule Each Appointment
@app.route('/appointments/schedule/<int:id>', methods=['POST'])
@login_required
def schedule_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.scheduled or appointment.cancelled:
        abort(400)  # bad request

    date_scheduled = request.form['dateScheduled']
    time_scheduled = request.form['timeScheduled']

    if not date_scheduled or not time_scheduled:
        flash('Please select a date and time for the appointment.', 'error')
        return redirect(url_for('scheduler'))

    appointment.dateSheduled = date_scheduled
    appointment.timeSheduled = time_scheduled
    appointment.scheduled = True
    db.session.commit()
    flash('Appointment scheduled successfully!', 'success')
    return redirect(url_for('confirm_appointment'))


#Confirm appointment
@app.route('/appointment/confirm')
@login_required
def confirm_appointment():
    return render_template("appointment_confirm.html")


#All Appointments
@app.route('/appointments')
@login_required
def appointments():
    return render_template("appointments.html")


#Scheduler
@app.route('/staff/scheduler')
#@login_required
def scheduler():
    appointments = Appointment.query.filter_by(scheduled=False).all()
#     tappointments = Appointment.query.filter_by(dateSheduled=todaydate).all()
# tappointments=tappointments
    return render_template("scheduler.html", appointments=appointments, )


#Admin Dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    admin = current_user.AdminAccess
    if admin == True:
        return render_template("dashboardadmin.html")
    else:
        flash ("Access Denied Administrators Only.")
        return render_template("dashboard.html")


#Admin Tools
@app.route('/admin/tools')
@login_required
def admin_tools():
    admin = current_user.AdminAccess
    if admin == True:
        return render_template("admin_tools.html")
    else:
        flash ("Access Denied Administrators Only.")
        return render_template("dashboard.html")


#Admin User Access Table
@app.route('/admin/useraccess')
@login_required
def user_access():
    admin = current_user.AdminAccess
    if admin:
        search_query = request.args.get('q')
        if search_query:
            users = User.query.filter(User.lastName.contains(search_query)).all()
        else:
            users = User.query.all()
        return render_template('user_access.html', users=users, search_query=search_query)
    else:
        flash("Access Denied: Admin Only")
        return render_template("dashboard.html")


#Admin Edit User Access Table
@app.route('/admin/useraccess/<int:user_id>', methods=['POST'])
@login_required
def update_access(user_id):
    admin = current_user.AdminAccess
    if admin == True:
        user = User.query.get_or_404(user_id)
        user.active = bool(request.form.get('active'))
        user.StaffAccess = bool(request.form.get('staff_access'))
        user.AdminAccess = bool(request.form.get('admin_access'))
        db.session.commit()
        flash('User access updated successfully.')
        return redirect(url_for('user_access'))
    else:
        flash ("Access Denied Admin Only.")
        return render_template("dashboard.html")


#Generate Reports
@app.route('/admin/reports/generate', methods=['GET', 'POST'])
def generate_reports():
    if request.method == 'POST':
        # Extract the selected date from the form data
        selected_date = request.form.get('selected_date')
        # Redirect to the appropriate URL that includes the date
        return redirect(url_for('reports_date', date_scheduled=selected_date))
    else:
        return render_template('reports_generate.html')


#Daily Reports Template
@app.route('/reports/<date_scheduled>', methods=['GET', 'POST'])
def reports_date(date_scheduled):
    if request.method == 'POST':
        # Extract the selected date from the form data
        selected_date = request.form.get('selected_date')
        # Redirect to the appropriate URL that includes the date
        return redirect(url_for('reports_date', date_scheduled=selected_date))
    else:
        appointments = Appointment.query.filter_by(dateSheduled=date_scheduled).all()
        if not appointments:
            # Display a flash message if there are no appointments scheduled
            flash("No appointments scheduled for this date.")
        rendered = render_template("reports_date.html", appointments=appointments)
        pdf = pdfkit.from_string(rendered, False)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=apppointments_date.pdf'

        return response


# # Admin View Reports
# @app.route('/admin/reports/view')
# @login_required
# def reports_view():
#     admin = current_user.AdminAccess
#     if admin == True:
#         return render_template("reports_view.html")
#     else:
#         flash ("Access Denied Administrators Only.")
#         return render_template("dashboard.html")


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
    try:
        users = User.query.all()
        pets = Pet.query.all()
        return render_template('records.html', users=users)
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('dashboard'))


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
@login_required
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
    return render_template('calendar.html')


#Calendar Event class
class Event(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    start = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, start):
        self.title = title
        self.start = start
    

#Calendar events
@app.route('/events')
@login_required
def events():
    events = Appointment.query.all()
    event_list = []
    for event in events:
        if event.scheduled:
            event_list.append({
                'title': event.firstName + ' '  + event.lastName,
                'start': event.dateSheduled + 'T' + event.timeSheduled + ':00',
                #'start': event.convert_to_iso_format(event.dateSheduled, event.timeSheduled),
                'customText' : event.service,
                'pet_name' : event.pet_name,
                'address' : event.streetNumber + ', ' + event.city + ', ' + event.zipcode,
                'time_unformatted' : event.dateSheduled + ' at ' + event.timeSheduled
            })
    return jsonify(event_list)

if __name__ == '__main__':
    app.run(debug=True)
    

#SMS Notification Page
@app.route('/sms/send', methods=['GET', 'POST'])
@login_required
def smsSend():
    if request.method == 'POST':
        phone_number = request.form.get('phoneNumber')
        message = 'Hello, your appointment has been scheduled.'
        try:
            message = client.messages.create(
                body=message,
                from_='+1775#######',  
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
@login_required
def send_sms():
    message = client.messages.create(
        messaging_service_sid='MGdc049f1edc574951803c83a97cd37602',
        body='Good Bye, World!',
        from_='+1775#######',
        to='+1775#######')
    flash('Notification sent successfully.', 'success')

    return render_template("dashboardadmin.html"), 'SMS sent!'




#####################
#########
######
###
##
#
#
#
# This is the stuff that we were talking about Donnie.. If you need help with understanding it, let me know..

# import os
# import sqlite3
# import random
# from flask import Flask, render_template, request, flash, redirect, url_for
# from twilio.rest import Client
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize the Flask app
# app = Flask(__name__)

# def init_db():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         phone_number TEXT,
#         verification_sid TEXT,
#         verified INTEGER DEFAULT 0
#     )''')
#     conn.commit()
#     conn.close()

# init_db()

# # Initialize the Twilio client
# client = Client(account_sid, auth_token)

# # Define the start_verification function
# def start_verification(to, channel='sms'):
#     if channel not in ('sms', 'call', 'whatsapp'):
#         channel = 'sms'

#     service = verify_service_id

#     verification = client.verify \
#         .v2.services(service) \
#         .verifications \
#         .create(to=to, channel=channel)
    
#     return verification.sid

# # Create a function to store a user's phone number and verification SID in the database
# def store_verification_sid(phone_number, verification_sid):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('INSERT INTO users (phone_number, verification_sid) VALUES (?, ?)',
#               (phone_number, verification_sid))
#     conn.commit()
#     conn.close()

# # Create the route that displays the phone number form
# @app.route('/')
# def enter_phone_number():
#     return render_template('enterphonenumber.html')

# # Create the route that handles the phone number form submission
# @app.route('/send_verification_code', methods=['POST'])
# def send_verification_code():
#     phone_number = request.form['phone_number']
    
#     # Initiate a new verification using Twilio Verify
#     verification_sid = start_verification(phone_number)
    
#     # Store the verification SID in the database
#     store_verification_sid(phone_number, verification_sid)
    
#     # Render the verification code form
#     return render_template('verify_account.html')

# # Create the route that displays the verification code form
# @app.route('/verify_account', methods=['GET'])
# def verify_account():
#     return render_template('verify_account.html')

# @app.route('/check_verification_code', methods=['POST'])
# def check_verification_code():
#     phone_number = request.form['phone_number']
#     verification_code = request.form['verification_code']

#     # Retrieve the verification SID from the database
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT verification_sid FROM users WHERE phone_number = ?', (phone_number,))
#     result = c.fetchone()
#     conn.close()

#     verification_sid = result[0] if result else None

#     # Verify the verification code using the Twilio Verify API
#     if verification_sid:
#         verification_check = client.verify.v2.services(verify_service_id).verification_checks.create(to=phone_number, code=verification_code)

#         # Check if the verification was successful
#         if verification_check.status == 'approved':
#             # Update the user's verified status in the database
#             conn = sqlite3.connect('users.db')
#             c = conn.cursor()
#             c.execute('UPDATE users SET verified = 1 WHERE phone_number = ?', (phone_number,))
#             conn.commit()
#             conn.close()

#             # Display a confirmation page
#             return render_template('confirmed.html')

#         # Display a denial page if verification failed
#         else:
#             return render_template('denied.html')

#     # Display a denial page if no verification SID found
#     else:
#         return render_template('denied.html')


#     # Create the index page
# @app.route('/index')
# def index():
#     return render_template('index.html')

# # Create the login page
# @app.route('/login')
# def login():
#     return render_template('login.html')

# if __name__ == '__main__':
#     app.run()





"""
# Initialize the Twilio client
client = Client(account_Sid, auth_Token)

def send_verification_code(to, channel='sms'):
    if channel not in ('sms', 'call', 'email'):
        channel = 'sms'

    service = verify_service_id
 

    # Send the verification code using Twilio Verify
    verification = client.verify \
        .v2.services(service) \
        .verifications \
        .create(to=to, channel=channel)

    return verification.sid

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password, firstName=form.firstName.data, lastName=form.lastName.data, phoneNumber=form.phoneNumber.data, streetNumber=form.streetNumber.data, city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)

        db.session.add(user)
        db.session.commit()

        send_verification_code(user.phoneNumber, 'phoneNumber')
        
        # Redirect to the enter code page
        return redirect(url_for('enter_code', phoneNumber=user.phoneNumber))

    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/enter_code/<phoneNumber>', methods=['GET', 'POST'])
def enter_code(phoneNumber):
    if request.method == 'POST':
        verification_code = request.form.get('verification-code')
        verify_service_sid = 'VA7ed47f6948af9225236fc25e6b538888'
        

        # Verify the verification code using Twilio Verify
        client = Client(account_Sid, auth_Token)
        verification_check = client.verify \
            .services(verify_service_sid) \
            .verification_checks \
            .create(to=phoneNumber, code=verification_code)

        # If verification was successful, mark the user's phone number as verified
        if verification_check.status == 'approved':
            user = User.query.filter_by(phoneNumber=phoneNumber).first()
            if user:
                    user.auth_code = verification_code
                    db.session.commit()
        else:        
            flash('Your phone number has been confirmed! You can now login.', 'success')
            return redirect(url_for('login'))
        
    else:
        flash('Invalid verification code. Please try again.', 'error')

    return render_template('enterCode.html', phoneNumber=phoneNumber)

@app.route('/verify_phone_number', methods=['POST'])
def verify_phone_number():
    phoneNumber = request.form['phoneNumber']
    verificationCode = request.form.get('verification-code')

    client = Client(account_Sid, auth_Token)

    # Verify the verification code using Twilio Verify
    verification_check = client.verify.services('VA7ed47f6948af9225236fc25e6b538888').verification_checks.create(to=phoneNumber, code=verificationCode)

    # If verification was successful, mark the user's phone number as verified
    if verification_check.status == 'approved':
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if user:
            user.auth_code = verificationCode
            db.session.commit()
        else:        
            flash('Your phone number has been confirmed! You can now login.', 'success')
            return redirect(url_for('login'))
        
    else:
        flash('Invalid verification code. Please try again.', 'error')

"""

