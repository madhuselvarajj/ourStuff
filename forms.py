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
    
class filterForm(FlaskForm):
    city = StringField('enter city to filter', default='none')
    category = StringField('enter category to filter by', default='none')
    maxPrice = StringField('enter maximum price to filer by', default='none')
    submit = SubmitField('Filter')
