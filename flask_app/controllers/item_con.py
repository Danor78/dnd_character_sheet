from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import item
from flask_app.models import weapon
from flask_app.models import armor
from flask_app.models import user


# from flask_app.models import weapon
# from flask_app.models import armor

@app.route("/new_item")
def new_item():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    return render_template("new_item.html", item_type = item.item_type, item_src = item.item_src, item_rarity = item.item_rarity, user = logged_in_user)

@app.route("/create_item", methods=["POST"])
def create_item():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    
    if not item.Item.validate_item(request.form): # if not (false)
        print("\n ____Item con validation FAILED____")
        return redirect("/new_item")
    
    logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n __Item Request.form__")
    print(request.form)
    
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
        "armor_id" : None,
        "weapon_id" : None,
        "img": None
    }
    
    print("\n __Item info__")
    print(item_info)
    
    item.Item.save(item_info)
    return redirect("/dashboard")

@app.route('/show_item/<int:id>')
def display_item(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    print("\n____display Item route____")
    a_item = item.Item.get_item_by_id(id)
    logged_in_user =user.User.get_by_id(session["user_id"])
    creator = user.User.get_by_id(a_item.user_id)
    item_src = item.item_src
    return render_template("display_item.html", item = a_item, creator = creator, user = logged_in_user, item_src = item_src)

@app.route('/edit_item/<int:id>')
def edit_item(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    print("\n____Edit Item route____")
    a_item = item.Item.get_item_by_id(id)
    creator = user.User.get_by_id(a_item.user_id)
    logged_in_user =user.User.get_by_id(session["user_id"])
    weapons = {}
    weapons['item_type'] = item.item_type
    weapons['item_src'] = item.item_src
    weapons['item_rarity'] = item.item_rarity

    if a_item.armor:
        weapons['armor_type'] = armor.armor_type
        weapons['stealth_prop'] = armor.stealth_prop
        weapons['body_part'] = armor.body_part
    
    if a_item.weapon:
        weapons['weapon_type'] = weapon.weapon_type
        weapons['damage_die'] = weapon.damage_die
        weapons['damage_type'] = weapon.damage_type
        weapons['properties'] = weapon.weapon_properties
        a_item.weapon.properties = a_item.weapon.properties.rsplit(',')
        print("\n____Weapons Properties____ ->",a_item.weapon.properties)
        a_item.weapon.damage_die = str(a_item.weapon.damage_die)
    
    return render_template("edit_item.html", item = a_item, weapons=weapons, creator = creator, user = logged_in_user)

@app.route('/update_item', methods=['POST'])
def update_item():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n _____update item route____")
    print("\n ____Update Request Form___", request.form)
    item_info = {
        "user_id" : request.form['user_id'],
        "id" : request.form["id"],
        "name" : request.form["name"],
        "type" : request.form["type"],
        "cost" : request.form["cost"],
        "weight" : request.form["weight"],
        "description" : request.form["description"],
        "rarity" : request.form["rarity"],
        "is_magical" : request.form["is_magical"],
        "is_attunable" : request.form["is_attunable"],
        "source": request.form["source"],
        "armor_id" : None,
        "weapon_id" : None,
        "img" : None
    }
    if "weapon_id" in request.form:
        item_info['weapon_id'] = int(request.form['weapon_id'])
        item_info['weapon_type'] = request.form['weapon_type']
        item_info['magical_mod'] = request.form['magical_mod']
        item_info['damage_die'] = request.form['damage_die']
        item_info['damage_type'] = request.form['damage_type']

        
        if 'range' not in request.form:
            item_info['base_attrb_key'] = "dexterity"
        else:
            item_info['base_attrb_key'] = "strength"
        item_info["base_attribute"] = 10
        
    
        
        for properties in weapon.weapon_properties:
            for prop in properties:
                if 'properties' not in item_info and prop in request.form:
                    item_info['properties'] = prop
                elif prop in request.form:
                    item_info['properties'] += ', ' + prop
        print("\n___Weapon Update Data___", item_info)
        weapon.Weapon.update(item_info)
    
    
    if "armor_id" in request.form:
        item_info['armor_id'] = int(request.form['armor_id'])
        item_info['armor_type'] = request.form['armor_type']
        item_info['body_part'] = request.form['body_part']
        item_info['magical_mod'] = request.form['magical_mod']
        item_info['armor_AC'] = request.form['armor_AC']
        item_info['str_req'] = request.form['str_req']
        item_info['stealth_property'] = request.form['stealth_property']
        print("\n___Armor Update Data___", item_info)
        armor.Armor.update(item_info)
    
        
    
    print("\n____item info____->", item_info)
    item.Item.update(item_info)
    
    return redirect("/dashboard")

@app.route("/delete_item/<int:id>")
def delete_item(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    item.Item.delete(id)
    return redirect("/dashboard")
    