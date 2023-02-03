
from flask_app.models import item
from flask_app.config.mysqlconnection import connectToMySQL


armor_type = {
    "heavy_armor" : "Heavy Armor",
    "medium_armor" : "Medium Armor",
    "light_armor" : "Light Armor",
    "shield" : "Shield"
}

body_part ={
    "chest" : "chest",
    "head" : "head",
    "legs" : "legs",
    "feet" : "feet",
    "forearms" : "forearms",
    "finger" : "finger"
}

stealth_prop ={
    "none" : "None",
    "advantage" : "Advantage",
    "disadvantage" : "Disadvantage"
}

class Armor(): 
    DB = "character_sheet"
    
    def __init__(self, data): 
        self.id = data["id"]
        self.armor_type = data["armor_type"]
        self.body_part = data['body_part']
        self.armor_AC = data["armor_AC"]
        self.magical_mod = data['magical_mod']
        self.str_req = data["str_req"]
        self.stealth_property = data["stealth_property"]
        

    @classmethod
    def populate_item_data(cls,data): # find and populate the super() dictionary of values
        item_data = {
            "name" : data["name"],
            "type" : data["type"],
            "cost" : data["cost"],
            "weight" : data["weight"],
        }
        return item_data


    @classmethod
    def get_all(cls):
        print("")
        print("__Armor Class Method__")
        query = "SELECT * FROM armors;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        print(f"Results are: {results}")
        # Create an empty list to append our instances of friends
        all_armor = []
        # Iterate over the db results and create instances of friends with cls.
        for piece_of_armor in results:
            all_armor.append( cls(piece_of_armor) )
        print(f"List of dojo[] is; {all_armor}")
        return all_armor

    
    @classmethod
    def get_armor_by_id(cls,id):
        data = {"id" : id}
        query = "SELECT * FROM armors WHERE id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("")
        print(f"The Result is: {result}")
        # Create an empty list to append our instances of friends
        armor_item = cls(result[0])
        print("")
        print(f"The a_item is: {armor_item}")
        # Iterate over the db results and create instances of friends with cls.
        return armor_item
    
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__Armor Save Method__")
        print(f"data: {data}")
        query = "INSERT INTO armors ( armor_type, body_part, armor_AC, magical_mod, str_req, stealth_property, created_at, updated_at) VALUES ( %(armor_type)s, %(body_part)s, %(armor_AC)s, %(magical_mod)s, %(str_req)s, %(stealth_property)s, NOW(), NOW() );"
        # data is a dictionary that will be passed into the save method from server.py,
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = "UPDATE items SET armor_type=%(armor_type)s, body_part=%(body_part)s, armor_AC=%(armor_AC)s, magical_mod=%(magical_mod)s, str_req=%(str_req)s, stealth_property=%(stealth_property)s, WHERE id=%(armor_id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = "DELETE FROM armors where id=%(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )

    @classmethod
    def validate_armor(cls,data):
        is_valid = True
        
        if not item.Item.validate_item(data): # if not (false)
            print("\n ____Weapon con item validation FAILED____")
            is_valid = False
        
        if 'amor_type' not in data or data['weapon_type'] == "":
            print("____Armor type FAILED____")
            flash("Please Select a armor Type","armor_input")
            is_valid = False
        
        if 'body_part' not in data or data['body_part'] == "":
            print("____armor body_part FAILED____")
            flash("Please Select a body part to be equipped","armor_input")
            is_valid = False
        
        if 'stealth_property' not in data or data['stealth_property'] == "":
            print("____armor stealth_property FAILED____")
            flash("Please Select a stealth property for the weapon","armor_input")
            is_valid = False
        
        return is_valid

    def set_armor_name(self, name):  # easy straight up value setting if needed
        self.armor_name = name
    
    def set_armor_AC(self, AC):  # easy straight up value setting if needed
        self.armor_AC = AC
    
    def set_str_req(self, req):  # easy straight up value setting if needed
        self.str_req = req
    
    def set_armor_stealth_prop(self,prop):  # easy straight up value setting if needed
        self.armor_stealth_property = prop
    
    def does_hit(self, hit): #a function to see of that attack roll 'hit' meets or beats the armor AC.
        if hit >= self.armor_AC:
            return True
        else:
            return False
    
    def armor_info(self): # display variables
        print("")
        print(f"Armor Type: {self.armor_type}")
        print(f"Equipted body bart: {self.body_part}")
        print(f"Armor AC: {self.armor_AC}")
        print(f"Armor Strength Requirement: {self.str_req}")
        print(f"Armor Stealth Property: {self.armor_stealth_property}")
        
