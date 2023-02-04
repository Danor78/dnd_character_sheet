import math
import random
import json
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import armor
from flask_app.models import weapon
from flask_app.models import item
from flask_app.models import user
from flask_app.models import query_gen
from pprint import pprint



class Char_class:
    DB="character_sheet"
    table_data = ["char_classes", "name", "description", "hit_die", "primary_ability", "sav_prof", "skill_prof", "armor_weapon_prof", 
        "features", "start_equipment", "sub_classes", "created_at", "updated_at", "user_id"]
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.hit_die = data['hit_die']
        self.primary_ability = data['primary_ability']
        self.sav_prof = json.loads(data['sav_prof'])
        self.skill_prof = json.loads(data['skill_prof'])
        self.armor_weapon_prof = json.loads(data['armor_weapon_prof'])
        self.features = data['features']
        self.start_equipment = data['start_equipment']
        self.sub_classes = data['sub_classes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        print("\n__classes get_all Method__")
        query = f"SELECT * FROM {cls.table_data[0]}; "
        print("\n___Get all query", query)
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # for result in results:
            # print(f"\nResult[] is: {result}")

        # Create an empty list to append our instances of friends
        all_classes = []
        # Iterate over the db results and create instances of friends with cls.
        for dict_row in results:
            a_class = cls(dict_row)
            a_class.user = user.User.get_by_id(dict_row['user_id'])
            # all_classes.append( cls(dict_row) )
            all_classes.append(a_class)
                
        # print(f"List of item[] is; {all_classes}")
        return all_classes
        
    @classmethod
    def get_class_by_id(cls,id):
        print("\n____Get Class by Id method____")
        data = {"id" : id}
        query = f"SELECT * FROM {cls.table_data[0]} WHERE {cls.table_data[0]}.id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("")
        print(f"The Result is: {result}")
        # Create an empty list to append our instances of friends
        a_class = cls(result[0])
        
        print("")
        # Iterate over the db results and create instances of friends with cls.
        return a_class
    
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__Class Save Method__")
        # print(f"data: {data}")
        pprint(data, depth=2, indent=4)
        query = query_gen.save_query(cls.table_data)
        print("\n__Save query__",query)
        print("")
        # query = """INSERT INTO char_classes ( name, description, hit_die, primary_ability, save_prof, armor_weapon_prof, 
        # features, start_equipment, sub_classes, created_at, updated_at) 
        # VALUES ( %(name)s, %(description)s, %(hit_die)s, %(primary_ability)s, %(sav_prof)s, %(armor_weapon_prof)s, %(features)s, 
        # %(start_equipment)s, %(sub_classes)s, NOW(), NOW());
        # """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = query_gen.update_query(cls.table_data)
    
        # query = "UPDATE items SET name=%(name)s, type=%(type)s, cost=%(cost)s, weight=%(weight)s, description=%(description)s, rarity=%(rarity)s,  source=%(source)s, is_magical=%(is_magical)s, is_attunable=%(is_attunable)s, img=%(img)s, armor_id=%(armor_id)s, weapon_id=%(weapon_id)s  WHERE id=%(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = F"DELETE FROM {cls.table_data[0]} WHERE id=%(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    