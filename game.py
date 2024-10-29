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
    def __init__(self,health:int,attack:int,sprite:str,name:str,tags:set):
        self.health = health
        self.attack = attack
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
        attack=self.attack
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
                    return(attack(interact,creature))
                elif isinstance(interact,item):
                    if interact.name=="gold":
                        creature.gold=creature.gold+next(iter(interact.tags))
                    else:
                        creature.inventory.append(interact)
                        if "monster" in creature.tags:
                            creature.autoEquip()
                    objects.remove(interact)

                
    return(0)
 
def attack(defender:entity,attacker:entity):
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

#Main game loop
room=generateFloor("large")
creatures[2].inventory.append(copy.deepcopy(itemPreset["sword"]))
while True:
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
    