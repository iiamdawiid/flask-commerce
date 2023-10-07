from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired, EqualTo
# will need sign up form, login form, edit profile form

class SignUpForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    email = StringField(label='New Email', validators=[validators.Optional()])
    confirm_email = StringField(label='Confirm New Email', validators=[validators.Optional(), EqualTo('email')])
    password = PasswordField('New Password', validators=[validators.Optional()])
    confirm_password = PasswordField('Confirm New Password', validators=[validators.Optional(), EqualTo('password')])
    submit = SubmitField()