from random import randint
import copy
class item:
    x=0
    y=0
    def __init__(self,tags:set,stats:dict,name:str,sprite:str):
        self.tags=tags
        self.name=name
        self.sprite=sprite
        self.stats=stats
    def use(self, user):
        "uses the item if possible"
        if "potion" in self.tags:
            for stats in self.stats:
                match stats:
                    case "health":
                        user.health = user.health+self.stats[stats]
                    case "attack":
                        user.attack = user.attack+self.stats[stats]

class entity:
    "Any type of creature"
    equipment = {}
    inventory = []
    gold =0
    x=3
    y=3
    def __init__(self,health:int,damage:int,sprite:str,name:str,tags:set):
        self.health = health
        self.damage = damage
        self.sprite = sprite
        self.name = name
        self.tags = tags
        if "humanoid" in tags:
            self.equipment =  {
                "helmet":None,
                "armor":None,
                "pants":None,
                "handL":None,
                "handR":None,
                "shoes":None                
        }
    
    def equip(self,item:item,slot:str):
        "equpis a item"
        if self.equipment[slot]!=None:
            self.inventory.append(self.equipment[slot])
        self.equipment[slot]=item

    def printEquipment(self,itmeSlot:str):
        "prints an equipped items"
        if self.equipment[itmeSlot]!=None:
            print("("+itmeSlot+"): "+ self.equipment[itmeSlot].name)
        else:
            print("("+itmeSlot+"): empty")

    def inventoryCheck(self):
        i=0
        for x in self.inventory:
            print ("("+str(i)+") "+x.name)
            i=i+1

    def getAttack(self):
        attack=self.damage
        for i in list(self.equipment.values()):
            if i:
                if "attack" in i.stats:
                    attack=attack+i.stats["attack"]
        return attack

    def autoEquip(self):
        for item in self.inventory:
            for tag in item.tags:
                if tag in self.equipment:
                    if self.equipment[tag]==None:
                        self.equipment[tag]=item
                        self.inventory.remove(item)
    


    def useItem(self, item:item):
        "lets you equip an item"
        if "equip" in item.tags:
            print("Which slot do you want to equip "+ item.name +" in")
            for itemTags in item.tags:
                if itemTags in self.equipment:
                    self.printEquipment(itemTags)
            inputSlot=input()
            if inputSlot in item.tags and inputSlot in self.equipment:
                self.equip(item,inputSlot)
        else:
            item.use(self)

    def kill(self):
        global creatures
        for x in self.inventory:
            self.drop(x)
        if self.gold>0:
            self.drop(item({self.gold},{},"gold","g"))
        creatures.remove(self)
    
    def drop(self, item):
        item.x=self.x
        item.y=self.y
        if(item.name!="gold"):
            self.inventory.remove(item)
        else:
            self.gold=0
        objects.append(item)
            
creatures =[]
objects =[]

creatures.append(entity(10,2,"I","John Dungeon",{"player","grabby","humanoid"}))
creatures[0].x=1
creatures[0].y=1
creaturePreset = {
    "rat":  entity(2,1,"~","Rat",{"monster"}),
    "skeleton":  entity(4,3,"|","Skeleton",{"monster","grabby","humanoid"}),
    "zombie":  entity(6,2,"Z","Zombie",{"monster","grabby","humanoid"}),
    "slime":  entity(3,2,"o","Slime",{"monster"})
}

itemPreset = {
    "helmet":  item({"helmet","equip"},{"defense":1},"Bucket","^"),
    "chainmail":  item({"armor","equip"},{"defense":1},"bunch of rings","Y"),
    "boots":  item({"shoes","equip"},{"defense":1},"boot","_"),
    "sword":  item({"handL","handR","equip"},{"attack":1},"big knife","/"),
    "potion": item({"potion"},{"health":2},"healing potion","Ö")
}


map=[]
room=[]
def roomPrint(room):
    "Prints the room that is provided"
    for i in room:
        print(i)

def roomCreator(x: int,y:int):
    "Creates a list[][] that's x spaces wide and y spaces high"
    room=[]
    for i in range(y):
        temp=[]
        for j in range(x):
            if j==0 or j==x-1 or i==0 or i==y-1:
                temp.append("X")
            else:
                temp.append(" ")    
        room.append(temp)
    return room

def move(x:int,y:int,creature:entity):
    "Attempts to move the creature x spaces horizontaly, y spaces vertically"
    global map
    global creatures
    if x!=0 or y!=0:
        match map[creature.y+y][creature.x+x]:
            case "X":
                print("WALL")
            case " ":
                creature.y=creature.y+y
                creature.x=creature.x+x
            case _: 
                interact = checkEntity(creature.x+x,creature.y+y)
                if isinstance(interact, entity):
                    if(creature==creatures[0]):
                        tempList=[]
                        tempList.append(interact)
                        c=checkEntity(interact.x+1,interact.y)
                        if isinstance(c, entity):
                            if("monster" in c.tags):
                                tempList.append(c)
                        c=checkEntity(interact.x-1,interact.y)
                        if isinstance(c, entity):
                            if("monster" in c.tags):
                                tempList.append(c)
                        c=checkEntity(interact.x,interact.y+1)
                        if isinstance(c, entity):
                            if("monster" in c.tags):
                                tempList.append(c)
                        c=checkEntity(interact.x,interact.y-1)
                        if isinstance(c, entity):
                            if("monster" in c.tags):
                                tempList.append(c)
                        match(len(tempList)):
                            case 1:
                                combat(interact)
                            case 2:
                                combat(interact,tempList[1])
                            case 3:
                                combat(interact,tempList[1],tempList[2])
                            case 4:
                                combat(interact,tempList[1],tempList[2],tempList[3])
                    else:
                        combat(creature)
                elif isinstance(interact,item):
                    if interact.name=="gold":
                        creature.gold=creature.gold+next(iter(interact.tags))
                    else:
                        creature.inventory.append(interact)
                        #if "monster" in creature.tags:
                            #creature.autoEquip()
                    objects.remove(interact)

                
    return(0)

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
#def attack(defender:entity,attacker:entity):
    "The attacker attacks the defender"
    dead=0
    defender.health=defender.health-attacker.getAttack()
    print(attacker.name + " dealt " + str(attacker.getAttack()) + " damage. Leaving " + defender.name + " with " + str(defender.health) + " health remaining")
    attacker.health=attacker.health-defender.getAttack()
    print(defender.name + " dealt " + str(defender.getAttack()) + " damage. Leaving " + attacker.name + " with " + str(attacker.health) + " health remaining")
    if defender.health<=0:
        print(defender.name+" died")
        defender.kill()
        dead=dead+1
    if attacker.health<=0:
        print(attacker.name+" died")
        attacker.kill()
        dead=dead+1
    return(dead)

def mapUpdate():
    "Updates the map based on current creatures"
    global map
    map=copy.deepcopy(room)
    for i in creatures:
        map[i.y][i.x]=i.sprite
    for i in objects:
        map[i.y][i.x]=i.sprite    

def checkEntity(x:int,y:int):
    "Checks what entity is at x,y"
    for i in creatures:
        if y==i.y and x==i.x:
            return i
    for i in objects:
        if y==i.y and x==i.x:
            return i
    return -1

def possibleMove(x:int,y:int,monster:entity):
    "Checks if the move is allowed"
    match(map[y][x]):
        case "X":
            return False
        case " ":
            return True
        case _:
            interact = checkEntity(x,y)
            if isinstance(interact, entity):
                if "monster" in monster.tags and "monster" in interact.tags :
                    return False
                else:
                    return True
            elif isinstance(interact,item) and "grabby" in monster.tags:
                return True

def monsterMove(x:int,y:int):
    "Attempts to move all creatures towards the provide x,y"
    global creatures
    global map
    i=1
    while i < len(creatures):
        monster = creatures[i]
        xMove=0
        yMove=0
        if x>monster.x and possibleMove(monster.x+1,monster.y,monster):
            xMove=1
        elif x<monster.x and possibleMove(monster.x-1,monster.y,monster):
            xMove=-1
        elif y>monster.y and possibleMove(monster.x,monster.y+1,monster):
            yMove=1
        elif y<monster.y and possibleMove(monster.x,monster.y-1,monster):
            yMove=-1
        i=i+1-move(xMove,yMove,monster)
        mapUpdate()

def generateFloor(size: str):
    "generates a new floor based on size preset"
    match(size):
        case "small":
            room =roomCreator(randint(6,8),randint(6,8))
            for i in range(0,3):
                createObject(len(room)-1, len(room[0])-1)
        case "medium":
            room =roomCreator(randint(9,10),randint(9,10))
            for i in range(0,5):
                createObject(len(room)-1, len(room[0])-1)
        case "large":
            room =roomCreator(randint(11,13),randint(11,13))
            for i in range(0,8):
                createObject(len(room)-1, len(room[0])-1)
    return room

def createObject(y:int,x:int):
    "creates an object at given space"
    match(randint(0,6)):
        case 0:
            tempObject=list(itemPreset.values())[randint(0,len(itemPreset)-1)]
            tempObject.x=randint(1,x-1)
            tempObject.y=randint(1,y-1)
            if tempObject.x<3 and tempObject.y<3:
                tempObject.x=3
            objects.append(copy.deepcopy(tempObject))
        case 1|2:
            tempObject=item({randint(20,80)},{},"gold","g")
            tempObject.x=randint(1,x-1)
            tempObject.y=randint(1,y-1)
            if tempObject.x<3 and tempObject.y<3:
                tempObject.x=3
            objects.append(copy.deepcopy(tempObject))
        case _:
            tempObject=list(creaturePreset.values())[randint(0,len(creaturePreset)-1)]
            tempObject.x=randint(1,x-1)
            tempObject.y=randint(1,y-1)
            if tempObject.x<3 and tempObject.y<3:
                tempObject.x=3
            creatures.append(copy.deepcopy(tempObject))

def useItem():
    #Items don't exist yet
    creatures[0].inventoryCheck()
    itemInput=input("write the number of the item:")
    if itemInput.isdigit():
        if int(itemInput)<len(creatures[0].inventory) and int(itemInput)>=0:
                creatures[0].useItem(creatures[0].inventory[int(itemInput)])

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
        match action:
            case "1":
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
            case "2":
                useItem()
            case "3":
                printMonsterStats(monster1, monster2, monster3, monster4)
            case "4":
                print("attempting to flee...")
                if randint(0,1) == 1:
                    print("you've fled successfully!")
                    return("combatEnd")
                else:
                    print("you where unsuccessfull in you attempt")
            case _:
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

#Main game loop
room=generateFloor("large")
creatures[2].inventory.append(copy.deepcopy(itemPreset["sword"]))
while "player" in creatures[0].tags:
    mapUpdate()
    roomPrint(map)
    match input():
        case "a":
            move(-1,0,creatures[0])
        case "d":
            move(1,0,creatures[0])
        case "w":
            move(0,-1,creatures[0])
        case "s":
            move(0,1,creatures[0])
        case "gold":
            print(creatures[0].gold)
        case "equip":
            print(creatures[0].equipment)
        case "inventory":
            creatures[0].inventoryCheck()
        case "item":
            creatures[0].inventoryCheck()
            itemInput=input("write the number of the item:")
            if itemInput.isdigit():
                if int(itemInput)<len(creatures[0].inventory) and int(itemInput)>=0:
                    creatures[0].useItem(creatures[0].inventory[int(itemInput)])
            
        case "restart":
            a=creatures[0]
            creatures.clear()
            objects.clear()
            creatures.append(a)
            generateFloor("large")

    mapUpdate()
    monsterMove(creatures[0].x,creatures[0].y)
    