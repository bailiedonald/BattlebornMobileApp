from flask import Flask, render_template, request
from flask_mail import Mail, Message
import secrets
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build




app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'spencer@alsetdsgd.com'
app.config['MAIL_PASSWORD'] = 'Spring22'

mail = Mail(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
        user = {'email': email, 'token': token, 'verified': False}

        return 'Thank you for signing up! Please check your email to verify your email address.'

    return render_template('signup.html')

@app.route('/verify/<token>')
def verify(token):
    # Retrieve the user's account information based on the token provided in the link
    # You can use a database or other storage mechanism to retrieve this information
    user = {'email': 'user@example.com', 'token': 'AbCdEf123456', 'verified': False}

    # Compare the token in the link to the one generated earlier
    if token == user['token']:
        # Update the user's account information to indicate that the email address is now verified
        user['verified'] = True

        return 'Your email address has been verified!'

    return 'Invalid verification link.'

if __name__ == '__main__':
    app.run(debug=True)
