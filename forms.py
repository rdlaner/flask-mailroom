#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import Donor


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        query = Donor.select().where(Donor.name == username.data)
        if query:
            raise ValidationError('Username already in use. Please try a'
                                  'different username.')

    def validate_email(self, email):
        query = Donor.select().where(Donor.email == email.data)
        if query:
            raise ValidationError('Email already in use. Please try a'
                                  'different email address.')


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
