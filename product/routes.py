from product import app, db
from flask import render_template, redirect, url_for, flash
from product.models import Project, User
from product.forms import RegisterForm, LoginForm, CreateForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
	return render_template("home.html")

@app.route("/projects")
@login_required
def projects_page():
	projects = Project.query.all()
	return render_template("projects.html", projects= projects)

@app.route("/register", methods= ['GET', 'POST'])
def register_page():
	form = RegisterForm()
	if form.validate_on_submit():
		user_to_create = User(username= form.username.data,
							email_address= form.email_address.data,
							 password= form.password_1.data)
		with app.app_context():
			db.session.add(user_to_create)
			db.session.commit()
			login_user(user_to_create)
		
		flash(f"Account created successfully! You are now logged in as {user_to_create.username}.", category= "success")

		return redirect(url_for("projects_page"))

	if form.errors != {}: 
		for err_msg in form.errors.values():
			flash(f"There was an error with creating a user: {err_msg}", category= "danger")

	return render_template("register.html", form= form)

@app.route("/login", methods= ['GET', 'POST'])
def login_page():
	form = LoginForm()
	if form.validate_on_submit():
		with app.app_context():
			attempted_user = User.query.filter_by(username= form.username.data).first()
			if attempted_user and attempted_user.check_password_correction(attempted_password= form.password.data):
				login_user(attempted_user)
				flash(f"Success! You are logged in as {attempted_user.username}.", category= "success")
				return redirect(url_for("projects_page"))
			else:
				flash("Username and password are incorrect! Please try again!", category= "danger")

	return render_template("login.html", form= form)

@app.route("/logout")
def logout_page():
	logout_user()
	flash("You have been logged out!", category= "info")
	return redirect(url_for("home_page"))

@app.route("/create", methods= ['GET', 'POST'])
@login_required
def create_page():
	form = CreateForm()
	if form.validate_on_submit():
		proj_to_create = Project(name= form.name.data, contributor= current_user.username, description= form.description.data,
									source_code= form.source_code.data)
		with app.app_context():
			db.session.add(proj_to_create)
			db.session.commit()
			flash(f"Project {proj_to_create.name} created successfully!", category= "success")

		return redirect(url_for("projects_page"))

	if form.errors != {}:
		for err_msg in form.errors.values():
			flash(f"There was an error with creating a project: {err_msg}", category= "danger")

	return render_template("create.html", form= form)

