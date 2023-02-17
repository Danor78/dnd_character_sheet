from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import character
from flask_app.models import char_class
from flask_app.models import char_race
from flask_app.models import char_background
from flask_app.models import cs_lib
from flask_app.models import user
from pprint import pprint
import math
import json


@app.route("/new_character")
def add_character():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n___new character route____")
    # classes = char_class.Char_class.get_all()
    classes = char_class.Char_class.get_all()
    races = char_race.Char_race.get_all()
    backgrounds = char_background.Char_Background.get_all()
    alignment = json.dumps(cs_lib.cs_lib['alignment_def'])
    
    # pprint(classes, indent= 3, depth=5)
    # print("classes are",classes)
    return render_template("new_character.html", alignment = alignment, backgrounds = backgrounds, races = races, classes=classes, user = logged_in_user)

    


# @app.route("/character_creation", methods=['POST'])
# def create_character():
    
    
@app.route('/new_character_part2', methods=['POST'])
def newCharacter_part2():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    # logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n___Character form data", request.form)
    # mods = {
    #     "str" : math.floor((int(request.form["str"]) - 10)/2),
    #     "dex" : math.floor((int(request.form["dex"]) - 10)/2),
    #     "con" : math.floor((int(request.form["con"]) - 10)/2),
    #     "int" : math.floor((int(request.form["int"]) - 10)/2),
    #     "wis" : math.floor((int(request.form["wis"]) - 10)/2),
    #     "cha" : math.floor((int(request.form["cha"]) - 10)/2)        
    # }

    
    data={
        "user_id" : session['user_id'],
        "char_name" : request.form["char_name"],
        "char_race" : request.form["char_race"],
        "char_class" : request.form["char_class"],
        "char_background" : request.form["char_background"],
        "char_alignment" : request.form["char_alignment"],
        "char_level" : 1,
        "prof_bonus" : 2,
        "inspiration" : 0
    }
    session['character']= data
    #     "ac_class" : 10,
    #     "initiative" : mods["dex"],
    #     "speed" : 30,
    #     "maximum_hp" : 10,
    #     "current_hp" : 10,
    #     "temp_hp" : 0,
    #     "hit_dice_total" : 1,
    #     "hit_dice" : 4,
    #     "death_save_successes" : 0,
    #     "death_save_failures" : 0,
    #     "attack_or_spell_id" : None,
    #     "equipment_list" : None,
    #     "features_and_traits" : None,
    #     "owner_name" : logged_in_user.first_name,
    #     "experience_points" : 0
    # }

    logged_in_user =user.User.get_by_id(session["user_id"])
    a_class = char_class.Char_class.get_class_by_id(int(request.form["char_class"]))
    a_race = char_race.Char_race.get_char_race_by_id(int(request.form["char_race"]))
    a_background = char_background.Char_Background.get_char_background_by_id(int(request.form['char_background']))
    char_dict = cs_lib.cs_lib['char_dict']
    
    skill_profs = []
    for skill in a_background:
        if skill not in skill_profs:
            skill_profs.append(skill)
        
    
    
    
    
    # print("\n ___ session['character']___", session['character'])
    return  render_template("add_character_2.html", a_race = a_race, a_background = a_background, char_dict= char_dict, a_class = a_class, user = logged_in_user)

@app.route("/export_char/<int:id>") 
def export_char(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    char = character.Character.get_character_by_id(id)
    creator = user.User.get_by_id(char.user_id)
    char_dict = character.char_dict
    return render_template("Character_sheet.html", character = char, char_dict=char_dict, user = logged_in_user, creator=creator)

@app.route("/edit_char/<int:id>")
def edit_character(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    char = character.Character.get_character_by_id(id)
    char_dict = character.char_dict
    return render_template("edit_character.html", character= char, char_dict=char_dict, user = logged_in_user)

@app.route("/update_char/<int:id>",  methods=['POST'])
def update_char(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    # print("\n___Character form data", request.form)
    mods = {
        "str" : math.floor((int(request.form["str"]) - 10)/2),
        "dex" : math.floor((int(request.form["dex"]) - 10)/2),
        "con" : math.floor((int(request.form["con"]) - 10)/2),
        "int" : math.floor((int(request.form["int"]) - 10)/2),
        "wis" : math.floor((int(request.form["wis"]) - 10)/2),
        "cha" : math.floor((int(request.form["cha"]) - 10)/2)        
    }
    
    # charact_class = char_class.Char_class.get_class_by_id(request.form['char_class'])
    
    data={
        "id" : int(request.form["id"]),
        "char_name" : request.form["char_name"],
        "char_race" : request.form["char_race"],
        "char_class" : request.form["char_class"],
        # "char_class" : charact_class.name + " " + str(charact_class.id),
        "char_background" : request.form["char_background"],
        "char_alignment" : request.form["char_alignment"],
        "personality_traits" : request.form["personality_traits"],
        "ideals" : request.form["ideal"],
        "bonds" : request.form["bond"],
        "flaws" : request.form["flaw"],
        "char_level" : 1,
        "prof_bonus" : 2,
        "inspiration" : 0,
        "ac_class" : 10,
        "initiative" : mods["dex"],
        "speed" : 30,
        "maximum_hp" : 10,
        "current_hp" : 10,
        "temp_hp" : 0,
        "hit_dice_total" : 1,
        "hit_dice" : 4,
        "death_save_successes" : 0,
        "death_save_failures" : 0,
        "attack_or_spell_id" : None,
        "equipment_list" : None,
        "features_and_traits" : None,
        "owner_name" : "Dan",
        "experience_points" : 0
    }

    
    prof_dict ={
        "savs" : 
            ["str_sav_prof",
            "dex_sav_prof",
            "con_sav_prof",
            "int_sav_prof",
            "wis_sav_prof",
            "cha_sav_prof"
            ],
        "skills" : 
            ["acrobatics_prof",
            "animal_handling_prof",
            "arcana_prof",
            "athletics_prof",
            "deception_prof",
            "history_prof",
            "insight_prof",
            "intimidation_prof",
            "investigation_prof",
            "medicine_prof",
            "nature_prof",
            "perception_prof",
            "performance_prof",
            "persuasion_prof",
            "religion_prof",
            "sleight_of_hand_prof",
            "stealth_prof",
            "survival_prof"],
        "lang" :
            ["common_lang",
            "dwarvish_lang",
            "Elvish_lang",
            "giant_lang",
            "gnomish_lang",
            "goblin_lang",
            "halfling_lang",
            "orc_lang",
            "abyssal_lang",
            "celestial_lang",
            "draconic_lang",
            "deepspeech_lang",
            "infernal_lang",
            "primordial_lang",
            "sylvan_lang",
            "undercommon_lang"]
    }
    # {"lang": {}, "savs": {"dex_sav_prof": "prof", "int_sav_prof": "prof"}, "skills": {"nature_prof": "prof", "insight_prof": "prof", "stealth_prof": "prof", "investigation_prof": "prof"}}
    proficiencies ={}
    for prof_section in prof_dict:
        proficiencies[prof_section] = {}
        
        for prof in prof_dict[prof_section]:
            # print(f"prof: {prof} in {prof_section}")
            
            if prof in request.form:
                proficiencies[prof_section][prof] = request.form[prof]
    
    # print("\n___Character_con proficiencies___ ->",proficiencies)
    
    
    attributes = {
        "str" : [request.form["str"], mods["str"]],
        "dex" : [request.form["dex"], mods["dex"]],
        "con" : [request.form["con"], mods["con"]],
        "int" : [request.form["int"], mods["int"]],
        "wis" : [request.form["wis"], mods["wis"]],
        "cha" : [request.form["cha"], mods["cha"]]
    }
    
    savs ={
        "str_sav_mod" : mods["str"],
        "dex_sav_mod" : mods["dex"],
        "con_sav_mod" : mods["con"],
        "int_sav_mod" : mods["int"],
        "wis_sav_mod" : mods["wis"],
        "cha_sav_mod" : mods["cha"]
    }
    
    skills = {
        "acrobatics_mod" : mods["str"],
        "animal_handling_mod" : mods["wis"],
        "arcana_mod" : mods["int"],
        "athletics_mod" : mods["str"],
        "deception_mod" : mods["cha"],
        "history_mod" : mods["int"],
        "insight_mod" : mods["wis"],
        "intimidation_mod" : mods["cha"],
        "investigation_mod" : mods["int"],
        "medicine_mod" : mods["wis"],
        "nature_mod" : mods["int"],
        "perception_mod" : mods["wis"],
        "performance_mod" : mods["cha"],
        "persuasion_mod" : mods["cha"],
        "religion_mod" : mods["int"],
        "sleight_of_hand_mod" : mods["dex"],
        "stealth_mod" : mods["dex"],
        "survival_mod" : mods["wis"]
    }
    
    coin = {"plat" : 0, "gold" : 0, "silver" : 0, "copper" : 0, "elec" : 0}
    
    
    if 'perception_prof' in request.form:
        data["passive_wisdom"] = math.floor((int(request.form["wis"]) - 10)/2) + 10 + 2
    else:
        data["passive_wisdom"] = math.floor((int(request.form["wis"]) - 10)/2) + 10
        
    data['attributes'] = json.dumps(attributes)
    data['proficiencies'] = json.dumps(proficiencies)
    data['savs'] = json.dumps(savs)
    data['skills'] = json.dumps(skills)
    data['coin'] = json.dumps(coin)
    
    # print("\n___Update Character___")
    character.Character.update(data)
    
    return redirect("/dashboard")

@app.route("/delete_char/<int:id>")
def delete_char(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    character.Character.delete(id)
    return redirect("/dashboard")
    