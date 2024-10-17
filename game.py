from random import randint
import copy
class entity:
    "Any type of creature"
    def __init__(self,health,damage,x,y,sprite,name,sight):
        self.health = health
        self.damage = damage
        self.x = x
        self.y = y
        self.sprite = sprite
        self.name = name
        self.sight = sight
creatures =[]
creatures.append(entity(10,2,1,1,"I","Humanperson",6))

creaturePreset = {
    "Rat":  entity(2,1,3,3,"o","Rat",6),
    "Skeleton":  entity(4,3,3,3,"|","Skeleton",6),
    "Zombie":  entity(6,2,3,3,"Z","Zombie",6)
}

map=[]
creatures.append(copy.deepcopy(creaturePreset["Rat"]))
creatures.append(copy.deepcopy(creaturePreset["Skeleton"]))
creatures[2].x=2
def roomPrint(room):
    "Prints the room that's provided"
    for i in range(len(room)):
        print(room[i])

def roomCreator(x,y):
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

def move(x,y,creature):
    "Attempts to move the creature x spaces horizontaly, y spaces vertically"
    global map
    global creatures
    match map[creature.y+y][creature.x+x]:
        case "X":
            print("WALL")
        case " ":
            creature.y=creature.y+y
            creature.x=creature.x+x
        case _: 
            i = checkEntity(creature.x+x,creature.y+y)
            if i!=-1:
                return(attack(creatures[i],creature))
            

def attack(defender,attacker):
    "The attacker attacks the defender"
    dead=0
    defender.health=defender.health-attacker.damage
    print(attacker.name + " dealt " + str(attacker.damage) + " damage. Leaving " + defender.name + " with " + str(defender.health) + " health remaining")
    attacker.health=attacker.health-defender.damage
    print(defender.name + " dealt " + str(defender.damage) + " damage. Leaving " + attacker.name + " with " + str(attacker.health) + " health remaining")
    if defender.health<=0:
        print(defender.name+" died")
        creatures.remove(defender)
        dead=dead+1
    if attacker.health<=0:
        print(attacker.name+" died")
        creatures.remove(attacker)
        dead=dead+1
    return(dead)

def mapUpdate():
    "Updates the map based on current creatures"
    global map
    map=roomCreator(7,7)
    for i in range(len(creatures)):
        map[creatures[i].y][creatures[i].x]=creatures[i].sprite

def checkEntity(x,y):
    "Checks what entity is at x,y"
    for i in range(len(creatures)):
        if y==creatures[i].y and x==creatures[i].x:
            return i
    return -1

def monsterMove(x,y):
    "Attempts to move all creatures towards the provide x,y"
    global creatures
    global map
    for i in range(len(creatures)):    
        if (x-creatures[i].x)**2+(y-creatures[i].y)**2<=creatures[i].sight**2:
            if x>creatures[i].x:
                move(1,0,creatures[i])
            elif x<creatures[i].x:
                move(-1,0,creatures[i])
            elif y>creatures[i].y:
                move(0,1,creatures[i])
            elif y<creatures[i].y:
                move(0,-1,creatures[i])
        mapUpdate()

def spawner(name):
    x=randint(0,len(map)-1)
    y=randint(0,len(map[0])-1)
    creatures.append()

#Main game loop
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
        case "spawn enemy":
            spawner("Rat")
    mapUpdate()
    monsterMove(creatures[0].x,creatures[0].y)
    