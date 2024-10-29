#creatures[0] placeholder for player
import random
import copy
class entity:
    #"Any type of creature"
    def __init__(self,health,damage,x,y,sprite,name):
        self.health = health
        self.damage = damage
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name = name
creatures =[]
#Buffed the player to survive combat againts 4 creatures (for the demo)
creatures.append(entity(30,3,1,1,"I","Humanperson"))

creaturePreset = {
    "rat":  entity(2,1,3,3,"o","Rat"),
    "skeleton":  entity(4,3,3,3,"|","Skeleton"),
    "zombie":  entity(6,2,3,3,"Z","Zombie")
}

def attack(defender,attacker):
    #"The attacker attacks the defender"
    dead = 0
    defender.health = defender.health - attacker.damage
    if attacker == creatures[0]:
        print("You attacked " + defender.name + " for " + str(attacker.damage) + " damage!")
    elif defender == creatures[0]:
        print(attacker.name + " attacked you for " + str(attacker.damage) + " damage!")
        print("You're left with " + str(defender.health) + "HP")
    else:
        print(attacker.name + " attacked " + defender.name + " for" + str(attacker.damage) + " damage!")
    if defender.health <= 0:
        print(defender.name + " died")
        creatures.remove(defender)
        dead = dead + 1
    return(dead)

def useItem():
    #Items don't exist yet
    print("items don't exist yet")

def printMonsterStats(monster1, monster2=None, monster3=None, monster4=None):
    #prints the current health and attack for each present monster in combat
    print("(1) " + str(monster1.name) + " health: " + str(monster1.health))
    print("    " + str(monster1.name) + " attack: " + str(monster1.damage))
    if monster2 != None:
        print("(2) " + str(monster2.name) + " health: " + str(monster2.health))
        print("    " + str(monster2.name) + " attack: " + str(monster1.damage))
    if monster3 != None:
        print("(3) " + str(monster3.name) + " health: " + str(monster3.health))
        print("    " + str(monster3.name) + " attack: " + str(monster3.damage))
    if monster4 != None:
        print("(4) " + str(monster4.name) + " health: " + str(monster4.health))
        print("    " + str(monster4.name) + " attack: " + str(monster4.damage))

def playerTurn(monster1, monster2=None, monster3=None, monster4=None):
    #Player's turn in combat against at least monster1
    action = None
    inp = None
    print("It's your turn!")
    while action not in ["1", "2", "3", "4"]:
        print("What will you do?")
        print("1) ATTACK")
        print("2) USE ITEM")
        print("3) CHECK MONSTER STATS")
        print("4) FLEE")
        action = input("")
        if action == "1":
            if monster2 != None:
                while inp == None:
                    print("Choose who to attack!")
                    print("1) " + monster1.name)
                    print("2) " + monster2.name)
                    if monster3 != None:
                        print("3) " + monster3.name)
                    if monster4 != None:
                        print("4) " + monster4.name)
                    inp = input("")
                    if inp == "1":
                        if attack(monster1,creatures[0]) == 1:
                            return("1dead")
                    elif inp == "2":
                        if attack(monster2,creatures[0]) == 1:
                            return("2dead")
                    elif inp == "3" and monster3 != None:
                        if attack(monster3,creatures[0]) == 1:
                            return("3dead")
                    elif inp == "4" and monster4 != None:
                        if attack(monster4,creatures[0]) == 1:
                            return("4dead")
                    else:
                        inp = None
                        print("invalid input")
                        print("")
            else:
                if attack(monster1,creatures[0]) == 1:
                    return("combatEnd")
        elif action == "2":
            useItem()
        elif action == "3":
            printMonsterStats(monster1, monster2, monster3, monster4)
        elif action == "4":
            print("attempting to flee...")
            if random.randint(0,1) == 1:
                print("you've fled successfully!")
                return("combatEnd")
            else:
                print("you where unsuccessfull in you attempt")
        else:
            action = "invalid"
            print("invalid input")

def monsterTurn(monster1, monster2=None, monster3=None, monster4=None):
    #monsters' turn, where each monster attacks the player 
    if attack(creatures[0],monster1) == 1:
        return("gameOver")
    if monster2 != None:
        if attack(creatures[0],monster2) == 1:
            return("gameOver")
        if monster3 != None:
            if attack(creatures[0],monster3) == 1:
                return("gameOver")
            if monster4 != None:
                if attack(creatures[0],monster4) == 1:
                    return("gameOver")
                

def combat(monster1, monster2=None, monster3=None, monster4=None):
    #The player fights up to 4 monsters
    if monster2 == None:
        print("You are fighting " + monster1.name + "!")
    elif monster3 == None:
        print("You are fighting " + monster1.name + " and " + monster2.name + "!")
    elif monster4 == None:
        print("You are fighting " + monster1.name + ", " + monster2.name + " and " + monster3.name + "!")
    else:
        print("You are fighting " + monster1.name + ", " + monster2.name + ", " + monster3.name + " and " + monster4.name + "!")
    fighting = 1
    while fighting:
        playerTurnResult = playerTurn(monster1, monster2, monster3, monster4)
        if playerTurnResult == "combatEnd":
            fighting = 0
        if playerTurnResult == "1dead" or playerTurnResult == "combatEnd":
            monster1 = None
            monster1 = monster2
            monster2 = None
            if monster3 != None:
                monster2 = monster3
                if monster4 != None:
                    monster3 = monster4
                    monster4 = None
                else:
                    monster3 = None
        elif playerTurnResult == "2dead":
            monster2 = None
            if monster3 != None:
                monster2 = monster3
                if monster4 != None:
                    monster3 = monster4
                    monster4 = None
                else:
                    monster3 = None
        elif playerTurnResult == "3dead":
            monster3 = None
            if monster4 != None:
                monster3 = monster4
                monster4 = None
        elif playerTurnResult == "4dead":
            monster4 = None
        if monster1 != None and playerTurnResult != "combatEnd":
            if monsterTurn(monster1, monster2, monster3, monster4) == "gameOver":
                fighting = 0
    

#creature defining
ARat = copy.deepcopy(creaturePreset["rat"])
creatures.append(ARat)
AZombie = copy.deepcopy(creaturePreset["zombie"])
creatures.append(AZombie)
AnoZombie = copy.deepcopy(creaturePreset["zombie"])
creatures.append(AnoZombie)
Skeletone = copy.deepcopy(creaturePreset["skeleton"])
creatures.append(Skeletone)
 
#combat
combat(AZombie, ARat, AnoZombie, Skeletone)
   
