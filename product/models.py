from product import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key= True)
	username = db.Column(db.String(15), nullable= False, unique= True)
	email_address = db.Column(db.String(50), nullable= False, unique= True)
	password_hash = db.Column(db.String(60), nullable= False)

	def __repr__(self):
		return f"User {self.username}"

	@property
	def password(self):
		return self.password
	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

	def check_password_correction(self, attempted_password):
		return bcrypt.check_password_hash(self.password_hash, attempted_password)
	

class Project(db.Model):
	id = db.Column(db.Integer(), primary_key= True)
	name = db.Column(db.String(30), nullable= False)
	contributor = db.Column(db.String(30), nullable= False, default= "N/A")
	likes = db.Column(db.Integer(), nullable= False, default= 0)
	comments = db.Column(db.Integer(), nullable= False, default= 0)
	description = db.Column(db.String(512), nullable= False, default= "This project has no descriptions")
	source_code = db.Column(db.String(2048), nullable= False)

	def __repr__(self):
		return f"Project {self.name}"


