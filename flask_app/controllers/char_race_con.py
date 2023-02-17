from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import char_class
from flask_app.models import char_race
from flask_app.models import item
from flask_app.models import user
from flask_app.models import weapon
from flask_app.models.cs_lib import cs_lib

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
    weapons = sorted(cs_lib['weapon_type'])
    weaponType_list = {}
    for type in weapons:
        weaponType_list[type] = cs_lib['weapon_type'][type]
    
    armorType_list = cs_lib['armor_prof']
    
    race_lang = cs_lib['lang_prof']
    
    skill_prof = cs_lib['skill_prof']
    
    source = cs_lib['source']
    
    
    
    return render_template("new_race.html", source = source, skill_prof = skill_prof, race_lang = race_lang, armor = armorType_list, weapons = weaponType_list, descriptions_num = descriptions_num,
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
    
    # race_lang = char_race.race_prof['lang_prof']
    
    racial_traits['lang_prof'] = {}
    for i in range(1,4):
        lang_prof = "lang_prof_" + str(i)
        if lang_prof in request.form:
            if request.form[lang_prof] != 'null' and request.form[lang_prof] != "":
                racial_traits['lang_prof'][lang_prof] = request.form[lang_prof]
    
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
    
    racial_profs = {
        "skill_prof" : [],
        "weapon_profs" : {
            "weaponTypeProf" : [],
            "weapon_prof" : {}
            },
        "armor_prof" : {}
    }
    for prof in cs_lib['skill_prof']:
        if prof in request.form:
            if request.form[prof] == 'on':
                racial_profs['skill_prof'].append(prof)
            elif request.form[prof] != 'null':
                racial_profs['skill_prof'].append(request.form[prof])
    
    for prof in cs_lib['weapon_prof']:
        if prof in request.form:
            if request.form[prof] == 'on':
                racial_profs['weapon_profs']['weaponTypeProf'].append(prof)
            elif request.form[prof] != 'null':
                racial_profs['weapon_profs']['weaponTypeProf'].append(prof)
    
    for choice in cs_lib['weap_choice']:
        if choice in request.form:
            if request.form[choice] != 'null':
                racial_profs['weapon_profs']['weapon_prof'][choice] = request.form[choice]
            else:
                racial_profs['weapon_profs']['weapon_prof'][choice] = 'null'
    
    for choice in cs_lib['armor_choice']:
        if choice in request.form:
            if request.form[choice] != 'null':
                racial_profs['armor_prof'][choice] = request.form[choice]
            else:
                racial_profs['armor_prof'][choice] = 'null'
    

    data['racial_profs'] = json.dumps(racial_profs)
    data['source'] = request.form['source']
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
    weapons = sorted(cs_lib['weapon_type'])
    weaponType_list = {}
    for type in weapons:
        weaponType_list[type] = cs_lib['weapon_type'][type]
    
    a_race = char_race.Char_race.get_char_race_by_id(id)
    
    edit_var = {
        "attrib" : cs_lib['attrib'],
        "weapon_prof" : cs_lib['weapon_prof'],
        "lang_prof" : cs_lib['lang_prof'],
        "skill_prof" : cs_lib['skill_prof'],
        "source" : cs_lib['source'],
        "armor_prof" : cs_lib['armor_prof'],
        "weapon_type" : weaponType_list,
    }
    
    return render_template("edit_race.html", edit_var = edit_var, a_race = a_race, user=logged_in_user)

@app.route('/update_race', methods=['POST'])
def update_race():
    if "user_id" not in session:
        print("\n___<<< User not logged in >>>___")
        return redirect("/")
    logged_in_user =user.User.get_by_id(session["user_id"])
    # print("\n___Race Request.form")
    # pprint(request.form, indent=3, depth=3)
    data = {
        "id" : request.form["id"],
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
    racial_traits['number_of'] = int(nums)
    tnums = int(nums) + 1
    for num in range(1,tnums):
        heading = "racial_heading_" + str(num)
        racial_trait = "racial_trait_" + str(num)
        if heading in request.form:
            racial_traits[heading] = request.form[heading]
        if racial_trait in request.form:
            racial_traits[racial_trait] = request.form[racial_trait]
    
    racial_traits['lang_prof'] = {}
    for i in range(1,4):
        lang_prof = "lang_prof_" + str(i)
        if lang_prof in request.form:
            if request.form[lang_prof] != 'null' and request.form[lang_prof] != "":
                racial_traits['lang_prof'][lang_prof] = request.form[lang_prof]
    
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
    
    racial_profs = {
        "skill_prof" : [],
        "weapon_profs" : {
            "weaponTypeProf" : [],
            "weapon_prof" : {}
            },
        "armor_prof" : {}
    }
    for prof in cs_lib['skill_prof']:
        if prof in request.form:
            if request.form[prof] == 'on':
                racial_profs['skill_prof'].append(prof)
            elif request.form[prof] != 'null':
                racial_profs['skill_prof'].append(request.form[prof])
    
    for prof in cs_lib['weapon_prof']:
        if prof in request.form:
            if request.form[prof] == 'on':
                racial_profs['weapon_profs']['weaponTypeProf'].append(prof)
            elif request.form[prof] != 'null':
                racial_profs['weapon_profs']['weaponTypeProf'].append(prof)
    
    for choice in cs_lib['weap_choice']:
        if choice in request.form:
            if request.form[choice] != 'null':
                racial_profs['weapon_profs']['weapon_prof'][choice] = request.form[choice]
            else:
                racial_profs['weapon_profs']['weapon_prof'][choice] = 'null'
    
    for choice in cs_lib['armor_choice']:
        if choice in request.form:
            if request.form[choice] != 'null':
                racial_profs['armor_prof'][choice] = request.form[choice]
            else:
                racial_profs['armor_prof'][choice] = 'null'
    

    data['racial_profs'] = json.dumps(racial_profs)
    data['source'] = request.form['source']
    # print("\n___racial_profs___")
    # pprint(data['racial_profs'], indent=2, depth=3)
    
    char_race.Char_race.update(data)
    
    return redirect('/dashboard')
    
@app.route("/display_race/<int:id>/<string:nav>")
def display_race(id,nav):
    a_race = char_race.Char_race.get_char_race_by_id(id)

    loggedin_user = user.User.get_by_id(session['user_id'])
    
    racial_prof = {}
    racial_prof['speed'] = a_race.speed
    
    racial_prof['attrib'] = ""
    for atb in  cs_lib['attrib']:
        if atb in a_race.racial_attrib:
            if a_race.racial_attrib[atb] != "0" and a_race.racial_attrib[atb] != "":
                racial_prof['attrib'] += atb.title() + ': +' + str(a_race.racial_attrib[atb]) + ' / '
    if racial_prof['attrib'] == "":
        racial_prof['attrib'] = "None"
    
    racial_prof['lang'] = ""
    for i in range(1,4):
        lang = "lang_prof_" + str(i)
        if lang in a_race.racial_traits['lang_prof']:
            racial_prof['lang'] += cs_lib['lang_prof'][a_race.racial_traits['lang_prof'][lang]] + ' / '
    if racial_prof['lang'] == "":
        racial_prof['lang'] = "None"
    
    racial_prof['skills'] = ""
    for skill in cs_lib['skill_prof']:
        if skill in a_race.racial_profs['skill_prof']:
            racial_prof['skills'] += cs_lib['skill_prof'][skill] + ' / '
    if racial_prof['skills'] == "":
        racial_prof['skills'] = "None"
    
    racial_prof['weapons'] = ""
    for weapon in cs_lib['weapon_prof']:
        if weapon in a_race.racial_profs['weapon_profs']['weaponTypeProf']:
            racial_prof['weapons'] += cs_lib['weapon_prof'][weapon] + ' / '
    if racial_prof['weapons'] == "":
        racial_prof['weapons'] = "None"
        
    racial_prof['weapon_profs'] = ""
    for i in range(1,5):
        weapon = "weapon_prof" + str(i)
        if weapon in a_race.racial_profs['weapon_profs']['weapon_prof'] and a_race.racial_profs['weapon_profs']['weapon_prof'][weapon] != 'null':
            racial_prof['weapon_profs'] += cs_lib['weapon_type'][a_race.racial_profs['weapon_profs']['weapon_prof'][weapon]] + ' / '
    if racial_prof['weapon_profs'] == "":
        racial_prof['weapon_profs'] = "None"
    
    racial_prof['armor_profs'] = ""
    for i in range(1,4):
        armor = "armor_prof" + str(i)
        if armor in a_race.racial_profs['armor_prof'] and a_race.racial_profs['armor_prof'][armor] != 'null':
            racial_prof['armor_profs'] += cs_lib['armor_prof'][a_race.racial_profs['armor_prof'][armor]] + ' / '
    if racial_prof['armor_profs'] == "":
        racial_prof['armor_profs'] = "None"
    
    racial_prof['source'] = cs_lib['source'][a_race.source]

    print("\n__nav is ___", nav)
    
    return render_template('display_race.html', racial_prof = racial_prof, a_race = a_race, nav = nav, user = loggedin_user)