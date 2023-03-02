# shell db script to migrate
# usage: Python3 migrate.py
from battlebornmobile import app, db
from battlebornmobile.models import User, Pet, Appointment, Role
app.app_context().push()
db.create_all()
exit()