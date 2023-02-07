from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import char_class
from flask_app.models import char_race
from flask_app.models import item
from flask_app.models import user
from flask_app.models import weapon
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
    weapons = sorted(char_race.race_prof['weapon_type'])
    weaponType_list = {}
    for type in weapons:
        weaponType_list[type] = char_race.race_prof['weapon_type'][type]
    
    armorType_list = char_race.race_prof['armor_prof']
    
    race_lang = char_race.race_prof['lang_prof']
    
    skill_prof = char_race.race_prof['skill_prof']
    
    
    
    return render_template("new_race.html", skill_prof = skill_prof, race_lang = race_lang, armor = armorType_list, weapons = weaponType_list, descriptions_num = descriptions_num,
                        racial_num = racial_num, user=logged_in_user)

@app.route("/create_race", methods=['POST'])
def create_race():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    # print("\n___Race Request.form")
    # pprint(request.form, indent=3, depth=3)
    data = {
        "user_id" : logged_in_user.id,
        "name" : request.form["name"],
        "speed" : request.form["speed"],
    }
    
    descriptions = {}
    nums = request.form['descriptions_num']
    # print("\n___Desc nums is___",type(nums))
    descriptions['number_of'] = int(nums)
    tnums = int(nums) + 1
    for num in range(1,tnums):
        heading = "description_heading_" + str(num)
        descript = "description_" + str(num)
        if heading in request.form:
            descriptions[heading] = request.form[heading]
        if descript in request.form:
            descriptions[descript] = request.form[descript]
    
    data['description'] = json.dumps(descriptions)
    
    racial_traits = {}
    nums = request.form['racial_num']
    # print("\n___racial nums is___",type(nums))
    racial_traits['number_of'] = int(nums)
    tnums = int(nums) + 1
    for num in range(1,tnums):
        heading = "racial_heading_" + str(num)
        racial_trait = "racial_trait_" + str(num)
        if heading in request.form:
            racial_traits[heading] = request.form[heading]
        if racial_trait in request.form:
            racial_traits[racial_trait] = request.form[racial_trait]
    
    race_lang = char_race.race_prof['lang_prof']
    
    for i in range(1,4):
        lang_prof = "lang_prof_" + str(i)
        if lang_prof in request.form:
            if request.form[lang_prof] != 'null' and request.form[lang_prof] != "":
                racial_traits[lang_prof] = request.form[lang_prof]
    
    data['racial_traits'] = json.dumps(racial_traits)
    
    attrib = [
        "str",
        "dex",
        "con",
        "int",
        "wis",
        "cha"
    ]
    racial_attrib = {}
    for atb in attrib:
        racial_attrib[atb] = request.form[atb]
        
    data['racial_attrib'] = json.dumps(racial_attrib)
    
    racial_profs = {}
    for prof_type in char_race.race_prof:
        # print("\n prof_type in char_race.race_prof", prof_type)
        for prof in char_race.race_prof[prof_type]:
            # print("\n Prof in prof_type ", prof)
            if prof in request.form:
                if request.form[prof] == 'on':
                    racial_profs[prof] = prof
                elif request.form[prof] != 'null':
                    racial_profs[prof]= request.form[prof]

    data['racial_profs'] = json.dumps(racial_profs)
    # print("\n___racial_profs___")
    # pprint(data['racial_profs'], indent=2, depth=3)
    
    char_race.Char_race.save(data)
    
    return redirect('/dashboard')

@app.route("/edit_race/<int:id>")
def edit_race(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    weapons = sorted(char_race.race_prof['weapon_type'])
    weaponType_list = {}
    for type in weapons:
        weaponType_list[type] = char_race.race_prof['weapon_type'][type]
    
    armorType_list = char_race.race_prof['armor_prof']
    a_race = char_race.Char_race.get_char_race_by_id(id)
    
    edit_var = {
        "attrib" : {
            "str" : "Strength",
            "dex" : "Dexterity",
            "con" : "Constitution",
            "int" : "Intelligence",
            "wis" : "Wisdom",
            "cha" : "Charisma"
        },
        "weapon_prof" : {
            "simple_weapons_prof" : "Simple Weapons",
            "martial_weapons_prof" : "Martial Weapons",
            "sword_prof" : "Sword",
            "axe_prof" : "Axe",
            "bow_prof" : "Bow",
            "pole_prof" : "Pole Arm",
            "warhammer_prof" : "War Hammer"
            },
        "lang_prof" : {
            "common_lang_prof" : "Common",
            "dwarvish_lang_prof" : "Dwarvish",
            "elvish_lang_prof" : "Elvish",
            "giant_lang_prof" : "Giant",
            "gnomish_lang_prof" : "Gnomish",
            "goblin_lang_prof" : "Goblin",
            "halfling_lang_prof" : "Halfling",
            "orc_lang_prof" : "Orc",
            "abyssal_lang_prof" : "Abyssal",
            "celestial_lang_prof" : "Celestial",
            "draconic_lang_prof" : "Draconic",
            "deepspeech_lang_prof" : "Deepspeech",
            "infernal_lang_prof" : "Infernal",
            "primordial_lang_prof" : "Primordial",
            "sylvan_lang_prof" : "Sylvan",
            "undercommon_lang_prof" : "Undercommon"
        },
        "skill_prof" : {
            "acrobatics_prof" : "Acrobatics",
            "animal_handling_prof" : "Animal Handling",
            "arcana_prof" : "Arcana",
            "athletics_prof" : "Athletics",
            "deception_prof" : "Deception",
            "history_prof" : "History",
            "insight_prof" : "Insight",
            "intimidation_prof" : "Intimidation",
            "investigation_prof" : "Investigation",
            "medicine_prof" : "Medicine",
            "nature_prof" : "Nature",
            "perception_prof" : "Perception",
            "performance_prof" : "Performance",
            "persuasion_prof" : "Persuasion",
            "religion_prof" : "Religion",
            "sleight_of_hand_prof" : "Sleight of Hand",
            "stealth_prof" : "Stealth",
            "survival_prof" : "Survival",
            },
    }
    
    return render_template("edit_race.html", edit_var = edit_var, a_race = a_race, armor = armorType_list, weapons = weaponType_list, user=logged_in_user)

    