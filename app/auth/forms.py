#!/usr/bin/env python
# coding: utf-8

#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length


#class LoginForm(Form):
class LoginForm(FlaskForm):
    username = StringField('User or Email', validators=[Required(),
        Length(1,64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')
