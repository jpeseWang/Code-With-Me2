from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from product import app
from product.models import User, Project

class RegisterForm(FlaskForm):
	def validate_username(self, username_to_check):
		with app.app_context():
			user = User.query.filter_by(username= username_to_check.data).first()
		if user:
			raise ValidationError("Username already exists! Please try a different username!")
		
	def validate_email_address(self, email_address_to_check):
		with app.app_context():
			email= User.query.filter_by(email_address= email_address_to_check.data).first()
		if email:
			raise ValidationError("Email already exists! Please try a different email!")

	username = StringField(label= "Username", validators= [Length(min= 6, max= 30), DataRequired()])
	email_address = StringField(label= "Email", validators= [Email(), DataRequired()])
	password_1 = PasswordField(label= "Password", validators= [Length(min= 6, max= 20), DataRequired()])
	password_2 = PasswordField(label= "Confirm password", validators= [EqualTo("password_1"), DataRequired()])
	submit = SubmitField(label= "Create Account")

class LoginForm(FlaskForm):
	username = StringField(label= "Username", validators= [DataRequired()])
	password = PasswordField(label= "Password", validators= [DataRequired()])
	submit = SubmitField(label= "Sign in")

class CreateForm(FlaskForm):
	def validate_name(self, name_to_check):
		with app.app_context():
			proj_name = Project.query.filter_by(name= name_to_check.data).first()
		if proj_name:
			raise ValidationError("Project's name already exists! Please try a different name!")

	name = StringField(label= "Project Name", validators= [Length(min= 3, max= 60), DataRequired()])
	description = TextAreaField(label= "Description", validators= [Length(min= 10, max= 512), DataRequired()])
	source_code = TextAreaField(label= "Your source code", validators= [Length(min= 5, max= 2048), DataRequired()])
	submit = SubmitField(label= "Create")
