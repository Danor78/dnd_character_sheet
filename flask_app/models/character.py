import math
import random
import json
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import armor
from flask_app.models import weapon
from flask_app.models import item
from flask import flash


char_dict ={
    "race" : {
        "human" : "Human",
        "duergar_dwarf" : "Duergar Dwarf",
        "hill_dwarf" : "Hill Dwarf",
        "mountain_dwarf" : "Mountain Dwarf",
        "sun_elf" : "Sun Elf",
        "wood_elf" : "Wood Elf",
        "dark_elf" : "Dark Elf",
        "gold_dragonborn" : "Gold Dragonborn",
        "silver_dragonborn" : "Silver Dragonborn",
        "Copper_dragonborn" : "Copper Dragonborn",
        "brass_dragonborn" : "Brass Dragonborn",
        "bronze_dragonborn" : "Bronze Dragonborn",
        "red_dragonborn" : "Red Dragonborn",
        "black_dragonborn" : "Black Dragonborn",
        "blue_dragonborn" : "Blue Dragonborn",
        "green_dragonborn" : "Green Dragonborn",
        "white_dragonborn" : "White Dragonborn",
        "forest_gnome" : "Forest Gnome",
        "rock_gnome" : "Rock Gnome",
        "half_elf" : "Half Elf",
        "half_orc" : "Half Orc",
        "lightfoot_halfling" : "Lightfoot Halfling",
        "Stout_halfling" : "Stout Halfling",
        "tiefling" : "Tiefling"
    },
    "class" : {
        "artificer" : "Artificer",
        "barbarian" : "Barbarian",
        "bard" : "Bard",
        "cleric" : "Cleric",
        "druid" : "Druid",
        "fighter" : "Fighter",
        "monk" : "Monk",
        "paladin" : "Paladin",
        "ranger" : "Ranger",
        "rogue" : "Rogue",
        "sorcerer" : "Sorcerer",
        "warlock" : "Warlock",
        "wizard" : "Wizard"
    },
    "background" : {
        "acolyte" : "Acolyte",
        "charlatan" : "Charlatan",
        "criminal" : "Criminal",
        "entertainer" : "Entertainer",
        "folk_hero" : "Folk Hero",
        "guild_artisan" : "Build Artisan",
        "hermit" : "Hermit",
        "noble" : "Noble",
        "outlander" : "Outlander",
        "sailor" : "Sailor",
        "soldier" : "Soldier",
        "urchin" : "Urchin"
    },
    "alignment" : {
        "law_good" : "Lawful Good",
        "law_neutral" : "Lawful Neutral",
        "law_evil" : "Lawful Evil",
        "neut_good" : "Neutral Good",
        "neut_neutral" : "Neutral Neutral",
        "neut_evil" : "Neutral Evil",
        "chaotic_good" : "Chaotic Good",
        "chaotic_neutral" : "Chaotic Neutral",                                    
        "chaotic_evil" : "Chotic Evil"  
    },
    "savs" : {
        "str_sav" : " Strength",
        "dex_sav" : " Dexterity",
        "con_sav" : " Constitution",
        "int_sav" : " Intelligence",
        "wis_sav" : " Wisdom",
        "cha_sav" : " Charisma",
    },
    "skills" : [{
        "acrobatics" : [" Acrobatics", "Dex"],
        "animal_handling" : [" Animal Handling", "Wis"],
        "arcana" : [" Arcana", "Int"],
        "athletics" : [" Athletics", "Str"],
        "deception" : [" Deception", "Cha"],
        "history" : [" History", "Int"],
        }, {
        "insight" : [" Insight", "Wis"],
        "intimidation" : [" Intimidation", "Cha"],
        "investigation" : [" Investigation", "Int"],
        "medicine" : [" Medicine", "Wis"],
        "nature" : [" Nature", "Int"],
        "perception" : [" Perception", "Wis"],
        }, {
        "performance" : [" Performance", "Cha"],
        "persuasion" : [" Persuasion", "Cha"],
        "religion" : [" Religion", "Int"],
        "sleight_of_hand" : [" Sleight of Hand", "Dex"],
        "stealth" : [" Stealth", "Dex"],
        "survival" : [" Survival", "Wis"]
        }
    ]
}




# The Character class will handle all the items, armor, weapons and all other attributes that pertain to the player
class Character:
    DB="character_sheet"
    def __init__(self, data):
        self.id = data["id"]#
        self.char_name = data['char_name']#
        self.char_class = data['char_class']#
        self.char_background = data['char_background']#
        self.char_race = data['char_race']#
        self.char_level = data['char_level']#
        self.owner_name = data['owner_name']
        self.char_alignment = data['char_alignment']#
        self.experience_points = data['experience_points']
        self.attributes = json.loads(data['attributes'])#
        self.inspiration = data['inspiration']#
        self.prof_bonus = data['prof_bonus']#
        self.proficiencies = json.loads(data['proficiencies'])#
        self.savs = json.loads(data['savs'])#
        self.skills = json.loads(data['skills'])#
        self.passive_wisdom = data['passive_wisdom']#
        self.ac_class = data['ac_class']
        self.initiative = data['initiative']#
        self.speed = data['speed']#
        self.maximum_hp = data['maximum_hp']#
        self.current_hp = data['current_hp']#
        self.temp_hp = data['temp_hp']#
        self.hit_dice_total = data['hit_dice_total']#
        self.hit_dice = data['hit_dice']#
        self.death_save_successes = data['death_save_successes']#
        self.death_save_failures = data['death_save_failures']#
        # self.attack_or_spell_id = data['attack_or_spell_id']#
        self.equipment_list = data['equipment_list']#
        self.coin = json.loads(data['coin'])#
        self.personality_traits = data['personality_traits']#
        self.ideals = data['ideals']#
        self.bonds = data['bonds']#
        self.flaws = data['flaws']#
        self.features_and_traits = data['features_and_traits']#
        self.created_at = data['created_at']#
        self.updated_at = data['updated_at']#
        self.user_id = data['user_id']
        
        
        # self.weapons_to_equip = weapons_equipped
        # self.equipped_weapons = {"main_hand" : equipment.Weapon,
        #                         "off_hand" : equipment.Weapon,
        #                         "two_handed" : False
        #                         }
        # self.armor_to_equip = armor_equipped
        # self.equipped_armor = { "head" : equipment.Armor,
        #                     "chest" : equipment.Armor,
        #                     "pants" : equipment.Armor,
        #                     "feet" : equipment.Armor,
        #                     "arms" : equipment.Armor,
        #                     "hands" : equipment.Armor
        #                     }
        # self.roll_attributes()
        # self.populate_skill_mods()
        # self.populate_sav_mods()

        # if self.weapons_to_equip != {}:
        #     self.equipped_weapons = Character.don_equipment(self.weapons_to_equip, self.equipped_weapons)

        # if self.armor_to_equip != {}:
        #     self.equipped_armor = Character.don_equipment(self.armor_to_equip, self.equipped_armor)



    @classmethod
    def get_all(cls):
        print("")
        print("__Armor Class Method__")
        query = "SELECT * FROM characters;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # for character in results:
            # print(f"\n__A character is: {character}")
            
        # Create an empty list to append our instances of friends
        all_characters = []
        # Iterate over the db results and create instances of friends with cls.
        for a_character in results:
            all_characters.append( cls(a_character) )
        # print(f"List of characters are; {all_characters}")
        return all_characters

    @classmethod
    def get_all_by_user(cls, id):
        data = {
            "id" : id
        }
        print("")
        print("__Armor Class Method__")
        query = "SELECT * FROM characters WHERE user_id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query, data)
        # for character in results:
            # print(f"\n__A character is: {character}")
            
        # Create an empty list to append our instances of friends
        all_characters = []
        # Iterate over the db results and create instances of friends with cls.
        for a_character in results:
            all_characters.append( cls(a_character) )
        # print(f"List of characters are; {all_characters}")
        return all_characters




    @classmethod
    def get_character_by_id(cls,id):
        data = {"id" : id}
        query = "SELECT * FROM characters WHERE id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
        print("")
        print(f"The Result is: {result}")
        # Create an empty list to append our instances of friends
        a_character = cls(result[0])
        print("")
        print(f"The character is: {a_character}")
        # Iterate over the db results and create instances of friends with cls.
        return a_character
    
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__Character Save Method__")
        # print(f"data: {data}")
        query = """
            INSERT INTO characters ( char_name, char_class, char_background, char_race, char_level, owner_name, char_alignment, experience_points, 
            attributes, inspiration, prof_bonus, proficiencies, savs, skills, passive_wisdom, ac_class, initiative, speed, maximum_hp, current_hp, 
            temp_hp, hit_dice_total, hit_dice, death_save_successes, death_save_failures, equipment_list, coin, personality_traits, 
            ideals, bonds, flaws, features_and_traits, created_at, updated_at, user_id) 
            VALUES ( %(char_name)s, %(char_class)s, %(char_background)s, %(char_race)s, %(char_level)s, %(owner_name)s, %(char_alignment)s, %(experience_points)s, 
            %(attributes)s, %(inspiration)s, %(prof_bonus)s, %(proficiencies)s, %(savs)s, %(skills)s, %(passive_wisdom)s, %(ac_class)s, %(initiative)s, %(speed)s, 
            %(maximum_hp)s, %(current_hp)s, %(temp_hp)s, %(hit_dice_total)s, %(hit_dice)s, %(death_save_successes)s, %(death_save_failures)s, 
            %(equipment_list)s, %(coin)s, %(personality_traits)s, %(ideals)s, %(bonds)s, %(flaws)s, %(features_and_traits)s, NOW(), NOW(), %(user_id)s );
            """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def validate_char(cls,data):
        is_valid = True
        
        print("\n___Character's validated data___", data)
        
        if len(data['char_name']) < 3:
            print("____Char Name FAILED____")
            flash("Name must be at least 3 letters long","char_input")
            is_valid = False
        
        if 'char_race' not in data or data['char_race'] != "":
            print("____Char Race FAILED____")
            flash("Please Select a race","char_input")
            is_valid = False
        
        if 'char_class' not in data or data['char_class'] != "":
            print("____Char class FAILED____")
            flash("Please Select a class","char_input")
            is_valid = False
        
        if 'char_background' not in data or data['char_background'] != "":
            print("____Char background FAILED____")
            flash("Please Select a background","char_input")
            is_valid = False
        
        if 'char_alignment' not in data or data['char_alignment'] != "" :
            print("____Char alignment FAILED____")
            flash("Please Select a alignment","char_input")
            is_valid = False
        
        if 'personality_traits' not in data or data['personality_traits'] != "":
            print("____Char Personality FAILED____")
            flash("Please fill out a Personality","char_input")
            is_valid = False
        
        if 'ideal' not in data or data['ideal'] != "":
            print("____Char Ideal FAILED____")
            flash("Please fill out a ideal","char_input")
            is_valid = False
        
        if 'bond' not in data or data['bond'] != "":
            print("____Char Bond FAILED____")
            flash("Please fill out a bond","char_input")
            is_valid = False
        
        if 'flaw' not in data or data['flaw'] != "":
            print("____Char Flaw FAILED____")
            flash("Please fill out a flaw","char_input")
            is_valid = False
        
        return is_valid
        
        
        
    
    
    @classmethod
    def update(cls, data ):
        query = """
        UPDATE characters SET char_name=%(char_name)s, char_class=%(char_class)s, char_background=%(char_background)s, char_race=%(char_race)s, char_level=%(char_level)s, 
        owner_name=%(owner_name)s, char_alignment=%(char_alignment)s, experience_points=%(experience_points)s, attributes=%(attributes)s, inspiration=%(inspiration)s, 
        prof_bonus=%(prof_bonus)s, proficiencies=%(proficiencies)s, savs=%(savs)s, skills=%(skills)s, passive_wisdom=%(passive_wisdom)s, ac_class=%(ac_class)s, 
        initiative=%(initiative)s,  speed=%(speed)s,  maximum_hp=%(maximum_hp)s,  current_hp=%(current_hp)s,  temp_hp=%(temp_hp)s, hit_dice_total=%(hit_dice_total)s, 
        hit_dice=%(hit_dice)s, death_save_successes=%(death_save_successes)s, death_save_failures=%(death_save_failures)s, equipment_list=%(equipment_list)s, coin=%(coin)s, 
        personality_traits=%(personality_traits)s, ideals=%(ideals)s, bonds=%(bonds)s, flaws=%(flaws)s, 
        features_and_traits=%(features_and_traits)s WHERE id=%(id)s;
        """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )   
    
    
    @classmethod
    def delete(cls, id):
        data = {'id':id}
        query = "DELETE FROM characters where id=%(id)s"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.DB).query_db( query, data )




    @staticmethod
    def calc_mod(attrib, prof_bonus = 2, is_proficient = False): # calculate the modifier of the attribute and return it
        if is_proficient:
            return math.floor((attrib - 10)/2) + prof_bonus
        else:
            return math.floor((attrib - 10)/2)
    
    @classmethod
    def roll_attributes(cls):  #  I made the function roll for attributes like I normally do.
                                #  You roll 4 six-sided die (4d6) and you drop the lowest values and add up the rest
                                #  You do this 6 times. I just don't know how to get the user to choose which numbers are assigned to what.
        
        for key in self.attribute_dict:
            rolled_nums = []
            for roll_num in range(4):
                rolled_nums.append(random.randint(0, 7))
            lowest_index = 0
            for i in range(4):
                if rolled_nums[lowest_index] > rolled_nums[i]:
                    lowest_index = i
            rolled_nums.pop(lowest_index)
            sum = 0
            for i in range(3):
                sum += rolled_nums[i]
            self.attribute_dict[key] = sum
            
    def populate_skill_mods(self): #populate all the appropriate modifiers for the skills
        
        key = "athletics"
        attrb_key = "strength"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        
        attrb_key = "dexterity"
        key = "acrobatics"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "slight_of_hand"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "stealth"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        
        attrb_key = "intelligence"
        key = "arcana"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "history"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "investigation"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "nature"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "religion"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        
        attrb_key = "wisdom"
        key = "animal_handling"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "insight"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "medicine"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "perception"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "survival"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        
        attrb_key = "charisma"
        key = "deception"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "intimidation"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "performance"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        key = "persuasion"
        self.skills[key] = Character.calc_mod(self.attribute_dict[attrb_key], self.proficiency_bonus, self.skill_proficiencies[key])
        # print(f"skills dict: {self.skills}")

    def populate_sav_mods(self):
        key_id = 0
        tempKey_arr =[]
        for key in self.attribute_dict:
            tempKey_arr.append(key)
            
        for key in self.saving_throws:
            self.saving_throws[key] = Character.calc_mod(self.attribute_dict[tempKey_arr[key_id]], self.proficiency_bonus, self.saving_throws_proficiencies[key])
            key_id += 1

    @staticmethod
    def don_equipment(stuff_to_don, don_to_me):
        for key in don_to_me:
            if key in don_to_me:
                don_to_me[key] = stuff_to_don[key]
        
        return don_to_me
    
    def does_hit(self, hit):
        if hit >= self.ac_class:
            return True
        else:
            return False
    
    # def equip_weapon(self, equip_wep =equipment.Weapon, hand = 'main_hand',):
    #     self.equipped_weapons[hand] = equip_wep
        
    # def display_equipment(self):
    #     print(f"Equipped weapons are {self.equipped_weapons}")
    
    # def melee_attack(self, target, hand = 'main_hand'):
    #     roll = self.equipped_weapons[hand].roll_attack()
    #     print(f"{self.my_name} rolled a {roll}")
    #     if target.does_hit(roll):
    #         damage = self.equipped_weapons[hand].roll_damage()
    #         print(f"attack hits for {damage} damage")
    #     else:
    #         print("attack does not hit")
        
    def roll_initiative(self):
        roll = random.randint(0,21) + math.floor((self.attribute_dict['dexterity'] - 10)/2)
        return roll







