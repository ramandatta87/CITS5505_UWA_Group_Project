from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    uwa_id = StringField('UWA ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    c_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    clear_form = SubmitField('Clear')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    uwa_id = StringField('UWA ID', validators=[DataRequired(message='Enter UWA ID.')])
    submit = SubmitField('Send Reset Link')
