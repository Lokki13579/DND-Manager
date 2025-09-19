import json
import os
from translate import *
Stats = {
	"class" : "",
	"race" : "",
	"level" : 0,
	"experience" : 0,
	"alingment" : "",
	"background" : "",
	"masterBonus" : "",
	"skills" : "",
	"diceStats" : "",
	"inventory" : "",
	"spells" : "",
	"otherData":{
		"learnedSpells" : 0,
		"learnedFocuses" : 0,
		"spellCells" : {
		"1": 0,
		"2":0,
		"3":0
		}
	},
	"lore" : ""
    }
characterPath = "AllCharacterData.json"  
class Character:
    def __init__(self,name = "Выбирается"):
        self.name = name
        self.Stats = {}
        self.maxExp = jsonLoad("JSONS/dnd_levels.json")[str(self.Stats.get("level",0)+1)].get("experience",300)
        self.status = dict(zip(jsonLoad("JSONS/dnd_statuses.json"),[False for i in range(15)]))
        self.spellCells = {"1": 4,
                           "2":4,
                           "3":3,
                           "4":3,
                           "5":3,
                           "6":2,
                           "7":2,
                           "8":1,
                           "9":1}
    def setName(self,newName):
        self.name = newName
    def setLevel(self,value):
        if value[0] in "+-":
            self.Stats["level"] += int(value)
        else:
            self.Stats["level"] = int(value)

        self.expReset(int(value))
        self.BMReset(int(value))
        self.skillReset(self.Stats["class"],int(value))
        self.initSpellCell()
    def setXp(self,value):
        if value[0] in "+-":
            self.Stats["experience"] += int(value)
        else:
            self.Stats["experience"] = int(value)
        self.expReset(self.Stats["level"])
        self.initSpellCell()
    def skillReset(self,cl,newLevel):
        self.Stats["skills"] = []
        for _level in range(int(newLevel),0,-1):
            self.Stats["skills"] += jsonLoad("JSONS/dnd_classes.json")[cl][str(_level)]["Умения"].split(", ")
        while "0" in self.Stats["skills"]:
            self.Stats["skills"].remove("0")
    def BMReset(self,newLevel):
        self.Stats["masterBonus"] = jsonLoad("JSONS/dnd_levels.json")[str(newLevel)]["BM"]
    def expReset(self,newLevel):
        lev = jsonLoad("JSONS/dnd_levels.json")[str(newLevel+1)]
        if self.Stats["experience"] > lev["experience"]:
            self.Stats["experience"] = 0
            self.Stats["level"] += 1
    def getStats(self):
        out = ""
        for k,v in self.Stats.items():
            out += "&" + k.center(15,"-") + "\n" + v.center(15) + "\n"
        return out
    def invMan(self,action,item = None):
        allItemlinks = {
            "JSONS/dnd_drugs.json":"drugs",
            "JSONS/dnd_giant_bag.json":"giantBag",
            "JSONS/dnd_magic_items.json":"magicItems",
            "JSONS/dnd_poisons.json":"poisons",
            "JSONS/dnd_trinkets.json":"trinkets"
            }
        allItems = []
        for file in allItemlinks:
            print(jsonLoad(file))
        if str(item) in allItems :
            pass
    def otherStatsReset(self):
        
        otherSt = {}
        classData = jsonLoad("JSONS/dnd_classes.json")[self.Stats["class"]]
        levelData = classData[str(self.Stats["level"])]
        for i in levelData:
             if i == "Умения":
                 continue
             if i == "DifferentSpellCells":
                 otherSt["MaxspellCells"] = {}
                 for spCell in levelData[i]:
                     print(spCell[-1])
                     otherSt["MaxspellCells"][spCell[-1]] = str(levelData[i][spCell])
                 continue
             if i == "Ячейки заклинаний" or i == "Уровень ячеек":
                 otherSt["MaxspellCells"] = {}
                 otherSt["MaxspellCells"][levelData["Уровень ячеек"]] = levelData["Ячейки заклинаний"]
                 continue
             otherSt[i] = levelData[i]
        if "formula" in classData:
             formula = classData["formula"].split(" ") + ["1"]
             otherSt["Известные заклинания"] = math.floor((int(self.Stats["diceStats"][formula[0]])-10)/2)+math.floor(self.Stats[formula[1]]/int(formula[2]))
             if otherSt["Известные заклинания"] < 1:
                 otherSt["Известные заклинания"] = 1
        self.Stats["otherStats"] = otherSt


    def setStats(self,st):
        self.Stats = st
        self.initSpellCell()
    def initSpellCell(self):
        try: 
            for key,val in self.Stats["otherStats"]["MaxspellCells"].items():
                self.spellCells[str(key)] = int(val)
        except KeyError:
            self.spellCells = {}
    def spellCellsCh(self,key,value):
        self.spellCells[key] += int(value)
        if int(self.Stats["otherStats"]["MaxspellCells"][key]) < int(value):
            self.spellCells[key] = int(self.Stats["otherStats"]["MaxspellCells"][key])
        elif int(self.spellCells[key]) < 0:
            self.spellCells[key] = 0
    def charSave(self,path=characterPath): 
        try:
            data = jsonLoad(path)
        except:
            data = {}
        print(self.name)
        print(data)
        data[self.name] = self.Stats
        with open(path,"w",encoding="utf-8") as file:
            json.dump(data,file, indent=4)
    def jsonCharDelete(self):
        oldData = jsonLoad()
        oldData.pop(self.name)
        self.jsonSave(oldData)
    def jsonSave(self,data,path = characterPath):
        with open(path,"w",encoding="utf-8") as file:
            json.dump(data,file)
class CharLoader:
    def __init__(self):
        self.allCharacters = {}
    def CharClassDispencer(self):
        for charData in jsonLoad():
            i = 1
            char = Character(charData)
            self.allCharacters["-" + str(i)] = char
        return self.allCharacters

def jsonLoad(path=characterPath):
    try: 
        with open(path,"r+",encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {} 
    return data

if __name__ == "__main__":
    character = Character()
    character.invMan("add")
