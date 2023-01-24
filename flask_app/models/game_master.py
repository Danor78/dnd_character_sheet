import flask_app.models.character as character
import equipment




class Game_Master():
    
    def __init__(self):
        pass
    
    
    def roll_for_initiative(self, players_list, enemies_list):
        
        initiative_list = []
        for i in range(len(players_list)):
            initiative_list.append([players_list[i].roll_initiative(),players_list[i]])
        for i in range(len(enemies_list)):
            initiative_list.append([enemies_list[i].roll_initiative(),enemies_list[i]])
        
        for i in range(len(initiative_list)):
            initiative_list
            for ii in range(i, len(initiative_list)):
                if initiative_list[i][0] < initiative_list[ii][0]:
                    temp = initiative_list[i]
                    initiative_list[i] = initiative_list[ii]
                    initiative_list[ii] = temp
        
        for i in range(len(initiative_list)):
            print(f"Initiative #{initiative_list[i][0]}, for {initiative_list[i][1].my_name}")
        return initiative_list



pass


wizard = character.DnDPlayer('wizard')
fighter = character.DnDPlayer('fighter')
bard = character.DnDPlayer('bard')
monk = character.DnDPlayer('monk')
rouge = character.DnDPlayer('rouge')
barbarian = character.DnDPlayer('barbarian')
paladin = character.DnDPlayer('paladin')

gobin_1 = character.DnDPlayer('goblin 1')
gobin_2 = character.DnDPlayer('goblin 2')
gobin_3 = character.DnDPlayer('goblin 3')
gobin_4 = character.DnDPlayer('goblin 4')
gobin_5 = character.DnDPlayer('goblin 5')
gobin_6 = character.DnDPlayer('goblin 6')




wizard.equip_weapon(equipment.Weapon({"name" : 'Short Sword', "damage_die" : 6}))

wizard.melee_attack(fighter)

dan = Game_Master()

dan.roll_for_initiative([wizard,fighter,bard,monk,rouge,barbarian,paladin],[gobin_1,gobin_2,gobin_3,gobin_4,gobin_5,gobin_6])
# dan.roll_for_initiative([paladin],[gobin_6])

