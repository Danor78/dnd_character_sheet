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

race_prof = {
    "sav_prof" : {
        "str_sav_prof" : "Strength",
        "dex_sav_prof" : "Dexterity",
        "con_sav_prof" : "Constitution",
        "int_sav_prof" : "Intelligence",
        "wis_sav_prof" : "Wisdom",
        "cha_sav_prof" : "Charisma"
        },
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
    "armor_prof" : {
        "heavy_armor_prof" : "Heavy Armor",
        "medium_armor_prof" : "Medium Armor",
        "light_armor_prof" : "Light Armor",
        "shields_prof" : "Shields"
        },
    "weapon_prof" : {
        "simple_weapons_prof" : "Simple Weapons",
        "martial_weapons_prof" : "Martial Weapons",
        "sword_prof" : "Swords",
        "axe_prof" : "Axes",
        "bow_prof" : "Bows",
        "pole_prof" : "Pole Arms",
        "warhammer_prof" : "War Hammers"
        },
    "weapon_type" : {
        "club_prof" : "Club",
        "dagger_prof" : "Dagger",
        "greatclub_prof" : "Greatclub",
        "handaxe_prof" : "Handaxe",
        "javelin_prof" : "Javelin",
        "light_hammer_prof" : "Light Hammer",
        "mace_prof" : "Mace",
        "quarterstaff_prof" : "Quarterstaff",
        "sickle_prof" : "Sickle",
        "spear_prof" : "Spear",
        "unarmed_strike_prof" : "Unarmed Strike",
        "light_crossbow_prof" : "Light Crossbow",
        "dart_prof" : "Dart",
        "shortbow_prof" : "Shortbow",
        "sling_prof" : "Sling",
        "battleaxe_prof" : "Battleaxe",
        "flail_prof" : "Flail",
        "glaive_prof" : "Glaive",
        "greateaxe_prof" : "Greateaxe",
        "greatsword_prof" : "Greatsword",
        "halberd_prof" : "Halberd",
        "lance_prof" : "Lance",
        "longsword_prof" : "Longsword",
        "maul_prof" : "Maul",
        "morningstar_prof" : "Morningstar",
        "pike_prof" : "Pike",
        "rapier_prof" : "Rapier",
        "scimitar_prof" : "Scimitar",
        "shortsword_prof" : "Shortsword",
        "trident_prof" : "Trident",
        "war_pick_prof" : "War_pick",
        "warhammer_prof" : "Warhammer",
        "whip_prof" : "Whip",
        "blowgun_prof" : "Blowgun",
        "crossbow_hand_prof" : "Crossbow, Hand",
        "crossbow_heavy_prof" : "Crossbow, Heavy",
        "longbow_prof" : "Longbow",
        "net_prof" : "Net"
    },
    "racial_profs" : [
        "weapon_prof1",
        "weapon_prof2",
        "weapon_prof3",
        "weapon_prof4",
        "armor_prof1",
        "armor_prof2",
        "armor_prof3",        
    ],
    "lang_prof" : {
            "common_lang_prof" : "Common",
            "dwarvish_lang_prof" : "Dwarvish",
            "elvish_lang_prof" : "Elvish",
            "giant_lang_prof" : "Giant",
            "gnomish_lang_prof" : "Gnomish",
            "goblin_lang_prof" : "Goblin",
            "halfling_lang_prof" : "Halfling",
            "orc_lang_prof" : "Orc",
            "abyssal_lang_prof" : "Abyssal",
            "celestial_lang_prof" : "Celestial",
            "draconic_lang_prof" : "Draconic",
            "deepspeech_lang_prof" : "Deepspeech",
            "infernal_lang_prof" : "Infernal",
            "primordial_lang_prof" : "Primordial",
            "sylvan_lang_prof" : "Sylvan",
            "undercommon_lang_prof" : "Undercommon"
        },
    "source" : {
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
    },
    "attrib" : [
        "str",
        "dex",
        "con",
        "int",
        "wis",
        "cha"
    ]
}

class Char_race:
    DB="character_sheet"
    table_data = ["char_races", "name", "description", 
                "racial_traits", "racial_attrib", "racial_profs", 
                "speed", "source", "created_at", "updated_at", "user_id"]
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = json.loads(data['description'])
        self.racial_traits = json.loads(data['racial_traits'])
        self.racial_attrib = json.loads(data['racial_attrib'])
        self.racial_profs = json.loads(data['racial_profs'])
        self.speed = data['speed']
        self.source = data['source']
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
    