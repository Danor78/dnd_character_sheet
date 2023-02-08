import math
import random
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import armor
from flask_app.models import weapon
from flask import flash

item_type = {
    "adventuring_gear": "Adventuring Gear",
    "poison" : "Poison",
    "weapon" : "Weapon",
    "ammunition" : "Ammunition",
    "artisans_tools" : "Artisan's Tools",
    "food_drink" : "Food and Drink",
    "gaming_set" : "Gaming Set",
    "generic_variant" : "Generic Variant",
    "armor" : "Armor",
    "instrument" : "Instrument",
    "simple_melee_weapon" : "Simple Melee Weapon",
    "simple_ranged_weapon" : "Simple Ranged Weapon",
    "martial_melee_weapon" : "Martial Melee Weapon",
    "martial_ranged_weapon" : "Martial Ranged Weapon",
    "other" : "Other",
    "shield" : "Shield",
    "simple_weapon" : "Simple Weapon",
    "spellcasting_focus" : "Spellcasting Focus",
    "staff" : "staff",
    "tack_harness" : "Tack and Harness",
    "tools" : "tools",
    "trade_good" : "Trade Good:",
    "vehicle" : "Vehicle",
    "vehicle_land" : "Vehicle (Land)",
    "wondrous_item" : "Wondrous Item",
    "firearm" : "Firearm",
    "potion" : "Potion",
    "ring" : "Ring",
    "rod" : "Rod",
    "scroll" : "Scroll",
    "wand" : "Wand",
    "tattoo" : "tattoo"
}

item_rarity = {
    "common": "Common", 
    "uncommon": "Uncommon", 
    "rare": "Rare", 
    "very_rare": "Very Rare", 
    "legendary": "Legendary"
}

item_src = {
    "hmb" : "HomeBrew",
    "AAG" : "Astral Adventures Guide",
    "BGDA" : "Balder's Gate: Descent into Avernus",
    "DMG" : "Dungeon Master's Guide",
    "EGW" : "Explorer's Guide to WildeMount",
    "ERLW" : "Eberron Rising from the Last War",
    "IDRF" : "Icewind Dale: Rime of the Frostmaiden",
    "JTRC" : "Journeys through the Radiant Citadel",
    "MTOF" : "Mordenkainen's Tome of Foes",
    "OOTA" : "Out of the Abyss",
    "PHB" : "Player's Handbook",
    "SCAG" : "Sword Coast Adventures Guide",
    "SCC" : "Strixhaven: A Curriculum of Chaos",
    "TOA" : "Tomb of Annihilatioin",
    "VGM" : "Volo's Guide to Monsters",
    "VRGR" : "Van Richten's Guide to Ravenloft",
    "WBTW" : "The Wild Beyond the Witchlight",
    "WDH" : "WaterDeep: Dragon Heist",
    "WDMM" : "WaterDeep: Dungeon of the Mad Mage",
    "XGE" : "Xanathar's Guide to Everything",
    "TCE" : "Tasha's Cauldron of Everything"
}





# The Item class is the base class for game items. Being simple rope, sword, shield, or magical. It has the most basic attributes
class Item:
    DB="character_sheet"
    def  __init__(self, data): # in the constructors I pass a dictionary into it with keyword keys with values. 
        # This way I don't have to add them in order if I don't want to or add some in the beginning and some others at the end.
        # name = 'item', type='item', cost = 0, weight = 0
        self.id = data["id"]
        self.name= data["name"]
        self.type = data["type"]
        self.cost = data["cost"]
        self.weight = data["weight"]
        self.description = data["description"]
        self.rarity = data["rarity"]
        self.source = data["source"]
        self.is_magical = data["is_magical"]
        self.is_attunable = data["is_attunable"]
        self.armor_id = data["armor_id"]
        self.weapon_id = data["weapon_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.weapon = None
        self.armor = None
        self.user_id = data['user_id']
    
    def display_item_info(self): # self explanitory
        print(" ")
        print(f"Item Name: {self.item_name}")
        print(f"Item Type: {self.type}")
        print(f"Item Cost: {self.cost}")
        print(f"Item Weight: {self.weight}")
        print(f"Item Description: {self.description}")
        print(f"Armor id: {self.armor_id}")
        print(f"Weapon id:  {self.weapon_id}")
        
        
    
    
    @classmethod
    def get_all(cls):
        # print("\n__item get_all Method__")
        query = "SELECT * FROM items LEFT JOIN weapons ON items.weapon_id = weapons.id LEFT JOIN armors on items.armor_id = armors.id ORDER BY items.name;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # for result in results:
            # print(f"\nResult[] is: {result}")

        # Create an empty list to append our instances of friends
        many_items = []
        # Iterate over the db results and create instances of friends with cls.
        for dict_row in results:
            a_item = cls(dict_row)
            # many_items.append( cls(dict_row) )
            if dict_row['armor_id']:
                armor_info ={
                    "id" : dict_row["armors.id"],
                    "armor_type" : dict_row["armor_type"],
                    "body_part" : dict_row["body_part"],
                    "armor_AC" : dict_row["armor_AC"],
                    "magical_mod" : dict_row['magical_mod'],
                    "str_req" : dict_row["str_req"],
                    "stealth_property" : dict_row["stealth_property"],
                }
                a_item.armor = armor.Armor(armor_info)
            elif dict_row["weapon_id"]:
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
                a_item.weapon = weapon.Weapon(weapon_info)
            
            many_items.append(a_item)
                
        # print(f"List of item[] is; {many_items}")
        return many_items

    @classmethod
    def get_all_by_order(cls,type):
        # print("\n__item get_all by order Method__")
        if type == 'type':
            query = f"SELECT * FROM items LEFT JOIN weapons ON items.weapon_id = weapons.id LEFT JOIN armors on items.armor_id = armors.id ORDER BY items.{type} ASC, armors.armor_type, weapons.weapon_type, items.name"
        else:
            query = f"SELECT * FROM items LEFT JOIN weapons ON items.weapon_id = weapons.id LEFT JOIN armors on items.armor_id = armors.id ORDER BY items.{type} ASC, items.name"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # for result in results:
            # print(f"\nResult[] is: {result}")

        # Create an empty list to append our instances of friends
        many_items = []
        # Iterate over the db results and create instances of friends with cls.
        for dict_row in results:
            a_item = cls(dict_row)
            # many_items.append( cls(dict_row) )
            if dict_row['armor_id']:
                armor_info ={
                    "id" : dict_row["armors.id"],
                    "armor_type" : dict_row["armor_type"],
                    "body_part" : dict_row["body_part"],
                    "armor_AC" : dict_row["armor_AC"],
                    "magical_mod" : dict_row['magical_mod'],
                    "str_req" : dict_row["str_req"],
                    "stealth_property" : dict_row["stealth_property"],
                }
                a_item.armor = armor.Armor(armor_info)
            elif dict_row["weapon_id"]:
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
                a_item.weapon = weapon.Weapon(weapon_info)
            
            many_items.append(a_item)
                
        # print(f"List of item[] is; {many_items}")
        return many_items
    
    
    @classmethod
    def get_item_by_id(cls,id):
        # print("\n____Get Item by Id method____")
        data = {"id" : id}
        query = "SELECT * FROM items LEFT JOIN weapons ON items.weapon_id = weapons.id LEFT JOIN armors ON items.armor_id = armors.id WHERE items.id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
       
        # print("\n____The Result of get item by id is:_____",result)
        # Create an empty list to append our instances of friends
        a_item = cls(result[0])
        # print("\n___ a_item after cls(result[0])", a_item)
        dict_row = result[0]
        if dict_row['armor_id']:
            armor_info ={
                "id" : dict_row["armors.id"],
                "armor_type" : dict_row["armor_type"],
                "body_part" : dict_row["body_part"],
                "armor_AC" : dict_row["armor_AC"],
                "magical_mod" : dict_row['armors.magical_mod'],
                "str_req" : dict_row["str_req"],
                "stealth_property" : dict_row["stealth_property"],
            }
            a_item.armor = armor.Armor(armor_info)
        elif dict_row["weapon_id"]:
            weapon_info ={
                "id" : dict_row["id"],
                "weapon_type" : dict_row["weapon_type"],
                "damage_die" : dict_row["damage_die"],
                "damage_type" : dict_row["damage_type"],
                "magical_mod" : dict_row['magical_mod'],
                "properties" : dict_row['properties'],
                "base_attrb_key" : dict_row["base_attrb_key"],
                "base_attribute" : dict_row["base_attribute"]
            }
            a_item.weapon = weapon.Weapon(weapon_info)
        # print("")
        # Iterate over the db results and create instances of friends with cls.
        return a_item
    
    
    @classmethod
    def save(cls, data ):
        # print("")
        # print("__item Save Method__")
        # print(f"data: {data}")
        query = "INSERT INTO items ( name, type, cost, weight, description, rarity, source, is_magical, is_attunable, created_at, updated_at, img, armor_id, weapon_id, user_id) VALUES ( %(name)s, %(type)s, %(cost)s, %(weight)s, %(description)s, %(rarity)s, %(source)s, %(is_magical)s, %(is_attunable)s, NOW(), NOW(), %(img)s, %(armor_id)s, %(weapon_id)s, %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def update(cls, data ):
        query = "UPDATE items SET name=%(name)s, type=%(type)s, cost=%(cost)s, weight=%(weight)s, description=%(description)s, rarity=%(rarity)s,  source=%(source)s, is_magical=%(is_magical)s, is_attunable=%(is_attunable)s, img=%(img)s, armor_id=%(armor_id)s, weapon_id=%(weapon_id)s  WHERE id=%(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = "DELETE FROM items where id=%(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def validate_item(cls, data): 
        is_valid = True
        
        print("\n___Item's validated data___", data)
        
        if len(data['name']) < 4:
            print("____Item Name FAILED____")
            flash("Name must be at least 3 letters long","item_input")
            is_valid = False
        
        if 'type' not in data or data['type'] == "":
            print("____Item Type FAILED____")
            flash("Must Select a Type","item_input")
            is_valid = False
            
        if int(data['cost']) <= 0:
            print("____Item Cost FAILED____")
            flash("Must input a cost for the Item","item_input")
            is_valid = False
        
        if int(data['weight']) <= 0:
            print("____Item weight FAILED____")
            flash("Must input a weight for the Item","item_input")
            is_valid = False
        
        if 'description' not in data or data['description'] == "":
            print("____Item description FAILED____")
            flash("Please enter a description","item_input")
            is_valid = False
        
        if data['rarity'] == "":
            print("____Item Rarity FAILED____")
            flash("Please Select a Rarity","item_input")
            is_valid = False
            
        if data['is_magical'] == "":
            print("____Item is magical FAILED____")
            flash("Please Select if Magical or not","item_input")
            is_valid = False
            
        if data['is_attunable'] == "":
            print("____Item is attunable FAILED____")
            flash("Please Select if attunable or not","item_input")
            is_valid = False
            
        if 'source' not in data or data['source'] == "":
            print("____Item source  FAILED____")
            flash("Please Select a source","item_input")
            is_valid = False
            
        return is_valid
            

        
        
        
        
# for data in import_data:
#     Item.save(data)
        
    
    
    
    # def set_description(self): # can't seem to make this work. It just sits there and seems to do nothing. I type but nothing happens.
    #     self.description = str(input("Enter Item Description:"))
    
    # def set_name(self,name): # easy straight up value setting if needed
    #     self.item_name = name
    
    # def set_type(self, type): # easy straight up value setting if needed
    #     self.type = type
    
    # def set_price(self, cost): # easy straight up value setting if needed
    #     self.cost = cost
        
    # def set_weight(self, weight): # easy straight up value setting if needed
    #     self.weight = weight