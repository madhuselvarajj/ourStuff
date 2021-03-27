from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()]) #validators that field is not null and is valid email
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
