from random import randint
import copy
map=[]
room=[]
creatures =[]
objects =[]
clearScreen = True
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
                        user.damage = user.damage+self.stats[stats]
            user.inventory.remove(self)

class entity:
    "Any type of creature"
    gold =0
    x=3
    y=3
    def __init__(self,health:int,damage:int,sprite:str,name:str,tags:set):
        self.health = health
        self.damage = damage
        self.sprite = sprite
        self.name = name
        self.tags = tags
        self.inventory= []
        self.equipment={}
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
        self.inventory.remove(item)
        self.equipment[slot]=item

    def printEquipment(self,itmeSlot:str):
        "prints an equipped items"
        if self.equipment[itmeSlot]!=None:
            print("("+itmeSlot+"): "+ self.equipment[itmeSlot].name)
        else:
            print("("+itmeSlot+"): empty")

    def inventoryCheck(self):
        "Prints out the entities inventory"
        print(chr(27) + "[2J")
        i=0
        for x in self.inventory:
            print ("("+str(i)+") "+x.name)
            i=i+1

    def getAttack(self):
        "gets the attack value of the creature"
        attack=self.damage
        for i in list(self.equipment.values()):
            if i:
                if "attack" in i.stats:
                    attack=attack+i.stats["attack"]
        return attack

    def autoEquip(self):
        "auto equips items for monsters WIP"
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
        "Kills the creature"
        global creatures
        while len(self.inventory)>0:
            self.drop(self.drop(self.inventory[0]))
        if self.gold>0:
            self.drop(item({self.gold},{},"gold","g"))
        creatures.remove(self)
    
    def drop(self, item):
        "Dropps the item"
        item.x=self.x
        item.y=self.y
        if(item.name!="gold"):
            self.inventory.remove(item)
        else:
            self.gold=0
        objects.append(item)


creaturePreset = {
    "rat":  entity(2,1,"~","Rat",{"monster"}),
    "skeleton":  entity(4,3,"|","Skeleton",{"monster","grabby","humanoid"}),
    "zombie":  entity(6,2,"Z","Zombie",{"monster","grabby","humanoid"}),
    "slime":  entity(3,2,"o","Slime",{"monster"})
}

itemPreset = {
    "helmet":  item({"helmet","equip"},{"defense":1},"Helmet","^"),
    "chainmail":  item({"armor","equip"},{"defense":1},"Chainmail","Y"),
    "boots":  item({"shoes","equip"},{"defense":1},"Boots","_"),
    "sword":  item({"handL","handR","equip"},{"attack":1},"Sword","/"),
    "potion": item({"potion"},{"health":8},"healing potion","Ö")
}

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
            case "D":
                if "player" in creature.tags:
                    newRoom()
            case _: 
                interact = checkEntity(creature.x+x,creature.y+y)
                if isinstance(interact, entity):
                    creatureInteract(creature, interact)
                elif isinstance(interact,item):
                    if interact.name=="gold":
                        creature.gold=creature.gold+next(iter(interact.tags))
                    else:
                        creature.inventory.append(interact)
                        #if "monster" in creature.tags:
                            #creature.autoEquip()
                    objects.remove(interact)

                
    return(0)

def creatureInteract(creature :entity, interact):
    "A method that handles interactions between two creatures"
    tempList=[]
    monster= None
    if "player" in creature.tags:
        monster=interact
    else:
        monster=creature
    tempList.append(monster)
    c=checkEntity(monster.x+1,monster.y)
    if isinstance(c, entity):
        if("monster" in c.tags):
            tempList.append(c)
    c=checkEntity(monster.x-1,monster.y)
    isMonster(tempList, c)
    c=checkEntity(monster.x,monster.y+1)
    isMonster(tempList, c)
    c=checkEntity(monster.x,monster.y-1)
    isMonster(tempList, c)
    combat(tempList)

def isMonster(tempList, c):
    "is c a monster returns bool"
    if isinstance(c, entity):
        if("monster" in c.tags):
            tempList.append(c)

def attack(defender: entity,attacker:entity):
    "The attacker attacks the defender"
    dead = 0
    attackDamage=attacker.getAttack()
    defender.health = defender.health - attackDamage
    if attacker == creatures[0]:
        print("You attacked " + defender.name + " for " + str(attackDamage) + " damage!")
    elif defender == creatures[0]:
        print(attacker.name + " attacked you for " + str(attackDamage) + " damage!")
        print("You're left with " + str(defender.health) + "HP")
    else:
        print(attacker.name + " attacked " + defender.name + " for" + str(attackDamage) + " damage!")
    if defender.health <= 0:
        print(defender.name + " died")
        dead = dead + 1
    return(dead)

def mapUpdate():
    "Updates the map based on current creatures"
    global map
    map=copy.deepcopy(room)
    for i in creatures:
        map[i.y][i.x]=i.sprite
    for i in objects:
        map[i.y][i.x]=i.sprite
    map[len(map)-2][len(map[0])-2]="D"  

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
            objectPlacement(y, x, tempObject)
            objects.append(copy.deepcopy(tempObject))
        case 1|2:
            tempObject=item({randint(10,30)},{},"gold","g")
            objectPlacement(y, x, tempObject)
            objects.append(copy.deepcopy(tempObject))
        case _:
            tempObject=list(creaturePreset.values())[randint(0,len(creaturePreset)-1)]
            objectPlacement(y, x, tempObject)
            creatures.append(copy.deepcopy(tempObject))
            creatures[-1].gold=randint(5,25)

def objectPlacement(y, x, tempObject):
    "Places tempObject at x,y"
    tempObject.x=randint(1,x-1)
    tempObject.y=randint(1,y-1)
    if tempObject.x<3 and tempObject.y<3:
        tempObject.x=3
    if tempObject.x==x and tempObject.y==y:
        tempObject.x=x-1

def useItem():
    #uses the item
    creatures[0].inventoryCheck()
    itemInput=input("write the number of the item:")
    if itemInput.isdigit():
        if int(itemInput)<len(creatures[0].inventory) and int(itemInput)>=0:
                creatures[0].useItem(creatures[0].inventory[int(itemInput)])

def printMonsterStats(monsterList):
    #prints the current health and attack for each present monster in combat
    for monster in monsterList:
        print("(1) " + str(monster.name) + " health: " + str(monster.health))
        print("    " + str(monster.name) + " attack: " + str(monster.damage))

def attackMonster(monsterList: list):
    "attacks the monsters in the list"
    inp = None
    if len(monsterList) > 1:
        while inp == None:
            print("Choose who to attack!")
            i=1
            for monster in monsterList:
                print( str(i)+ ") " + monster.name)
                i=i+1
            i=1
            inp = input("")
            print(chr(27) + "[2J")
            for monster in monsterList:
                if inp == str(i):
                    inp == "break"
                    if attack(monster,creatures[0]) == 1:
                        monsterList.remove(monster)
                        monster.kill()
                    return
                i=i+1
            if inp != "break":
                inp = None
                print("invalid input")
    
    elif attack(monsterList[0],creatures[0]) == 1:
            monster=monsterList[0]
            monsterList.remove(monster)
            monster.kill()
            global clearScreen
            clearScreen = False
            return "combatEnd"

def playerTurn(monsterList: list):
    #Player's turn in combat against at least monster1
    action = None
    print("It's your turn!")
    while action not in ["1", "2", "3", "4"]:
        print("What will you do?")
        print("1) ATTACK")
        print("2) USE ITEM")
        print("3) CHECK MONSTER STATS")
        print("4) FLEE")
        action = input("")
        print(chr(27) + "[2J")
        match action:
            case "1":
                if attackMonster(monsterList)=="combatEnd":
                    return "combatEnd"
            case "2":
                useItem()
            case "3":
                printMonsterStats(monsterList)
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
        
def monsterTurn(monsterList : list):
    #monsters turn, where each monster attacks the player 
    for monster in monsterList:
        if attack(creatures[0],monster) == 1:
            print("Gold:"+ f'{creatures[0].gold}')
            creatures[0].kill()
            return("gameOver")

def combat(monsterList: list):
    #The player fights up to 4 monsters
    print(chr(27) + "[2J")
    fightString = ("You are fighting "+ monsterList[0].name)
    for monster in monsterList[1:]:
        if monster == monsterList[-1]:
            fightString = fightString + " and " + monster.name
        else:
            fightString = fightString + ", " + monster.name
    print(fightString+"!")
    fighting = True
    while fighting:
        playerTurnResult = playerTurn(monsterList)
        if playerTurnResult == "combatEnd" or monsterTurn(monsterList) == "gameOver":
            fighting = False

def newRoom():
    "generates a new room"
    global room
    a=creatures[0]
    creatures.clear()
    objects.clear()
    a.x=1
    a.y=1
    creatures.append(a)
    room=generateFloor(["large","medium","small"][randint(0,2)])

#Main game loop
creatures.append(entity(20,3,"I","John Dungeon",{"player","grabby","humanoid"}))
creatures[0].inventory.append(copy.deepcopy(itemPreset["potion"]))
creatures[0].inventory.append(copy.deepcopy(itemPreset["potion"]))
creatures[0].x=1
creatures[0].y=1
print(chr(27) + "[2J")
room=generateFloor(["large","medium","small"][randint(0,2)])
while "player" in creatures[0].tags:
    monsterAction=True
    mapUpdate()
    roomPrint(map)
    clearScreen=True
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
            print(chr(27) + "[2J")
            print(creatures[0].gold)
            clearScreen=False
            monsterAction=False
        case "health":
            print(chr(27) + "[2J")
            print(creatures[0].health)
            clearScreen=False
            monsterAction=False
        case "equip":
            print(creatures[0].equipment)
            clearScreen=False
            monsterAction=False
        case "inventory":
            if len(creatures[0].inventory)<1:
                print("Your inventory is empty")
            else:
                creatures[0].inventoryCheck()
            clearScreen=False
            monsterAction=False
        case "item":
            creatures[0].inventoryCheck()
            itemInput=input("write the number of the item:")
            if itemInput.isdigit():
                if int(itemInput)<len(creatures[0].inventory) and int(itemInput)>=0:
                    creatures[0].useItem(creatures[0].inventory[int(itemInput)])
            monsterAction=False
        case "help":
            print(chr(27) + "[2J")
            monsterAction=False
            print("You are the \'I\' you can use the following commands:")
            print("\'w\',\'a\',\'s\' and \'d\' for movement")
            print("\'inventory\' to check your inventory")
            print("\'item\' to use or equip an item")
            print("\'gold\' to check your gold")
            print("________________________________________________________")
            print("The map icons means the following:")
            print("\'X\' = Wall")
            print("\'g\' = Gold")
            print("\'D\' is the door to the next room")
            print("\'o\', \'~\', \'|\' and \'Z\' are different types of enemies that chase you")
            print("the rest are items")
            input("Write anything to continue")
    if clearScreen:
        print(chr(27) + "[2J")

    mapUpdate()
    if monsterAction:
        monsterMove(creatures[0].x,creatures[0].y)
print
    