from flask import Blueprint, request, render_template

auth = Blueprint("auth", __name__)

# GET user navigates to page and gets served the empty form
# POST the user fills out the login, hits submit, credentials gets sent to the server
@auth.route("/login", methods = ["GET", "POST"])
def login():
    # show login page
    if request.method == "GET":
        return render_template("login.html")
    
    # read submitted data and check it against DB
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)
        return render_template("Logged in with success")

# GET user navigates to page and gets served empty form to create user
# POST user fills out form and we sent it to the server to create the user
@auth.route("/create_user", methods = ["GET", "POST"])
def create_user():
    pass

# POST - intentional action to end the user session, redirects to login
@auth.route("/logout", methods = ["POST"])
def logout():
    pass