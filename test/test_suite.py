import unittest
from datetime import datetime
from battlebornmobile.models import User
from flask import url_for
from flask_testing import TestCase
from flask_login import current_user
from battlebornmobile import app, db, os
from battlebornmobile.models import User, Pet, Appointment, Role
from battlebornmobile.forms import SignUpForm, LoginForm, PetForm, AppointmentForm, UpdateProfilePictureForm
from battlebornmobile.views import Event

class unitTests(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_successful(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
        response = self.app.post('/login', data=dict(email='test@example.com', password='password'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(current_user.is_authenticated)

    def test_login_unsuccessful(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
        response = self.app.post('/login', data=dict(email='test@example.com', password='wrongpassword'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)

    def test_login_with_next_page(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
        response = self.app.post('/login?next=/dashboard', data=dict(email='test@example.com', password='password'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/dashboard')

    def test_login_redirect_authenticated_user(self):
        with app.app_context():
            user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(user)
            db.session.commit()
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user_id'] = user.id
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')
        
    def setUp(self):
        """Setup test environment"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

        # Add a test user to the database
        self.user = User(username='testuser', email='testuser@example.com', password='password')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Destroy test environment"""
        db.session.remove()
        db.drop_all()

    def test_profile_picture_update(self):
        # Login as the test user
        self.app.post('/login', data=dict(
            email='testuser@example.com',
            password='password'
        ), follow_redirects=True)

        # Upload a profile picture for the user
        with open('test.jpg', 'rb') as f:
            data = {'profile_picture': (f, 'test.jpg')}
            response = self.app.post('/profile/picture/update', data=data, follow_redirects=True)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the user's profile picture was updated in the database
        user = User.query.filter_by(id=self.user.id).first()
        self.assertIsNotNone(user.image_file)
        self.assertEqual(user.image_file, 'testuserpicture.jpg')

        # Delete the test image file
        os.remove(os.path.join(app.root_path, 'static/profile_pics', 'testuserpicture.jpg'))

    def test_schedule_appointment_valid_inputs(client, appointment):
        # Test that a valid appointment can be scheduled
        response = client.post(f'/appointments/schedule/{appointment.id}',
                            data={'dateScheduled': '2023-05-01', 'timeScheduled': '09:00:00'})
        assert response.status_code == 302  # Redirects to confirm_appointment page
        assert appointment.scheduled == True
        assert appointment.dateScheduled == '2023-05-01'
        assert appointment.timeScheduled == '09:00:00'
        assert b'Appointment scheduled successfully!' in response.data

    def test_schedule_appointment_invalid_inputs(client, appointment):
        # Test that appointment cannot be scheduled with missing date or time
        response = client.post(f'/appointments/schedule/{appointment.id}',
                            data={'dateScheduled': '', 'timeScheduled': ''})
        assert response.status_code == 302  # Redirects to scheduler page
        assert appointment.scheduled == False
        assert b'Please select a date and time for the appointment.' in response.data

    def test_schedule_appointment_already_scheduled(client, scheduled_appointment):
        # Test that a scheduled appointment cannot be scheduled again
        response = client.post(f'/appointments/schedule/{scheduled_appointment.id}',
                            data={'dateScheduled': '2023-05-01', 'timeScheduled': '09:00:00'})
        assert response.status_code == 400  # Bad request
        assert scheduled_appointment.scheduled == True
        assert b'' in response.data  # Check for appropriate error message in response data

    def test_schedule_appointment_cancelled(client, cancelled_appointment):
        # Test that a cancelled appointment cannot be scheduled
        response = client.post(f'/appointments/schedule/{cancelled_appointment.id}',
                            data={'dateScheduled': '2023-05-01', 'timeScheduled': '09:00:00'})
        assert response.status_code == 400  # Bad request
        assert cancelled_appointment.scheduled == False
        assert b'' in response.data  # Check for appropriate error message in response data

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_search_route(self):
        response = self.app.get('/staff/records/search?q=John')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    def test_update_user_route(self):
        response = self.app.post('/update/1', data=dict(email='test@test.com'))
        self.assertEqual(response.status_code, 200)
        user = User.query.get(1)
        self.assertEqual(user.email, 'test@test.com')

    def test_calendar_route(self):
        response = self.app.get('/calendar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Calendar</h1>', response.data)

    def test_events_route(self):
        event = Event(title='Appointment', start='2023-04-25 10:00:00')
        db.session.add(event)
        db.session.commit()
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Appointment', response.data)

    def test_sms_send_route(self):
        response = self.app.post('/sms/send', data=dict(phoneNumber='+17753763523'))
        self.assertEqual(response.status_code, 302)

    def test_send_sms_route(self):
        response = self.app.post('/sendtext')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SMS sent!', response.data)

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['SECRET_KEY'] = 'secret_key'
        return app

    def initialization():
        db.create_all()
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()
        admin = User(username='admin', email='admin@test.com', password='password', roles=[role])
        db.session.add(admin)
        db.session.commit()

    def destructors():
        db.session.remove()
        db.drop_all()
        
    def test_create_user(self):
        user = User(username='testuser', email='testuser@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        result = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'testuser')
        self.assertEqual(result.email, 'testuser@example.com')
        self.assertEqual(result.password, 'password')
        

    def test_validate_username_unique(app, user):
        # Create a user with the same username as the one we'll use to test validation
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

            # Create a signup form with the same username as the existing user
        form = SignUpForm(username='testuser', email='test2@example.com', password='password',
                confirm_password='password', firstName='John', lastName='Doe',
                phoneNumber='123-456-7890', streetNumber='123 Main St',
                city='Anytown', state='CA', zipcode='12345')

        # Validate the form and check that it raises a validation error for the username field
        assert not form.validate()
        assert 'That username is taken. Please choose a different one.' in form.username.errors
    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Battle Born Mobile', response.data)

    def test_about(self):
        response = self.client.get(url_for('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)

    def test_services(self):
        response = self.client.get(url_for('services'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Our Services', response.data)

    def test_contact(self):
        response = self.client.get(url_for('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Us', response.data)

    def test_layout(self):
        response = self.client.get(url_for('layout'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Layout', response.data)

    def test_signup(self):
        response = self.client.get(url_for('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create an Account', response.data)

    def test_signup_post(self):
        data = dict(username='testuser', email='testuser@test.com', password='password', confirm_password='password', firstName='Test', lastName='User', phoneNumber='1234567890', streetNumber='123', city='Reno', state='NV', zipcode='89523')
        response = self.client.post(url_for('signup'), data=data, follow_redirects=True)
        self.assertIn(b'Your account has been created!', response.data)

    def test_login(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_login_post(self):
        data = dict(email='admin@test.com', password='password')
        response = self.client.post(url_for('login'), data=data, follow_redirects=True)
        self.assertIn(b'Welcome to the Battle Born Mobile Dashboard', response.data)

    def test_logout(self):
        with self.client:
            self.client.post(url_for('login'), data=dict(email='admin@test.com',
                                                        password='password'), follow_redirects=True)
            response = self.client.get(url_for('logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome to Battle Born Mobile', response.data)
