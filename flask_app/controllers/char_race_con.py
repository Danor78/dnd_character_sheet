from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import char_class
from flask_app.models import item
from flask_app.models import user
import math
from pprint import pprint
import json

@app.route("/new_race")
def new_race():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    descriptions_num = 1
    racial_num = 1
    return render_template("new_race.html", descriptions_num = descriptions_num, racial_num = racial_num, user=logged_in_user)
    