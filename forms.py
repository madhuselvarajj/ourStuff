from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    lname = StringField('last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    dob = DateField('Date', validators=[DataRequired()])
    street = StringField('street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('province', validators=[DataRequired()])
    postalCode = StringField('postal code', validators=[DataRequired()])
    fname = StringField('first name', validators=[DataRequired()])
    submit = SubmitField('Register')

class UserInfoForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    street = StringField('street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('province', validators=[DataRequired()])
    postalCode = StringField('postal code', validators=[DataRequired()])
    submit = SubmitField('Save Changes', validators=[DataRequired()])


class FilterForm(FlaskForm):
    city = StringField('enter city to filter', default='none')
    category = StringField('enter category to filter by', default='none')
    maxPrice = StringField('enter maximum price to filer by', default='none')
    submit = SubmitField('Filter')

class RentalRequestForm(FlaskForm):
    startDate = DateField('starting date', validators=[DataRequired()])
    duration = IntegerField('duration', validators=[DataRequired()])
    pickup = DateField('pick up date', validators=[DataRequired()])
    dropoff = DateField('drop off date', validators=[DataRequired()])
    submit = SubmitField('Request this rental')
