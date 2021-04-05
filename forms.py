from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class registerForm(FlaskForm):
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
    fname = StringField('First Name')
    lname = StringField('Last Name')
    email = StringField('Email')
    password = PasswordField('Password')
    dob = DateField('Date')
    street = StringField('street', validators=[DataRequired()])
    city = StringField('City')
    province = StringField('province')
    postalCode = StringField('postal code')
    submit = SubmitField('Save Changes')
