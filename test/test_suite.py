import unittest
from datetime import datetime
from models import User
from battlebornmobile.forms import SignUpForm

from flask import url_for
from flask_testing import TestCase
from battlebornmobile import app, db
from battlebornmobile.models import User, Pet, Appointment, Role
from battlebornmobile.forms import SignUpForm, LoginForm, PetForm, AppointmentForm

class unitTests(unittest.TestCase):
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
