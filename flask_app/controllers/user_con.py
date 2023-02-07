from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/register", methods={"POST"})
def register():
    # print("")
    # print("\n ____user_con /register____")
    # print("\n ____Request.Form info____")
    # print(request.form)
    if not user.User.validate_register(request.form): # if not (false)
        print("\n ____user_con validation FAILED____")
        return redirect("/registration")
    user_id = user.User.register(request.form)
    session["user_id"] = user_id
    return redirect("/dashboard")

# @app.route("/home")
# def home():
#     if "user_id" not in session:
#         redirect("/")
#     logged_in_user =user.User.get_by_id(session["user_id"])
    
#     return render_template("home.html",logged_in_user=logged_in_user)

@app.route("/logout")
def logout():
    session.clear
    return redirect("/")

@app.route("/login", methods={"POST"})
def login():
    # print("")
    # print("\n ____user_con /login____")
    logged_in_user = user.User.validate_login(request.form)
    if not logged_in_user:
        print("\n ____user_con loin FAILED____")
        return redirect("/")
    print ("\n _____Logged in User id____ ->", logged_in_user)
    session["user_id"] = logged_in_user.id
    return redirect("/dashboard")