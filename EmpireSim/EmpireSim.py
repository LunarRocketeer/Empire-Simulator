class Asset:
    """Things that empires own, be they places, objects, armies, etc.  Sum up to Empire's score in different categories"""

    
    def __init__(self, name="newAsset", type="none", strength=0, defense=0, hp=0, cunning=0, upkeep=0, cost=0, importance=0, empireID = 0):
        self.name = name #objects name
        self.type = type #place, person, object, army
        self.strength = strength #attack points
        self.defense = defense #defense points
        self.maxHp = hp #maximum health points
        self.hp = self.maxHp #current hp
        self.cunning = cunning #points for stealth, espionage, research
        self.upkeep = upkeep #cost to run, per turn
        self.cost = cost #cost to buy        
        self.importance = importance #more important assets can only be attacked with higher world tension score; less important assets will be sold off first, after bankruptcy
        self.empireID = empireID #keep track of which emprie the asset belongs to

class Empire:
    """Stores data about each Empire"""

    def __init__(self, name="newFaction", assets=[], affinities=[], initStrength=0, initCunning=0, credits=0):
        self.name = name #empire name
        self.assets = assets #array of Empire's assets 
        self.affinities = affinities #array of Empire's relationship with other empires
        self.strength = initStrength #base strength, to be added to strength of all assets
        self.cunning = initCunning #base cunning, to be added to strength of all assets
        self.credits = credits #Empire's money

        #decides if empire is bankrupt
        if (credits <= 0):
            self.bankrupt = True
        else:
            self.bankrupt = False

    #Adds a new asset to the asset array
    def addAsset(self, newAsset):
        self.assets.append(newAsset);

    #Returns all assets' names as a single string
    def getAssetSummaryString(self):
        return self.name + " Asset Summary:" + "\n" + ", ".join(x.name for x in self.assets)

    #Sums the strength of all assets, and adds to initial strength
    def getStrength(self):
        str = self.strength
        for a in self.assets:
            str += a.strength
        return str 
    
    #Sums the cunning of all assets, and adds to initial cunning
    def getCunning(self):
        cunning = self.cunning
        for a in self.assets:
            cunning += a.cunning
        return cunning 

    #Sums the upkeep of all assets
    def getUpkeep(self):
        upk = 0;
        for a in self.assets:
            upk += a.upkeep
        return upk

    #Sums the hp of all assets, and adds initial hp
    def getHp(self):
        hp = 0
        for a in self.assets:
            hp += a.hp
        return hp

    #Adds or removes credits from Empire's coffers
    #Calculates if change in credits results in bankruptcy or escaping bankruptcy
    def changeCredits(self, netCreds = 0):
        creds = self.credits + netCreds
        if (creds <= 0):
            self.bankrupt = True
        else:
            self.bankrupt = False
    
    #Changes an Empire's credits based on the upkeep of its assets        
    def runUpkeep(self):
        self.changeCredits(-1 * self.getUpkeep())

    #Returns true if total credits is equal to or less than 0
    def isBankrupt(self):
        return self.bankrupt

class World:
    """Stores Empires, Assets, and other stats for a game."""

    def __init__(self, name="newWorld", worldTension=0, empires=[], assets=[], turnCount = 0):
        self.turnCount = turnCount #sets the gamee's time counter
        self.name = name #sets the world name
        self.worldTension = worldTension #events that are allowed to happen adapt with rising world tension
        self.empires = empires #stores the array of factions
        self.assets = assets #stores the array of assets

import sys
import csv
world = World()

humanEmpire = Empire("Human Conglomerate",[],[], 50, 50, 10)
humanEmpire.addAsset(Asset("Well of Eternity", "location",50,50,50,50,50,50))
humanEmpire.addAsset(Asset("Marshall Fedder", "army", 50))
humanEmpire.addAsset(Asset("Sword of the Well of Eternity","object", 50))


print(humanEmpire.getAssetSummaryString())
print("Human Empire Strength: " + str(humanEmpire.getStrength()))
print("Human Empire Credits: " + str(humanEmpire.credits))
humanEmpire.runUpkeep()
if (humanEmpire.isBankrupt()):
    print("Human Empire is bankrupt!")

def newWorld():
    print("Creating new world...")

"""Allows user to choose a .csv file, which is parsed and loaded into a World object"""
def loadWorld():
    print("Choose your world:")
    ##Gets list of files in local directory, filters out non csvs and inserts into list
    import os
    f = os.listdir()
    worlds = ["GO BACK    "]
    for files in f:
        if (files.lower().endswith(".csv")):
            worlds.append(files)
    
    #prints list of possible worlds for user to choose from
    for ind, w in enumerate(worlds):
        print(str(ind) + ". " + w.upper()[0:-4])

    #prompts user for input
    menu = True
    file = 0
    world = 0
    while(menu):
        inp = input()
        try:
            if int(inp) == 0:
                menu = False
            if int(inp) > 0 and int(inp) <= len(worlds):
                file = worlds[int(inp)]
                world = World(file[0:-4])
                menu = False
                print("World name: " + world.name.upper())
            else:
                print("Please enter valid input.")
        except:
            print("Please enter valid input.")
            pass

    #populate World with data from chosen csv
    path = os.path.dirname(os.path.realpath(__file__)) + "\\" + file
    reader = csv.reader(open(path, newline='', encoding='utf-8-sig'))

    #first row is non-repeating data [worldName, assetRow, worldTension, turnCount]
    firstRow = 0
    assetRow = 0 #tells the csv parser when to start making assets instead of empires
    try:
        firstRow = next(reader)
        world.name = firstRow[0]
        assetRow = int(firstRow[1])
        world.worldTension = int(firstRow[2])
        world.turnCount = int(firstRow[3])
    #will return to main menu if file does not have this telltale header data
    except:
        print("There is nothing in this file.")
        print()
        pass
    #loads repeating data (empires and assets) into world file
    for i, r in enumerate(reader):
            #populate Empires
            if (i < assetRow):
                #[name, affinities=[], strength, cunning, credits=0]
                world.empires.append(Empire(r[0],[], int(r[1]), int(r[2]), int(r[3])))
                world.empires[i].changeCredits(int(r[4]))
                ##TODO: load affinity array 
            #populate assets
            else:
                #[name, type, strength, defense, hp, cunning, upkeep, cost, importance, empireID]
                world.empires[int(r[9])].addAsset(Asset(r[0], r[1], int(r[2]), int(r[3]), int(r[4]), int(r[5]), int(r[6]), int(r[7]), int(r[8]), int(r[9])))
                print(world.empires[int(r[9])].getAssetSummaryString())
   

menu = True
while(menu):
    print("Hello, welcome to Empire Builder.  Please enter input.")
    print("1. New World")
    print("2. Load World")
    print("3. Quit")

    inp = input()
    if inp == "1":
        newWorld()
    elif inp == "2":
        loadWorld()
    elif inp == "3":
        print("Have a lovely day!")
        sys.exit()
    else:
        print("Invalid input.")

