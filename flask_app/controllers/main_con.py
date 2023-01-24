from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import item
from flask_app.models import character
from flask_app.models import user





# @app.route("/")
@app.route("/dashboard")
def character_sheet():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    items = item.Item.get_all()
    # characters = character.Character.get_all()
    characters = character.Character.get_all_by_user(logged_in_user.id)
    return render_template("item_dashboard.html", items=items, characters = characters, user = logged_in_user)
    
@app.route("/dashboard/<type>")
def order_items(type):
    if "user_id" not in session:
        return redirect("/")
        print("\n___<<< User not logged in >>>___")
    logged_in_user =user.User.get_by_id(session["user_id"])
    items = item.Item.get_all_by_order(type)
    # characters = character.Character.get_all()
    characters = character.Character.get_all_by_user(logged_in_user.id)
    return render_template("item_dashboard.html", items=items, characters = characters, user = logged_in_user)

