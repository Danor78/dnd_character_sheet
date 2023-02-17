from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import char_class
from flask_app.controllers import main_con
from flask_app.models import char_background
from flask_app.models import item
from flask_app.models import user
from flask_app.models.cs_lib import cs_lib

from pprint import pprint
import json



@app.route("/new_background")
def new_background():
    loggedin_user = user.User.get_by_id(session['user_id'])
    tools = item.Item.get_items_by_type('tools')
    bkgrnd_prof = {
        "skill_prof" : cs_lib['skill_prof'],
        "tool_type" : cs_lib['tool_type'],
        "lang_prof" : cs_lib['lang_prof']
    }
    descriptions_num = 0
    return render_template("new_background.html",descriptions_num = descriptions_num, tools = tools, bkgrnd_prof = bkgrnd_prof, user = loggedin_user)

@app.route('/create_background', methods = ['POST'])
def create_background():
    data = {
        "name" : request.form['name'],
        "equipment" : request.form['equipment'],
        "suggested_char" : request.form['suggested_char'],
        "user_id" : session['user_id']
    }
    
    bkgrnd_prof = {
        "skill_prof" : cs_lib['skill_prof'],
        "tool_type" : cs_lib['tool_type'],
        "lang_prof" : cs_lib['lang_prof']
    }
    
    tool_prof = {}
    tool_prof['type'] = request.form['tool_type']
    tool_prof['tools'] = []
    for i in range(1,4):
        tool = "tool_" + str(i)
        if tool in request.form:
            if request.form[tool] != "null":
                tool_prof['tools'].append(request.form[tool])
            else:
                tool_prof['tools'].append("0")
        else:
            tool_prof['tools'].append("0")
    
    data['tool_prof'] = json.dumps(tool_prof)
    
    lang_prof = {}
    lang_prof['number_of'] = request.form['num_lang']
    lang_prof['lang_prof'] = []
    for lang in bkgrnd_prof['lang_prof']:
        if lang in request.form:
            lang_prof['lang_prof'].append(lang)
    data['lang_prof'] = json.dumps(lang_prof)
    
    features = {}
    features['feature_name'] = request.form['feature_name']
    features['feature_desc'] = request.form['feature_desc']
    data['features'] = json.dumps(features)
    
    skill_prof = []
    for bkgrnd in bkgrnd_prof['skill_prof']:
        if bkgrnd in request.form:
            skill_prof.append(bkgrnd)
    data['skill_prof'] = json.dumps(skill_prof)
    
    descriptions = {}

    descriptions['description'] = request.form['description']
    nums = request.form['description_num']
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
    
    per_trait = {}
    for i in range(1,9):
        trait = "per_trait_" + str(i)
        per_trait[trait] = request.form[trait]
    data['personality_traits'] = json.dumps(per_trait)
    
    per_ideal = {}
    for i in range(1,7):
        ideal = "ideal_" + str(i)
        per_ideal[ideal] = request.form[ideal]
    data['ideals'] = json.dumps(per_ideal)
    
    per_bond = {}
    for i in range(1,7):
        bond = "bond_" + str(i)
        per_bond[bond] = request.form[bond]
    data['bonds'] = json.dumps(per_bond)
    
    per_flaw = {}
    for i in range(1,7):
        flaw = "flaw_" + str(i)
        per_flaw[flaw] = request.form[flaw]
    data['flaws'] = json.dumps(per_flaw)
    
    # print("\n__Background request.form__", request.form)
    char_background.Char_Background.save(data)
    
    return redirect('/dashboard')

@app.route("/edit_background/<int:id>")
def edit_background(id):
    loggedin_user = user.User.get_by_id(session['user_id'])
    tools = item.Item.get_items_by_type('tools')
    
    bkgrnd_prof = {
        "skill_prof" : cs_lib['skill_prof'],
        "tool_type" : cs_lib['tool_type'],
        "lang_prof" : cs_lib['lang_prof']
    }
    
    background = char_background.Char_Background.get_char_background_by_id(id)
    return render_template("edit_background.html", background = background, tools = tools, 
                        bkgrnd_prof = bkgrnd_prof, user = loggedin_user)

@app.route("/update_background", methods = ['POST'])
def update_background():
    data = {
        "id" : request.form['id'],
        "name" : request.form['name'],
        "equipment" : request.form['equipment'],
        "suggested_char" : request.form['suggested_char'],
        "user_id" : session['user_id']
    }
    tool_prof = {}
    tool_prof['type'] = request.form['tool_type']
    tool_prof['tools'] = []
    for i in range(1,4):
        tool = "tool_" + str(i)
        if tool in request.form:
            if request.form[tool] != "null":
                tool_prof['tools'].append(request.form[tool])
            else:
                tool_prof['tools'].append("0")
        else:
            tool_prof['tools'].append("0")
    
    data['tool_prof'] = json.dumps(tool_prof)
    
    lang_prof = {}
    lang_prof['number_of'] = request.form['num_lang']
    lang_prof['lang_prof'] = []
    for lang in char_background.bkgrnd_prof['lang_prof']:
        if lang in request.form:
            lang_prof['lang_prof'].append(lang)
    data['lang_prof'] = json.dumps(lang_prof)
    
    features = {}
    features['feature_name'] = request.form['feature_name']
    features['feature_desc'] = request.form['feature_desc']
    data['features'] = json.dumps(features)
    
    skill_prof = []
    for bkgrnd in char_background.bkgrnd_prof['skill_prof']:
        if bkgrnd in request.form:
            skill_prof.append(bkgrnd)
    data['skill_prof'] = json.dumps(skill_prof)
    
    descriptions = {}

    descriptions['description'] = request.form['description']
    nums = request.form['description_num']
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
    
    per_trait = {}
    for i in range(1,9):
        trait = "per_trait_" + str(i)
        per_trait[trait] = request.form[trait]
    data['personality_traits'] = json.dumps(per_trait)
    
    per_ideal = {}
    for i in range(1,7):
        ideal = "ideal_" + str(i)
        per_ideal[ideal] = request.form[ideal]
    data['ideals'] = json.dumps(per_ideal)
    
    per_bond = {}
    for i in range(1,7):
        bond = "bond_" + str(i)
        per_bond[bond] = request.form[bond]
    data['bonds'] = json.dumps(per_bond)
    
    per_flaw = {}
    for i in range(1,7):
        flaw = "flaw_" + str(i)
        per_flaw[flaw] = request.form[flaw]
    data['flaws'] = json.dumps(per_flaw)
    
    char_background.Char_Background.update(data)
    
    return redirect('/dashboard')

@app.route('/show_background/<int:id>/<string:nav>')
def show_background(id,nav):
    loggedin_user = user.User.get_by_id(session['user_id'])
    tools = item.Item.get_items_by_type('tools')
    bckgrnd = char_background.Char_Background.get_char_background_by_id(id)
    
    bkgrnd_prof = {
        "skill_prof" : cs_lib['skill_prof'],
        "tool_type" : cs_lib['tool_type'],
        "lang_prof" : cs_lib['lang_prof']
    }
    
    
    tmp = ""
    for skill in bckgrnd.skill_prof:
        tmp += main_con.no_prof(skill) + ' / '
    bckgrnd.skill_prof = tmp
    
    tmp = ""
    if bckgrnd.tool_prof['type'] != "null":
        tmp = bkgrnd_prof['tool_type'][bckgrnd.tool_prof['type']]
    bckgrnd.tool_prof['type'] = tmp
    
    tmp = ""
    for id in bckgrnd.tool_prof['tools']:
        if id != '0':
            tmp += item.Item.get_item_by_id(int(id)).name + ' / '
    bckgrnd.tool_prof['tools'] = tmp
    
    tmp = ""
    if bckgrnd.lang_prof['number_of'] != '0':
        tmp = bckgrnd.lang_prof['number_of'] + " of your choice."
    bckgrnd.lang_prof['number_of'] = tmp
    
    tmp = ""
    if bckgrnd.lang_prof['lang_prof']:
            tmp += "Proficient Languages: "
            for lang in bckgrnd.lang_prof['lang_prof']:
                tmp += bkgrnd_prof['lang_prof'][lang] + " / "
    bckgrnd.lang_prof['lang_prof'] = tmp
    return render_template('display_background.html', nav = nav, user = loggedin_user, bkgrnd_prof = bkgrnd_prof, tools = tools, background = bckgrnd)
