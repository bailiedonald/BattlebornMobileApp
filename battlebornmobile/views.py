from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#Create FlaskInstance
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = "Super Secret Password"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/battleborn'



#Initailize Database
db = SQLAlchemy(app)

#Create db Model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # Create a Function to return a string
    def __repr__(self):
        return '<Name %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


#Route Decorators
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
    return render_template("scheduler.html", appointmnet_requests = appointmnet_requests)

#Services
@app.route('/services')
def services():
    return render_template("services.html")

#Services
@app.route('/contact')
def contact():
    return render_template("contact.html")

#Login Page
@app.route('/login')
def login():
    return render_template("login.html")

#Layout
@app.route('/layout')
def layout():
    return render_template("layout.html")
