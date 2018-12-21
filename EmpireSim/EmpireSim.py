class Asset:
    """Items for empires"""

    #Type includes location, army, support, object
    def __init__(self, name="name", type="none", strength=0, defense=0, hp=0, cunning=0, upkeep=0, cost=0):
        self.name = name
        self.type = type
        self.strength = strength
        self.defense = defense
        self.maxHp = hp
        self.cunning = cunning
        self.upkeep = upkeep
        self.cost = cost
        self.hp = self.maxHp

class Empire:
    """Manages the empire"""

 
    def __init__(self, name="name", assets = [], affinities=[], initHp=0, initStrength=0, initCunning=0, credits=0):
        self.name = name
        self.assets = assets
        self.afinities = affinities
        self.hp = initHp
        self.strength = initStrength
        self.cunning = initCunning
        self.credits = credits
        if (credits <= 0):
            self.bankrupt = True;
        else:
            self.bankrupt = False;

    def addAsset(self, newAsset):
        self.assets.append(newAsset);

    def getAssetSummaryString(self):
        return self.name + " Asset Summary:" + "\n" + ", ".join(x.name for x in self.assets)

    def getStrength(self):
        str = self.strength
        for a in self.assets:
            str += a.strength
        return str 
    
    def getCunning(self):
        cunning = self.cunning
        for a in self.assets:
            cunning += a.cunning
        return cunning 

    def getUpkeep(self):
        upk = 0;
        for a in self.assets:
            upk += a.upkeep
        return upk

    def getHp(self):
        hp = self.hp
        for a in self.assets:
            hp = a.upkeep
        return hp

    def changeCredits(self, netCreds = 0):
        creds = self.credits + netCreds
        if (creds <= 0):
            self.bankrupt = True;
            
    def runUpkeep(self):
        self.changeCredits(-1 * self.getUpkeep())

    def isBankrupt(self):
        return self.bankrupt
        
humanEmpire = Empire("Human Conglomerate",[],[], 50, 50, 50, 10)
humanEmpire.addAsset(Asset("Well of Eternity", "location",50,50,50,50,50,50))
humanEmpire.addAsset(Asset("Marshall Fedder", "army", 50))
humanEmpire.addAsset(Asset("Sword of the Well of Eternity","object", 50))


print(humanEmpire.getAssetSummaryString())
print("Human Empire Strength: " + str(humanEmpire.getStrength()))
print("Human Empire Credits: " + str(humanEmpire.credits))
humanEmpire.runUpkeep();
if (humanEmpire.isBankrupt()):
    print("Human Empire is bankrupt!")
