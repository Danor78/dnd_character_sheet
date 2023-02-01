import math
import random
from flask_app.models import item
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

weapon_type ={
    "club" : "Club",
    "dagger" : "Dagger",
    "greatclub" : "Greatclub",
    "handaxe" : "Handaxe",
    "javelin" : "Javelin",
    "light_hammer" : "Light Hammer",
    "mace" : "Mace",
    "quarterstaff" : "Quarterstaff",
    "sickle" : "Sickle",
    "spear" : "Spear",
    "unarmed_strike" : "Unarmed Strike",
    "light_crossbow" : "Light Crossbow",
    "dart" : "Dart",
    "shortbow" : "Shortbow",
    "sling" : "Sling",
    "battleaxe" : "Battleaxe",
    "flail" : "Flail",
    "glaive" : "Glaive",
    "greateaxe" : "Greateaxe",
    "greatsword" : "Greatsword",
    "halberd" : "Halberd",
    "lance" : "Lance",
    "longsword" : "Longsword",
    "maul" : "Maul",
    "morningstar" : "Morningstar",
    "pike" : "Pike",
    "rapier" : "Rapier",
    "scimitar" : "Scimitar",
    "shortsword" : "Shortsword",
    "trident" : "Trident",
    "war_pick" : "War_pick",
    "warhammer" : "Warhammer",
    "whip" : "Whip",
    "blowgun" : "Blowgun",
    "crossbow_hand" : "Crossbow, Hand",
    "crossbow_heavy" : "Crossbow, Heavy",
    "longbow" : "Longbow",
    "net" : "Net"
}

damage_die = {
    "4" : "4",
    "6" : "6",
    "8" : "8",
    "10" : "10",
    "12" : "12"
    ""
}

damage_type = {
    "bludgeoning" : "bludgeoning",
    "piercing" : "piercing",
    "slashing" : "slashing"
}

weapon_properties = [['ammunition', 'finesse', 'heavy', 'light'], ['loading', 'range', 'reach', 'special'], ['thrown', 'two-handed', 'versatile']]


class Weapon():             # this is the weapon class that is a child of the Item class
    DB="character_sheet"
    def __init__(self, data):
        # name = 'Weapon Name', type='weapon', cost = 0, weight = 0, wt_index = 0, damage_Die = 4, is_magical = False, properties = [], base_attrb = 10
        self.id = data["id"]
        self.weapon_type = data["weapon_type"]
        self.damage_die = data["damage_die"]
        self.damage_type = data["damage_type"]
        self.magical_mod = data["magical_mod"]
        self.properties = data["properties"]
        self.base_attrb_key = data["base_attrb_key"]
        self.base_attrb = data["base_attribute"]
        self.prof_bonus = 2
        self.atk_bonus = math.floor((self.base_attrb - 10)/2) + self.prof_bonus
        # self.item_id = item.Item.save(Weapon.populate_item_data())

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
        print("__Weapon Class Method__")
        query = "SELECT * FROM weapons;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        print(f"Results are: {results}")
        # Create an empty list to append our instances of friends
        all_weapons = []
        # Iterate over the db results and create instances of friends with cls.
        for a_weapon in results:
            all_weapons.append( cls(a_weapon) )
        print(f"List of dojo[] is; {all_weapons}")
        return all_weapons

    
    @classmethod
    def get_weapon_by_id(cls,id):
        data = {"id" : id}
        query = "SELECT * FROM weapons WHERE id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("")
        print(f"The Result is: {result}")
        # Create an empty list to append our instances of friends
        weapon_item = cls(result[0])
        print("")
        print(f"The a_item is: {weapon_item}")
        # Iterate over the db results and create instances of friends with cls.
        return weapon_item
    
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__Weapon Save Method__")
        print(f"data: {data}")
        query = """INSERT INTO weapons ( weapon_type, damage_die, damage_type, properties, base_attrb_key, base_attribute, created_at, updated_at) 
        VALUES ( %(weapon_type)s, %(damage_die)s, %(damage_type)s, %(properties)s, %(base_attrb_key)s, %(base_attribute)s, NOW(), NOW() );
        """
        
        print("\n___Weapon Info Query____->", query)
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = """UPDATE weapons SET weapon_type=%(weapon_type)s, damage_die=%(damage_die)s, damage_type=%(damage_type)s, properties=%(properties)s, 
        base_attrb_key=%(base_attrb_key)s, base_attribute=%(base_attribute)s WHERE id=%(weapon_id)s;
        """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = "DELETE FROM weapons where id=%(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def get_all_weapons(cls):
        query = "SELECT * FROM items JOIN weapons ON items.weapon_id = weapons.id ORDER BY items.name;"
        results = connectToMySQL(cls.DB).query_db(query)
        weapons = {
            "simple_melee_weapon" : [],
            "simple_ranged_weapon" : [],
            "martial_melee_weapon" : [],
            "martial_ranged_weapon" : []
        }
        for dict_row in results:
            a_item = item.Item(dict_row)
            weapon_info ={
                "id" : dict_row["weapons.id"],
                "weapon_type" : dict_row["weapon_type"],
                "damage_die" : dict_row["damage_die"],
                "damage_type" : dict_row["damage_type"],
                "magical_mod" : dict_row['magical_mod'],
                "properties" : dict_row['properties'],
                "base_attrb_key" : dict_row["base_attrb_key"],
                "base_attribute" : dict_row["base_attribute"]
            }
            a_item.weapon = cls(weapon_info)
            
            if a_item.weapon.weapon_type == "simple_melee_weapon":
                weapons["simple_melee_weapon"].append(a_item)
            elif a_item.weapon.weapon_type == "simple_ranged_weapon":
                weapons["simple_ranged_weapon"].append(a_item)
            elif a_item.weapon.weapon_type == "martial_melee_weapon":
                weapons["martial_melee_weapon"].append(a_item)
            elif a_item.weapon.weapon_type == "martial_ranged_weapon":
                weapons["martial_ranged_weapon"].append(a_item)
            
        return weapons
    
    @classmethod
    def validate_weapon(cls,data):
        is_valid = True
        
        if not item.Item.validate_item(data): # if not (false)
            print("\n ____Weapon con item validation FAILED____")
            is_valid = False
        
        if 'weapon_type' not in data or data['weapon_type'] == "":
            print("____Weapon type FAILED____")
            flash("Please Select a Weapon Type","weapon_input")
            is_valid = False
        
        if 'damage_die' not in data or data['damage_die'] == "":
            print("____weapon damage_die FAILED____")
            flash("Please Select a damage die for the weapon","weapon_input")
            is_valid = False
        
        if 'damage_type' not in data or data['damage_type'] == "":
            print("____weapon damage_type FAILED____")
            flash("Please Select a damage type for the weapon","weapon_input")
            is_valid = False
        
        if 'damage_die' not in data or data['damage_die'] == "":
            print("____weapon damage_die FAILED____")
            flash("Please Select a damage die for the weapon","weapon_input")
            is_valid = False
        
        return is_valid
    
    def set_is_magical(self, magical):  # easy straight up value setting if needed
        self.is_magical = magical
    
    def set_damageDie(self, die):  # easy straight up value setting if needed
        self.damageDie = die
    
    def set_properties(self, property):  # easy straight up value setting if needed
        self.property = property
    
    def set_base_attrb(self, attrb):  # easy straight up value setting if needed
        self.base_attrb = int(attrb)
    
    def set_prof_bonus(self, prof):  # easy straight up value setting if needed
        self.prof_bonus = prof
    
    def set_atk_bonus(self): #configure the attack bonus
        self.atk_bonus = math.floor((self.base_attrb - 10)/2) + self.prof_bonus
    
    def roll_attack(self): # calculate and return the attack roll
        roll = random.randint(0,21)
        if roll == 20:
            print("ITS A CRIT!!")
        else:
            print(f"{roll} + {self.atk_bonus} = {roll + self.atk_bonus}")
        return (roll + self.atk_bonus)
    
    def roll_damage(self, is_crit = False): # Roll the damage that was dun and return it
        if is_crit:
            return (2 * (random.randint(0, self.damage_die+1)) +  math.floor((self.base_attrb - 10)/2))
        else:
            return (random.randint(1, self.damage_die+1) +  math.floor((self.base_attrb - 10)/2))
