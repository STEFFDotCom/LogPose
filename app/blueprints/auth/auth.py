from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from flask_login import login_user

auth = Blueprint("auth", __name__)

# GET user navigates to page and gets served the empty form
# POST the user fills out the login, hits submit, credentials gets sent to the server
@auth.route("/login", methods = ["GET", "POST"])
def login():
    # show login page
    if request.method == "GET":
        return render_template("auth/login.html")
    
    # read submitted data and check it against DB
    if request.method == "POST":
        # get the password and username the user tried to login with
        username_input = request.form.get("username")
        password_input = request.form.get("password")

        # check the username against the DB and return the first result - return None if it cant find it
        stored_user = User.query.filter_by(user_name = username_input).first()

        # if username is not valid, return error message and redirect to login page
        if stored_user is None:
            flash("Wrong username or password - try again!", "danger")
            return redirect(url_for("auth.login"))
        
        if check_password_hash(stored_user.password_hash, password_input):
            # remember=True has the user logged in even after closing the browser
            login_user(stored_user, remember=True)
            # PLACEHOLDER UNTIL WE CREATE BOARDS REMEMBER TO CHANGE
            return redirect(url_for("auth.login"))
        else:
            flash("Wrong username or password - try again!", "danger")
            return redirect(url_for("auth.login"))

# GET user navigates to page and gets served empty form to create user
# POST user fills out form and we sent it to the server to create the user
@auth.route("/create_user", methods = ["GET", "POST"])
def create_user():
    # show register page
    if request.method == "GET":
        return render_template("auth/register.html")
    
    # take data from user and check against DB - if it passes it regisers the user in DB and sends the user to login page
    if request.method == "POST":

        email_input = request.form.get("reg-mail")
        username_input = request.form.get("reg-username")
        password_input = request.form.get("reg-password")
        hashed_password = generate_password_hash(password_input)
        verify_password_input = request.form.get("reg-verify-password")

        email_taken = User.query.filter_by(email = email_input).first()

        if email_taken is not None:
            flash("Email is already taken", "danger")
            return redirect(url_for("auth.create_user"))
        
        username_taken = User.query.filter_by(user_name = username_input).first()

        if username_taken is not None:
            flash("Username is already taken", "danger")
            return redirect(url_for("auth.create_user"))

        if password_input != verify_password_input:
            flash("Passwords does not match - try again!", "danger")
            return redirect(url_for("auth.create_user"))


        # create new user with the info from user
        new_user = User(user_name = username_input, email = email_input, password_hash = hashed_password)

        # add user to the DB
        db.session.add(new_user)

        # save user in DB and send log them in
        db.session.commit()
        return redirect(url_for("auth.login"))

# POST - intentional action to end the user session, redirects to login
@auth.route("/logout", methods = ["POST"])
def logout():
    pass