import math
import random
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import armor
from flask_app.models import weapon

# import_data = [{"id":10, "name":"Padded Armor", "type":"armor", "cost":5000, "weight":8, "description":"Padded armor consists of quilted layers of cloth and batting.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 11:14:09", "updated_at":"2023-01-16 18:49:33", "img":"", "armor_id":3, "weapon_id":0, "user_id":1},
#     {"id":11, "name":"Leather Armor", "type":"armor", "cost":10000, "weight":10, "description":"The breastplate and shoulder protectors of this armor are made of leather that has been stiffened by being boiled in oil. The rest of the armor is made of softer and more flexible materials.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 11:25:29", "updated_at":"2023-01-16 11:25:29", "img":"", "armor_id":4, "weapon_id":0, "user_id":1},
#     {"id":12, "name":"Studded Leather Armor", "type":"armor", "cost":450000, "weight":13, "description":"Made from tough but flexible leather, studded leather is reinforced with close-set rivets or spikes.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:27:13", "updated_at":"2023-01-16 21:31:15", "img":"", "armor_id":5, "weapon_id":0, "user_id":1},
#     {"id":13, "name":"Hide Armor", "type":"armor", "cost":100000, "weight":12, "description":"This crude armor consists of thick furs and pelts. It is commonly worn by barbarian tribes, evil humanoids, and other folk who lack access to the tools\r\nand materials needed to create better armor.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:30:46", "updated_at":"2023-01-16 21:30:46", "img":"", "armor_id":6, "weapon_id":0, "user_id":1},
#     {"id":14, "name":"Chain Shirt Armor", "type":"armor", "cost":500000, "weight":20, "description":"Made of interlocking metal rings, a chain shirt is worn between layers of clothing or leather. This armor offers modest protection to the wearer's upper\r\nbody and allows the sound of the rings rubbing against one another to be muffled by outer layers.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:34:23", "updated_at":"2023-01-16 21:34:23", "img":"", "armor_id":7, "weapon_id":0, "user_id":1},
#     {"id":15, "name":"Scale Mail Armor", "type":"armor", "cost":500000, "weight":45, "description":"This armor consists of a coat and leggings (and perhaps a separate skirt) of leather covered with overlapping pieces of metal, much like the scales of a\r\nfish, The suit includes gauntlets.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:37:42", "updated_at":"2023-01-16 21:37:42", "img":"", "armor_id":8, "weapon_id":0, "user_id":1},
#     {"id":16, "name":"Breastplate Armor", "type":"armor", "cost":4000000, "weight":20, "description":"This armor consists of a fitted metal\r\nchest piece worn with supple leather, Although it leaves the legs and arms relatively unprotected, this armor\r\nprovides good protection for the wearer's vital organs while leaving the wearer relatively unencumbered.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:40:04", "updated_at":"2023-01-16 21:40:04", "img":"", "armor_id":9, "weapon_id":0, "user_id":1},
#     {"id":17, "name":"Half Plate Armor", "type":"armor", "cost":7500000, "weight":40, "description":"Half plate consists of shaped metal plates that cover most of the wearer's body, it does not include leg protection beyond simple greaves that are attached with leather straps.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 21:42:54", "updated_at":"2023-01-16 21:42:54", "img":"", "armor_id":10, "weapon_id":0, "user_id":1},
#     {"id":18, "name":"Ring Mail Armor", "type":"armor", "cost":300000, "weight":40, "description":"This armor is leather armor with heavy\r\nrings sewn into it. The rings help reinforce the armor against blows from swords and axes. Ring mail is inferior to chain mail, and it\"s usually worn only by those who can't afford better armor.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 23:23:00", "updated_at":"2023-01-16 23:23:00", "img":"", "armor_id":11, "weapon_id":0, "user_id":1},
#     {"id":19, "name":"Chain Mail Armor", "type":"armor", "cost":750000, "weight":0, "description":"Made of interlocking metal rings, chain\r\nmail includes a layer of quilted fabric worn underneath the mail to prevent chafing and to cushion the impact of\r\nblows. The suit includes gauntlets.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 23:26:09", "updated_at":"2023-01-16 23:26:09", "img":"", "armor_id":12, "weapon_id":0, "user_id":1},
#     {"id":20, "name":"Splint Amor", "type":"armor", "cost":2000000, "weight":60, "description":"This armor is made of narrow vertical strips of metal riveted to a backing of leather that is worn over cloth padding. Flexible chain mail protects the joints.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 23:29:13", "updated_at":"2023-01-16 23:29:13", "img":"", "armor_id":13, "weapon_id":0, "user_id":1},
#     {"id":21, "name":"Plate Armor", "type":"armor", "cost":15000000, "weight":65, "description":"Plate consists of shaped, interlocking metal plates to cover the entire body. A suit of plate includes gauntlets, heavy leather boots, a visored helmet, and\r\nthick layers of padding underneath the armor. Buckles and straps distribute the weight over the body.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-16 23:32:24", "updated_at":"2023-01-16 23:32:24", "img":"", "armor_id":14, "weapon_id":0, "user_id":1},
#     {"id":22, "name":"Shield", "type":"armor", "cost":100000, "weight":6, "description":"A shield is made from wood or metal and is carried in one hand.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:20:23", "updated_at":"2023-01-17 00:20:23", "img":"", "armor_id":15, "weapon_id":0, "user_id":1},
#     {"id":23, "name":"Club", "type":"simple_melee_weapon", "cost":100, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:30:07", "updated_at":"2023-01-17 00:30:07", "img":"", "armor_id":0, "weapon_id":3, "user_id":1},
#     {"id":24, "name":"Dagger", "type":"simple_melee_weapon", "cost":20000, "weight":1, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:34:29", "updated_at":"2023-01-17 00:34:29", "img":"", "armor_id":0, "weapon_id":4, "user_id":1},
#     {"id":25, "name":"Greatclub", "type":"simple_melee_weapon", "cost":200, "weight":10, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:36:18", "updated_at":"2023-01-17 01:27:00", "img":"", "armor_id":0, "weapon_id":5, "user_id":1},
#     {"id":26, "name":"Handaxe", "type":"simple_melee_weapon", "cost":50000, "weight":2, "description":"range 20/60", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:38:56", "updated_at":"2023-01-17 01:27:45", "img":"", "armor_id":0, "weapon_id":6, "user_id":1},
#     {"id":27, "name":"Javelin", "type":"simple_melee_weapon", "cost":500, "weight":2, "description":"range 30/120", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 00:41:40", "updated_at":"2023-01-17 01:26:24", "img":"", "armor_id":0, "weapon_id":7, "user_id":1},
#     {"id":28, "name":"Light Hammer", "type":"simple_melee_weapon", "cost":20000, "weight":2, "description":"range 20/60", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 01:19:47", "updated_at":"2023-01-17 01:25:35", "img":"", "armor_id":0, "weapon_id":8, "user_id":1},
#     {"id":29, "name":"Mace", "type":"simple_melee_weapon", "cost":5000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 01:21:45", "updated_at":"2023-01-17 01:25:00", "img":"", "armor_id":0, "weapon_id":9, "user_id":1},
#     {"id":30, "name":"Quarterstaff", "type":"simple_melee_weapon", "cost":200, "weight":0, "description":"Versatile (1/8)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 01:24:11", "updated_at":"2023-01-17 01:24:11", "img":"", "armor_id":0, "weapon_id":10, "user_id":1},
#     {"id":31, "name":"Sickle", "type":"simple_melee_weapon", "cost":10000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 14:18:19", "updated_at":"2023-01-17 14:23:05", "img":"", "armor_id":0, "weapon_id":11, "user_id":1},
#     {"id":32, "name":"Spear", "type":"simple_melee_weapon", "cost":10000, "weight":3, "description":"(range 20/60), versatile (ld8)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 14:22:40", "updated_at":"2023-01-17 14:22:40", "img":"", "armor_id":0, "weapon_id":12, "user_id":1},
#     {"id":33, "name":"Crossbow, light", "type":"simple_ranged_weapon", "cost":250000, "weight":5, "description":"Ammunition (range 80/320), loading, two-handed", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 14:28:58", "updated_at":"2023-01-17 14:28:58", "img":"", "armor_id":0, "weapon_id":13, "user_id":1},
#     {"id":34, "name":"Dart", "type":"simple_ranged_weapon", "cost":5, "weight":0, "description":"Finesse, thrown (range 20/60)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 15:24:42", "updated_at":"2023-01-17 15:24:42", "img":"", "armor_id":0, "weapon_id":14, "user_id":1},
#     {"id":35, "name":"Shortbow", "type":"simple_ranged_weapon", "cost":250000, "weight":2, "description":"Ammunition (range 80/320), two-handed\r\n", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 15:30:14", "updated_at":"2023-01-17 15:30:14", "img":"", "armor_id":0, "weapon_id":15, "user_id":1},
#     {"id":36, "name":"Sling", "type":"simple_ranged_weapon", "cost":100, "weight":0, "description":"Ammunition (range 30/120)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 15:32:33", "updated_at":"2023-01-17 15:32:33", "img":"", "armor_id":0, "weapon_id":16, "user_id":1},
#     {"id":37, "name":"Battleaxe", "type":"martial_melee_weapon", "cost":100000, "weight":4, "description":"Versatile (1d10)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 15:45:59", "updated_at":"2023-01-17 15:45:59", "img":"", "armor_id":0, "weapon_id":17, "user_id":1},
#     {"id":38, "name":"Flail ", "type":"martial_melee_weapon", "cost":100000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 15:47:03", "updated_at":"2023-01-17 15:47:03", "img":"", "armor_id":0, "weapon_id":18, "user_id":1},
#     {"id":39, "name":"Glaive", "type":"martial_melee_weapon", "cost":200000, "weight":6, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 16:35:26", "updated_at":"2023-01-17 16:35:26", "img":"", "armor_id":0, "weapon_id":19, "user_id":1},
#     {"id":40, "name":"Greataxe", "type":"martial_melee_weapon", "cost":300000, "weight":7, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 16:41:49", "updated_at":"2023-01-17 16:41:49", "img":"", "armor_id":0, "weapon_id":20, "user_id":1},
#     {"id":41, "name":"Greatsword", "type":"martial_melee_weapon", "cost":500000, "weight":6, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 16:56:06", "updated_at":"2023-01-17 16:56:06", "img":"", "armor_id":0, "weapon_id":21, "user_id":1},
#     {"id":42, "name":"Halberd", "type":"martial_melee_weapon", "cost":200000, "weight":6, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 16:57:55", "updated_at":"2023-01-17 16:57:55", "img":"", "armor_id":0, "weapon_id":22, "user_id":1},
#     {"id":43, "name":"Lance", "type":"martial_melee_weapon", "cost":100000, "weight":6, "description":"You have disadvantage when you use a lance to attack a target within 5 feet of you. Also, a lance requires two hands to wield when you aren't mounted.", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:01:22", "updated_at":"2023-01-17 17:01:22", "img":"", "armor_id":0, "weapon_id":23, "user_id":1},
#     {"id":44, "name":"Longsword", "type":"martial_melee_weapon", "cost":150000, "weight":3, "description":"Versatile (1d10)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:03:12", "updated_at":"2023-01-17 17:03:12", "img":"", "armor_id":0, "weapon_id":24, "user_id":1},
#     {"id":45, "name":"Maul", "type":"martial_melee_weapon", "cost":100000, "weight":0, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:04:10", "updated_at":"2023-01-17 17:04:10", "img":"", "armor_id":0, "weapon_id":25, "user_id":1},
#     {"id":46, "name":"Morningstar", "type":"martial_melee_weapon", "cost":150000, "weight":4, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:09:00", "updated_at":"2023-01-17 17:09:00", "img":"", "armor_id":0, "weapon_id":26, "user_id":1},
#     {"id":47, "name":"Pike", "type":"martial_melee_weapon", "cost":50000, "weight":18, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:10:56", "updated_at":"2023-01-17 17:10:56", "img":"", "armor_id":0, "weapon_id":27, "user_id":1},
#     {"id":48, "name":"Rapier", "type":"martial_melee_weapon", "cost":250000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:12:07", "updated_at":"2023-01-17 17:14:17", "img":"", "armor_id":0, "weapon_id":28, "user_id":1},
#     {"id":49, "name":"Scimitar", "type":"martial_melee_weapon", "cost":250000, "weight":3, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:13:26", "updated_at":"2023-01-17 17:13:26", "img":"", "armor_id":0, "weapon_id":29, "user_id":1},
#     {"id":50, "name":"Shortsword", "type":"martial_melee_weapon", "cost":100000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:16:20", "updated_at":"2023-01-17 17:16:20", "img":"", "armor_id":0, "weapon_id":30, "user_id":1},
#     {"id":51, "name":"Trident", "type":"martial_melee_weapon", "cost":50000, "weight":4, "description":"Thrown (range 20/60), versatile (ld8)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:18:10", "updated_at":"2023-01-17 17:18:10", "img":"", "armor_id":0, "weapon_id":31, "user_id":1},
#     {"id":52, "name":"War Pick", "type":"martial_melee_weapon", "cost":50000, "weight":2, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:19:13", "updated_at":"2023-01-17 17:19:13", "img":"", "armor_id":0, "weapon_id":32, "user_id":1},
#     {"id":53, "name":"Warhammer", "type":"martial_melee_weapon", "cost":150000, "weight":2, "description":"Versatile(1d10)", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:27:46", "updated_at":"2023-01-17 17:27:46", "img":"", "armor_id":0, "weapon_id":33, "user_id":1},
#     {"id":54, "name":"Whip", "type":"martial_melee_weapon", "cost":20000, "weight":3, "description":"", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:29:13", "updated_at":"2023-01-17 17:29:13", "img":"", "armor_id":0, "weapon_id":34, "user_id":1},
#     {"id":55, "name":"Blowgun", "type":"martial_ranged_weapon", "cost":100000, "weight":1, "description":"Ammunition (range 25/100), loading", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:33:25", "updated_at":"2023-01-17 17:37:25", "img":"", "armor_id":0, "weapon_id":35, "user_id":1},
#     {"id":56, "name":"Crossbow, hand", "type":"martial_ranged_weapon", "cost":750000, "weight":3, "description":"Ammunition (range 30/120), light, loading", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:36:52", "updated_at":"2023-01-17 17:36:52", "img":"", "armor_id":0, "weapon_id":36, "user_id":1},
#     {"id":57, "name":"Crossbow, heavy", "type":"martial_ranged_weapon", "cost":5000000, "weight":18, "description":"Ammunition (range 100/400), heavy, loading, two.handed", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:41:16", "updated_at":"2023-01-17 17:41:16", "img":"", "armor_id":0, "weapon_id":37, "user_id":1},
#     {"id":58, "name":"Longbow", "type":"martial_ranged_weapon", "cost":500000, "weight":2, "description":"Ammunition (range 150/600), heavy, two-handed", "rarity":"common", "source":"PHB", "is_magical":"no", "is_attunable":"no", "created_at":"2023-01-17 17:50:16", "updated_at":"2023-01-17 17:50:16", "img":"", "armor_id":0, "weapon_id":38, "user_id":1}]

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
    "MTF" : "Mordenkainen's Tome of Foes",
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
        print("\n__item get_all Method__")
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
        print("\n__item get_all by order Method__")
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
        print("\n____Get Item by Id method____")
        data = {"id" : id}
        query = "SELECT * FROM items LEFT JOIN weapons ON items.weapon_id = weapons.id LEFT JOIN armors ON items.armor_id = armors.id WHERE items.id=%(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        result = connectToMySQL(cls.DB).query_db(query,data)
       
        print("\n____The Result of get item by id is:_____",result)
        # Create an empty list to append our instances of friends
        a_item = cls(result[0])
        print("\n___ a_item after cls(result[0])", a_item)
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
        print("")
        # Iterate over the db results and create instances of friends with cls.
        return a_item
    
    
    @classmethod
    def save(cls, data ):
        print("")
        print("__item Save Method__")
        print(f"data: {data}")
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