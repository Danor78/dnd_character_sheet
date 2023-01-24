from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import item
# from flask_app.models import weapon
from flask_app.models import armor
from flask_app.models import user


@app.route("/new_armor")
def new_armor():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    armors = {}
    armors['item_type'] = item.item_type
    armors['item_src'] = item.item_src
    armors['item_rarity'] = item.item_rarity
    armors['armor_type'] = armor.armor_type
    armors['stealth_prop'] = armor.stealth_prop
    armors['body_part'] = armor.body_part

    return render_template("new_armor.html", armors = armors, user=logged_in_user)


@app.route("/create_armor", methods=["POST"])
def create_armor():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n____ armor Request form data____",request.form)
    armor_info ={
        "armor_type" : request.form["armor_type"],
        "body_part" : request.form['body_part'],
        "armor_AC" : request.form["armor_AC"],
        "magical_mod" : request.form['magical_mod'],
        "str_req" : request.form['str_req'],
        "stealth_property" : request.form['stealth_property']
    }
    print("\n____armor Info___->", armor_info)
    
    item_info = {
        "user_id" : logged_in_user.id,
        "name" : request.form["name"],
        "type" : request.form["type"],
        "cost" : request.form["cost"],
        "weight" : request.form["weight"],
        "description" : request.form["description"],
        "rarity" : request.form["rarity"],
        "is_magical" : request.form["is_magical"],
        "is_attunable" : request.form["is_attunable"],
        "source": request.form["source"],
        "img": "",
        "armor_id" :  armor.Armor.save(armor_info),
        "weapon_id" : None
    }
    if 'magical_mod' in request.form and int(request.form['magical_mod']) > 0:
        item_info["name"] = request.form["name"] + request.form['magical_mod']
    else:
        item_info["name"] = request.form["name"]
    
    item.Item.save(item_info)
    return redirect("/dashboard")