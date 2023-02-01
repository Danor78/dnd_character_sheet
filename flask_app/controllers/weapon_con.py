from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import item
from flask_app.models import weapon
from flask_app.models import armor
from flask_app.models import user

@app.route("/new_weapon")
def new_weapon():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    
    logged_in_user =user.User.get_by_id(session["user_id"])
    weapons = {}
    weapons['item_type'] = item.item_type
    weapons['item_src'] = item.item_src
    weapons['item_rarity'] = item.item_rarity
    weapons['weapon_type'] = weapon.weapon_type
    weapons['damage_die'] = weapon.damage_die
    weapons['damage_type'] = weapon.damage_type

    return render_template("new_weapon.html", weapons = weapons, user = logged_in_user)

@app.route("/create_weapon", methods=["POST"])
def create_weapon():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    
    if not weapon.Weapon.validate_weapon(request.form): # if not (false)
        print("\n ____weapon con validation FAILED____")
        return redirect("/new_weapon")
    
    logged_in_user =user.User.get_by_id(session["user_id"])
    
    weapon_info ={
        "weapon_type" : request.form["weapon_type"],
        "damage_die" : request.form["damage_die"],
        "damage_type" : request.form["damage_type"],
        "magical_mod" : request.form['magical_mod'],
        "base_attribute" : 10,
        "properties" : "",
    }
    if 'range' not in request.form:
        weapon_info['base_attrb_key'] = "dexterity"
    else:
        weapon_info['base_attrb_key'] = "strength"
    
    
    for properties in weapon.weapon_properties:
        for prop in properties:
            if not weapon_info['properties'] and prop in request.form:
                weapon_info['properties'] = prop
            elif prop in request.form:
                weapon_info['properties'] += ', ' + prop

    print("\n____Weapon Info____->", weapon_info)
    
    item_info = {
        "user_id" : request.form['user_id'],
        "type" : request.form["type"],
        "cost" : request.form["cost"],
        "weight" : request.form["weight"],
        "description" : request.form["description"],
        "rarity" : request.form["rarity"],
        "is_magical" : request.form["is_magical"],
        "is_attunable" : request.form["is_attunable"],
        "source": request.form["source"],
        "img": "",
        "armor_id" : None,
        "weapon_id" : weapon.Weapon.save(weapon_info)
    }
    if 'magical_mod' in request.form and int(request.form['magical_mod']) > 0:
        item_info["name"] = request.form["name"] + request.form['magical_mod']
    else:
        item_info["name"] = request.form["name"]
        
        
    
    
    item.Item.save(item_info)
    return redirect("/dashboard")
    