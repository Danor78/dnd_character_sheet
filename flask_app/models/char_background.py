from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import armor
from flask_app.models import weapon
from flask_app.models import item
from flask_app.models import user
from flask_app.models import query_gen
from pprint import pprint
import math
import random
import json

bkgrnd_prof = {
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
    "tool_type" : {
        "artisans_tools" : "Artisan's Tools",
        "gaming_set" : "Gaming Set",
        "instrument" : "Instrument",
        "vehicle" : "Vehicle",
        "vehicle_land" : "Vehicle (Land)",
        "vehicle_water" : "Vehicle (water)"
    }
    
}


class Background:
    DB = "character_sheet"
    table_data = ["char_backgrounds", "name", "skill_prof", 
                "tool_prof", "lang_prof", "equipment", "descriptions", 
                "features", "suggested_char", "personality_traits", 
                "ideals", "bonds", "flaws", "created_at", "updated_at", 
                "user_id" ]
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.skill_prof = data['skill_prof']
        self.tool_prof = data['tool_prof']
        self.lang_prof = data['lang_prof']
        self.equipment = data['equipment']
        self.descriptions = data['descriptions']
        self.features = data['features']
        self.suggested_char = data['suggested_char']
        self.personality_traits = data['personality_traits']
        self.ideals = data['ideals']
        self.bonds = data['bonds']
        self.flaws = data['flaws']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    
    @classmethod
    def get_all(cls):
        # print("\n__char_background get_all Method__")
        query = f"SELECT * FROM {cls.table_data[0]}; "
        # print("\n___Get all query", query)
        results = connectToMySQL(cls.DB).query_db(query)

        all_char_backgrounds = []
        for dict_row in results:
            a_char_background = cls(dict_row)
            a_char_background.user = user.User.get_by_id(dict_row['user_id'])
            all_char_backgrounds.append(a_char_background)
                
        return all_char_backgrounds
    
    @classmethod
    def get_char_background_by_id(cls,id):
        print("\n____Get char_background by Id method____")
        data = {"id" : id}
        query = f"SELECT * FROM {cls.table_data[0]} WHERE {cls.table_data[0]}.id=%(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        a_char_background = cls(result[0])

        return a_char_background
    
    @classmethod
    def save(cls, data ):
        print("\n__char_background Save Method__")
        # pprint(data, depth=2, indent=4)
        query = query_gen.save_query(cls.table_data)
        # print("\n__Save query__",query)
        
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = query_gen.update_query(cls.table_data)
    
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = f"DELETE FROM {cls.table_data[0]} WHERE id=%(id)s"
        
        return connectToMySQL(cls.DB).query_db( query, data )