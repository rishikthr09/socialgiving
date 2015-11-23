from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, validators, TextField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
	email = TextField('email', validators=[validators.Required('Field cannot be empty')])
	password = PasswordField('password', validators=[validators.Required('Enter a valid password')])
	remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
	name = TextField('name', validators=[validators.Required('Field cannot be empty')])
	email = TextField('email', validators=[validators.Required('Cannot Be Empty')])
	password = PasswordField('password', validators=[validators.Required('Enter a valid password'),validators.EqualTo('repeat_password',message="Passwords Do Not Match")])
	repeat_password = PasswordField('repeat_password', validators=[validators.Required('Cannot Be Empty')])

class PostItemForm(Form):
	name = TextField('name', validators=[validators.Required('Name Cannot Be Empty')])
	info = TextField('info')

class RequestItemForm(Form):
	info = TextField('info')

class MessageForm(Form):
	message = TextField('message', validators=[validators.Required('Field cannot be empty')])