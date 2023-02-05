from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import char_class
from flask_app.models import item
from flask_app.models import user

from pprint import pprint

import json

@app.route("/new_class")
def new_class():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    descriptions_num = 1
    features_num = 1
    start_equip = 1
    items = item.Item.get_all_by_order('type')
    return render_template("new_class.html", descriptions_num = descriptions_num, features_num = features_num, start_equip=start_equip, items=items, user=logged_in_user)

@app.route("/create_class", methods=['POST'])
def create_class():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    print("\n___Class Request.form", request.form)
    data = {
        "user_id" : logged_in_user.id,
        "name" : request.form["name"],
        "hit_die" : request.form["hit_die"],
        "primary_ability" : None,
        "sub_classes" : ""
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
            "undercommon_lang"],
        "armor_prof" : [
            "heavy_armor_prof",
            "medium_armor_prof",
            "light_armor_prof"
            ],
        "weapon_prof" : [
            "simple_weapons_prof",
            "martial_weapons_prof",
            "sword_prof",
            "axe_prof",
            "bow_prof",
            "pole_prof",
            "warhammer_prof"
        ]
    }
    sav_prof ={}
    for prof in prof_dict["savs"]:
        if prof in request.form:
            sav_prof[prof] = request.form[prof]
    data['sav_prof'] = json.dumps(sav_prof)
    
    skill_prof = []
    skill_prof.append(request.form['skill_prof_num'])
    for prof in prof_dict["skills"]:
        if prof in request.form:
            skill_prof.append(prof)
    data['skill_prof'] = json.dumps(skill_prof)
    
    
    armor_weapon_prof = []
    for prof in prof_dict["armor_weapon_prof"]:
        if prof in request.form:
            armor_weapon_prof.append(prof)
    data['armor_weapon_prof'] = json.dumps(armor_weapon_prof)
    
    descriptions = {}
    nums = request.form['descript_num']
    print("\n___Desc nums is___",type(nums))
    descriptions['number_of'] = int(nums)
    tnums = int(nums) + 1
    for num in range(1,tnums):
        heading = "desc_heading_" + str(num)
        descript = "description_" + str(num)
        if heading in request.form:
            descriptions[heading] = request.form[heading]
        if descript in request.form:
            descriptions[descript] = request.form[descript]
    
    data['description'] = json.dumps(descriptions)
    
    features = {}
    nums = request.form['feature_num']
    features['number_of'] = nums
    tnums = int(nums) + 1
    for num in range(1,tnums):
        name = "feature_name_" + str(num)
        lvl = "feature_level_" + str(num)
        desc = "feature_descript_" + str(num)
        print("\n___for loop___",num,name,lvl,desc)
        if name in request.form:
            features[name] = request.form[name]
        if lvl in request.form:
            features[lvl] = request.form[lvl]
        if desc in request.form:
            features[desc] = request.form[desc]
            
    data['features'] = json.dumps(features)
    
    start_equipment = {}
    for i in range(1,5):
        option= 'option' + str(i)
        print("\n___option___", option)
        start_equipment[option] = {}
        for j in range(1,4):
            opt = "opt" + str(i) + "_start" + str(j)
            print("\n___opt___", opt)
            if opt in request.form:
                start_equipment[option][opt] = request.form[opt]
    
    start_equipment['default']={}
    for i in range(1,4):
        opt = "def_start" + str(i)
        if opt in request.form:
            start_equipment['default'][opt] = request.form[opt]
                
    print("\n__start_equipment__",start_equipment)
    data['start_equipment'] = json.dumps(start_equipment)
    # print("\n__Json start_equipment__", data['start_equipment'])
    print("\n__Json start_equipment__", json.dumps(start_equipment))
    
    
    print("\n____Class Data___",data)
    print("\n____Pretty Class Data___")
    pprint(data, depth=2, indent=4)
    
    char_class.Char_class.save(data)
    
    return redirect("/dashboard")

@app.route("/edit_class/<int:id>")
def edit_class(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    descriptions_num = 1
    features_num = 1
    start_equip = 1
    items = item.Item.get_all_by_order('type')
    a_class = char_class.Char_class.get_class_by_id(id)
    a_class.description['number_of'] = int(a_class.description['number_of'])
    a_class.features['number_of'] = int(a_class.features['number_of'])
    
    edit_var = {
        "hit_die": [ 4,6,8,10,12],
        "savs" : {
            "str_sav_prof" : "Strength Save",
            "dex_sav_prof" : "Dexterity Save",
            "con_sav_prof" : "Constitution Save",
            "int_sav_prof" : "Intelligence Save",
            "wis_sav_prof" : "Wisdom Save",
            "cha_sav_prof" : "Charisma Save"
            },
        "skills" : {
            "acrobatics_prof" : "Acrobatics Proficiency",
            "animal_handling_prof" : "Animal Handling Proficiency",
            "arcana_prof" : "Arcana Proficiency",
            "athletics_prof" : "Athletics Proficiency",
            "deception_prof" : "Deception Proficiency",
            "history_prof" : "History Proficiency",
            "insight_prof" : "Insight Proficiency",
            "intimidation_prof" : "Intimidation Proficiency",
            "investigation_prof" : "Investigation Proficiency",
            "medicine_prof" : "Medicine Proficiency",
            "nature_prof" : "Nature Proficiency",
            "perception_prof" : "Perception Proficiency",
            "performance_prof" : "Performance Proficiency",
            "persuasion_prof" : "Persuasion Proficiency",
            "religion_prof" : "Religion Proficiency",
            "sleight_of_hand_prof" : "Sleight of Hand Proficiency",
            "stealth_prof" : "Stealth Proficiency",
            "survival_prof" : "Survival Proficiency",
            },
        "armor_prof" : {
            "heavy_armor_prof" : "Heavy Armor Proficiencies",
            "medium_armor_prof" : "Medium Armor Proficiencies",
            "light_armor_prof" : "Light Armor Proficiencies"
            },
        "weapon_prof" : {
            "simple_weapons_prof" : "Simple Weapons Proficiency",
            "martial_weapons_prof" : "Martial Weapons Proficiency",
            "sword_prof" : "Sword Proficiency",
            "axe_prof" : "Axe Proficiency",
            "bow_prof" : "Bow Proficiency",
            "pole_prof" : "Pole Arm Proficiency",
            "warhammer_prof" : "War Hammer Proficiency"
            },
        "starting_equip" : {
            "simple_weapon" : "Any Simple Weapon",
            "martial_weapon" : "Any Martial Weapon"
        }
    }

    print("\n__ a_class.start_equipment['option1'] = ", a_class.start_equipment['option1']['opt1_start1'])

    return render_template("edit_class.html", edit_var = edit_var, a_class = a_class, descriptions_num = descriptions_num, features_num = features_num, start_equip=start_equip, items=items, user=logged_in_user)

@app.route("/update_class/<int:id>", methods=['POST'])
def update_class(id):
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    # print("\n___Class Request.form", request.form)
    data = {
        "user_id" : logged_in_user.id,
        "name" : request.form["name"],
        "hit_die" : request.form["hit_die"],
        "primary_ability" : None,
        "sub_classes" : ""
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
            "undercommon_lang"],
        "armor_prof" : [
            "heavy_armor_prof",
            "medium_armor_prof",
            "light_armor_prof"
            ],
        "weapon_prof" : [
            "simple_weapons_prof",
            "martial_weapons_prof",
            "sword_prof",
            "axe_prof",
            "bow_prof",
            "pole_prof",
            "warhammer_prof"
        ]
    }
    sav_prof ={}
    for prof in prof_dict["savs"]:
        if prof in request.form:
            sav_prof[prof] = request.form[prof]
    data['sav_prof'] = json.dumps(sav_prof)
    
    skill_prof = []
    skill_prof.append(request.form['skill_prof_num'])
    for prof in prof_dict["skills"]:
        if prof in request.form:
            skill_prof.append(prof)
    data['skill_prof'] = json.dumps(skill_prof)
    
    
    armor_weapon_prof = []
    for prof in prof_dict["weapon_prof"]:
        if prof in request.form:
            armor_weapon_prof.append(prof)
    for prof in prof_dict["armor_prof"]:
        if prof in request.form:
            armor_weapon_prof.append(prof)
    data['armor_weapon_prof'] = json.dumps(armor_weapon_prof)
    
    descriptions = {}
    nums = request.form['descript_num']
    # print("\n___Desc nums is___",type(nums))
    descriptions['number_of'] = int(nums)
    tnums = int(nums) + 1
    for num in range(1,tnums):
        heading = "desc_heading_" + str(num)
        descript = "description_" + str(num)
        if heading in request.form:
            descriptions[heading] = request.form[heading]
        if descript in request.form:
            descriptions[descript] = request.form[descript]
    
    data['description'] = json.dumps(descriptions)
    
    features = {}
    nums = request.form['feature_num']
    features['number_of'] = nums
    tnums = int(nums) + 1
    for num in range(1,tnums):
        name = "feature_name_" + str(num)
        lvl = "feature_level_" + str(num)
        desc = "feature_descript_" + str(num)
        # print("\n___for loop___",num,name,lvl,desc)
        if name in request.form:
            features[name] = request.form[name]
        if lvl in request.form:
            features[lvl] = request.form[lvl]
        if desc in request.form:
            features[desc] = request.form[desc]
            
    data['features'] = json.dumps(features)
    
    start_equipment = {}
    for i in range(1,5):
        option= 'option' + str(i)
        # print("\n___option___", option)
        start_equipment[option] = {}
        for j in range(1,4):
            opt = "opt" + str(i) + "_start" + str(j)
            # print("\n___opt___", opt)
            if opt in request.form:
                start_equipment[option][opt] = request.form[opt]
    
    start_equipment['default']={}
    for i in range(1,4):
        opt = "def_start" + str(i)
        if opt in request.form:
            start_equipment['default'][opt] = request.form[opt]
                
    # print("\n__start_equipment__",start_equipment)
    data['start_equipment'] = json.dumps(start_equipment)
    data["id"] = id
    # print("\n__Json start_equipment__", data['start_equipment'])
    # print("\n__Json start_equipment__", json.dumps(start_equipment))
    
    
    # print("\n____Class Data___",data)
    # print("\n____Pretty Class Data___")
    # pprint(data, depth=2, indent=4)
    
    char_class.Char_class.update(data)
    
    return redirect("/dashboard")