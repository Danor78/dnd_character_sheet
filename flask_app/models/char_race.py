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


class Char_race:
    DB="character_sheet"
    table_data = ["char_races", "name", "description", "racial_traits", "racial_attrib", "speed", "created_at", "updated_at", "user_id"]
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = json.loads(data['description'])
        self.racial_traits = json.loads(data['racial_traits'])
        self.racial_attrib = json.loads(data['description'])
        self.speed = data['speed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    
    @classmethod
    def get_all(cls):
        print("\n__char_races get_all Method__")
        query = f"SELECT * FROM {cls.table_data[0]}; "
        print("\n___Get all query", query)
        results = connectToMySQL(cls.DB).query_db(query)

        all_char_races = []
        for dict_row in results:
            a_char_race = cls(dict_row)
            a_char_race.user = user.User.get_by_id(dict_row['user_id'])
            # all_char_races.append( cls(dict_row) )
            all_char_races.append(a_char_race)
                
        return all_char_races
    
    @classmethod
    def dict_get_all(cls):
        print("\n__classes get_all Method__")
        query = f"SELECT * FROM {cls.table_data[0]}; "
        print("\n___Get all query", query)
        results = connectToMySQL(cls.DB).query_db(query)
        
        for row in results:
            row['description'] = json.loads(row['description'])
            row['racial_traits'] = json.loads(row['sav_prof'])

        return results
    
    @classmethod
    def get_char_race_by_id(cls,id):
        print("\n____Get char_race by Id method____")
        data = {"id" : id}
        query = f"SELECT * FROM {cls.table_data[0]} WHERE {cls.table_data[0]}.id=%(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("")
        print(f"The Result is: {result}")
        a_char_race = cls(result[0])
        
        print("")
        return a_char_race
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__Class Save Method__")
        pprint(data, depth=2, indent=4)
        query = query_gen.save_query(cls.table_data)
        print("\n__Save query__",query)
        
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = query_gen.update_query(cls.table_data)
    
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = F"DELETE FROM {cls.table_data[0]} WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db( query, data )
    