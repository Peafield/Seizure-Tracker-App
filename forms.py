from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateTimeLocalField

class NewEntry(FlaskForm):
    date = DateTimeLocalField("Date and Time", validators=[DataRequired()])
    seizure_type = SelectField(u'Seizure Type', choices=['Strong', 'Medium', 'Mild'], validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Me Up')

class LogIn(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign In')