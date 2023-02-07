from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import item
from flask_app.models import character
from flask_app.models import user
from flask_app.models import char_class



def swap_out(str):
    str = ''.join(str)
    str.replace("_", " ")
    # for i in range(len(str)):
    #     if str[i] == "_":
    #         str[i] = " "
    return str

def f3(str):
    tmp = ""
    for i in range(3):
        tmp += str[i]
    return tmp.title()

def no_prof(str):
    tmp = ""
    for i in range(len(str)-5):
        if str[i] == '_':
            tmp += ' '
        else:
            tmp += str[i]
    return tmp.title()


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
    classes = char_class.Char_class.get_all()
    for a_class in classes:
        savs = ""
        # print("\na_class.sav_prof is: ",a_class.sav_prof)
        for sav in a_class.sav_prof:
            _sav = f3(sav)
            # _sav.title()
            # print("\n__sav of sav_prof 2 ",_sav)
            savs += _sav + ' '
        a_class.sav_prof = savs
        
        skills = ""
        for skill in a_class.skill_prof:
            if skill.isdigit():
                tmp = 'Choose (' + skill + ')'
            else:
                tmp = no_prof(skill)
            skills += tmp + ', '
        a_class.skill_prof = skills

        armor_weapons = ""
        for armor_weapon in a_class.armor_weapon_prof:
            tmp = no_prof(armor_weapon)
            armor_weapons += tmp + ', '
        a_class.armor_weapon_prof = armor_weapons
        # print(f"\n___{a_class.name} Saves: {savs}")    
        # print(f"\n___{a_class.name} Skills: {skills}")
        # print(f"\n___{a_class.name} Armor and Weapons: {armor_weapons}")            
    return render_template("item_dashboard.html", items=items, characters = characters, user = logged_in_user, classes = classes)
    
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

