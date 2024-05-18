from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_ckeditor import CKEditor,CKEditorField

# Form for user registration
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    uwa_id = StringField('UWA ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    major = StringField('Major', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Form for user login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

 #Form for users who forgot their password
class ForgetPasswordForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    uwa_id = StringField('UWA ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message='Your password should be at least 6 characters long.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Submit')

# Form for changing password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', [
        DataRequired(),
        Length(min=6, message='Password should be at least 6 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', [
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')

# Form for editing user profile
class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])


# Form for creating and editing posts
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    question_type = RadioField('Question Type', choices=[('unit', 'Unit Question'), ('career', 'Career Preparation')], default='unit')
    submit = SubmitField("Submit")
    draft = SubmitField("Save as Draft")



# Form for Filter 
class FilterSortForm(FlaskForm):
    filter_by = SelectField('Filter By', choices=[('author', 'Author'), ('title', 'Title'), ('tag', 'Tag')], validators=[DataRequired()])
    filter_value = StringField('Filter Value')
    order = SelectField('Order', choices=[('asc', 'Ascending'), ('desc', 'Descending')], validators=[DataRequired()])
    submit = SubmitField('Apply')    

# Form for creating a reply
class ReplyForm(FlaskForm):
    answer = CKEditorField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for Filter Sort
class FilterSortForm(FlaskForm):
    order = SelectField('Order', choices=[('asc', 'Newest'), ('desc', 'Oldest')])
    submit = SubmitField('Apply')
    