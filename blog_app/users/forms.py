from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from blog_app.models import User


class UserRegistrationForm(FlaskForm):
    email = StringField('Email*', validators=[DataRequired(), Email()])
    username = StringField('Username*', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password1 = PasswordField('Password*', validators=[DataRequired()])
    password2 = PasswordField('Password confirmation*', validators=[
                              DataRequired(), EqualTo('password1', 'Passwords have to match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')


class UserLoginForm(FlaskForm):
    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    submit = SubmitField('Login')
