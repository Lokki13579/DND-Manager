from pprint import pp
import random
from art import tprint
import math
from server_client import *
from panels import *
clearstr = "cls"
IP = gethostbyname(gethostname())
ServerOBJ = ServerClass()
ClientOBJ = Client()
#translateOBJ = jsonLoad("JSONS/translate.json")
class diceRandomer:
    def __init__(self):
        self.dices = [random.randint(1,6) for i in range(4)]
        self.dices.remove(min(self.dices))
        self.out = sum(self.dices)
    def _out(self):
        return self.out

class Button:
    def __init__(self,name = "<X> Кнопка <Х>", data = None):
        self.name = name
        self.data = data
    def _action(self):
        pass

class PlayerSelectButton(Button):
    def __init__(self,player):
        self.player = player
        super().__init__(player.character.name)
    def _action(self):
        addMenu("player"+self.player.character.name,PlayerCharacterMenu(self.player))
        manager("player"+self.player.character.name)
class CharacterSelectButton(Button):
    def __init__(self,character):
        self.char = character
        super().__init__(self.char.name)
    def _action(self):
        addMenu("play"+self.char.name,CharacterCharacteristicsMenu(self.char))
        ClientOBJ.sendToServer("characterNameChanged",self.char.name)
        ClientOBJ.sendToServer("newData",self.char.Stats,self.char.spellCells,self.char.status)
        ClientOBJ.character = self.char
        manager("play"+self.char.name)
class ExitButton(Button):
    def __init__(self,name = "Уйти"):
        super().__init__(name) 
    def _action(self):
        quit()
class MSB(Button):
    def _action(self):
        manager(self.data)
class CharButton(Button):
    def _action(self):
        addMenu(self.name,CharInfoMenu(self.name))
        manager(self.name) 
class CharRemoveButton(Button):
    def __init__(self,name = "Удалить персонажа",data = None):
        super().__init__(name,data)
    def _action(self):
        temp = Character(name=self.data)
        temp.jsonCharDelete()
        manager("charlist")
class ParamSelButton(Button):
    def _action(self):
        return self.name

class Menu:
    def __init__(self, name = " <Y> Менюшка <Y> ",rawButtons = []):
        self.name = name
        self.rawButtons = rawButtons
        self.buttonPrepare()
    def buttonPrepare(self):
        self.allButtons = {}
        i = 1
        for button in self.rawButtons:
            self.allButtons[i] = button
            i += 1
    def _update(self):
        os.system(clearstr)
        self.showName()
    def draw(self):
        self.buttonPrepare()
        os.system(clearstr)
        self.showName()
        self.showInfo()
        self.showButtons()
        self.GetAction()
    def showName(self):
        print(self.name)
    def showInfo(self):
        pass
    def showButtons(self):
        for buttonIndex in self.allButtons:
            print(str(buttonIndex) + ". " + self.allButtons[buttonIndex].name)
    def GetAction(self):
        try: select = int(input("Что вы хотите сделать? - "))
        except ValueError: select = ""
        if select == -1:
            ExitButton()._action()
        elif select == -2:
            self.draw()
            return
        try: 
            self.allButtons[select]._action()
        except KeyError:
            self.draw()
            return
class MainMenu(Menu):
    def __init__(self,name = "⩎ Главни ⩎"):
        super().__init__(name,[MSB("Создать комнату", "host"),MSB("Подключиться к лобби", "connect"),MSB("Лист персонажей","charlist"),ExitButton()])
class CharListMenu(Menu):
    def __init__(self, name = "Список персонажей"):
        buttons = [MSB("Создать нового персонажа", "charcreate"),MSB("Вернуться","main")]
        for char in jsonLoad():
            buttons.insert(0,CharButton(char,char))
        super().__init__(name,buttons)
    def draw(self):
        buttons = [MSB("Создать нового персонажа", "charcreate"),MSB("Вернуться","main")]
        for char in jsonLoad():
            buttons.insert(0,CharButton(char))
        super().__init__(self.name,buttons)
        super().draw()
class CharInfoMenu(Menu):
    def __init__(self,characterName,name = "(42) Просмотр характеристик персонажа (42)"):
        self.CN = characterName
        self.character = jsonLoad()[characterName]
        super().__init__(name,[CharRemoveButton("Удалить персонажа",self.CN),MSB("Вернуться","charlist")])
    def showInfo(self):
        print(self.CN)
        for i in self.character:
            if type(self.character[i]) == dict:
                print("    "+i+":"); self._secretShowD(self.character[i],"    "*2)
            elif type(self.character[i]) ==  list:
                print("    "+i+":"); self._secretShowL(self.character[i],"    "*2)
            else:   print("    "+i + " - " + str(self.character[i]))
    def _secretShowD(self,_dict,deep = "    "):
        for el in _dict:
            if type(_dict[el]) == dict:
                print(deep+el+":"); self._secretShowD(_dict[el],deep*2)
            elif type(_dict[el]) == list:
                print(deep+el+":"); self._secretShowL(_dict[el],deep*2)
            else: print(deep + el + " - " + str(_dict[el]))
    def _secretShowL(self,_list,deep = "    "):
        
        for _ in _list:
            if type(_) == dict:
                self._secretShowD(_,deep*2)
            elif type(_) ==  list:
                self._secretShowL(_,deep*2)
            else:   print(deep + str(_))
class CharCreateMenu(Menu):
    def __init__(self,name = "(55) Создание нового персонажа (55)"):
        super().__init__(name,[MSB("Вернуться","charlist")])
    def showInfo(self):
        self.newCharacter = Character()
        self.newCharacter.name = self.nameGet()
        self.newCharacter.Stats = {
            "class": self.paramGet("JSONS/dnd_classes.json"),
            "race": self.paramGet("JSONS/dnd_races.json"),
            "level": self.levelGet()}
        self.newCharacter.Stats["speed"] = jsonLoad("JSONS/dnd_races.json")[self.newCharacter.Stats["race"]]["speed"]
        self.newCharacter.Stats["experience"] = self.expGet()
        self.newCharacter.Stats["worldview"] = self.paramGet("JSONS/dnd_alingments.json")
        self.newCharacter.Stats["background"] = self.paramGet("JSONS/dnd_backgrounds.json")
        self.newCharacter.BMReset(self.newCharacter.Stats["level"])
        self.newCharacter.skillReset(self.newCharacter.Stats["class"],self.newCharacter.Stats["level"])
        self.newCharacter.Stats["diceStats"] = self.diceStatDispencer()
        self.newCharacter.Stats["lore"] = self.loreGet()
        self.newCharacter.otherStatsReset()
        self.newCharacter.charSave()
        manager("charlist")
    def nameGet(self):
        return input("Введите имя персонажа - ")
    def diceStatDispencer(self):
        choice = int(input(" --------- \n Выберите: \n 1. Случайно \n 2. Вручную(WIP) \n --------- \n"))
        match choice:
            case 1:
                diceStats = self.randomDice()
            case 2:
                diceStats = self.manualDice()
        diceStats = self.adderDiceFromRace(diceStats)
        return diceStats
    def adderDiceFromRace(self,ds):
        raceData = jsonLoad("JSONS/dnd_races.json")[self.newCharacter.Stats["race"]]["CharsUP"]
        for d in raceData:
            ds[d] += raceData[d]
        return ds
    def randomDice(self):
        os.system(clearstr)
        print(self.name)
        ds = {}
        translate = {
            "С":"Strength",
            "Л":"Dexterity",
            "Т":"Constitution",
            "И":"Intelligence",
            "Х":"Charisma",
            "М":"Wisdom"
        }
        constan = {
            "Strength":"",
            "Dexterity":"",
            "Constitution":"",
            "Intelligence":"",
            "Charisma":"",
            "Wisdom":"",
            

            }
        variants = sorted([diceRandomer()._out() for i in range(6)],reverse=True)
        for i in range(6):
            os.system(clearstr)
            print(self.name)
            for d in ds:
                print("Введено - ",d,"-",ds[d])
            for v in variants:
                print(variants.index(v)+1,"-",v,end="  ")
            print(f"\nВведите первую букву характеристики для присвоения первого элемента\n{constan['Strength']}Сила \n{constan['Dexterity']}Ловкость \n{constan['Constitution']}Телосложение \n{constan['Intelligence']}Интеллект \n{constan['Charisma']}Харизма \n{constan['Wisdom']}Мудрость ",end="")
            stat = input("\n").upper()
            constan[translate[stat]] = " --Использовано-- "
            ds[translate[stat]] = variants.pop(0) 
        os.system(clearstr)
        print(self.name)
        return ds

    def loreGet(self):
        os.system(clearstr)
        print(self.name)
        lore = ""
        print("Вводите свою предысторию (<Exit> чтобы закончить)")
        i = 1
        while True:
            story = input(f"{i} абзац - ")
            lore += story + "\n"
            if "<Exit>" in story:
                lore = lore[:lore.find("<Exit>")]
                break
            i += 1
        return lore
    def manualDice(self):
        diceStats = {
            "Strength":8,
            "Dexterity":8,
            "Constitution":8,
            "Intelligence":8,
            "Charisma":8,
            "Wisdom":8}
        return diceStats
    def paramGet(self,link):
        params = {}
        i = 1
        for _className in jsonLoad(link):
            params[i] = ParamSelButton(_className)
            i += 1
        i = 0
        for _p in list(params.keys())[:-1]:
            end = ""
            i += 1
            if i % 2 == 0:
                end = "\n"
            print(str(_p) + ". " + str(params[_p]._action())+"   ",end=end)
        print(str(list(params.keys())[-1]) + ". " + str(params[list(params.keys())[-1]]._action()))
        select = int(input("Введите номер - "))
        os.system(clearstr)
        print(self.name)
        print(f"Выбрано - {params[select]._action()}")
        return params[select]._action()
    def levelGet(self):
        while True:
            level = int(input("Введите уровень персонажа - "))
            if level > 20 or level < 0:
                print("Ошибка == Недопустимый уровень ==")
                continue
            os.system(clearstr)
            print(self.name)
            print(f"Выбран - {level} уровень")
            return level
    def expGet(self):
        exp = int(input("Введите количество опыта - "))
        while True:
            try: maxExp = int(jsonLoad("JSONS/dnd_levels.json")[str(1+self.newCharacter.Stats["level"])]["experience"]) 
            except ValueError: maxExp = math.inf
            if exp < 0:
                exp = 0
            if exp >= maxExp:
                self.newCharacter.Stats["level"] += 1
                exp -= maxExp
                continue
            os.system(clearstr)
            print(self.name)
            print(f"Выбрано {exp} опыта")
            return exp
class ServerCreateMenu(Menu):
    def __init__(self,name = "Создание сервера"):
        super().__init__(name,[MSB("Да я ДМ!", "serverstart"),MSB("Вернуться","main")]) 
    def showInfo(self):
        print("Продолжая вы подстверждаете что вы ... ДМ!!!")
        ServerOBJ = ServerClass()
class ServerStart(Menu):
    def __init__(self):
        pass
    def draw(self):
        ServerOBJ._startServer()
        manager("playerlistmenu")
class ServerJoinMenu(Menu):
    def __init__(self,name = "Подключение к серверу"):
        super().__init__(name,[MSB("Я - подготовленный игрок и хочу присоединиться","joinserver"),MSB("Вернуться","main")])
    def showInfo(self):
        print("Вы уверены, что хотите зайти?")
        ClientOBJ = Client()
class JoinServer():
    def __init__(self):
        pass
    def draw(self):
        ClientOBJ._connectToServer()
        manager("charselectmenu")
class PlayerListMenu(Menu):
    def __init__(self,name = "Список подключенных приключенцев"):
        self.rawButtons = []
        super().__init__(name,self.rawButtons)       
    def buttonPrepare(self):
        self.rawButtons = []
        for i in ServerOBJ.connectedClients.values():
            self.rawButtons.append(PlayerSelectButton(i)) 
        super().buttonPrepare()
allChars = []
class CharacterSelectMenu(Menu):
    def __init__(self,name = "Выбор персонажа"):
        self.rawButtons = []
        super().__init__(name,self.rawButtons)
    def draw(self):
        for char in self._loadCharact():
            self.rawButtons.append(CharacterSelectButton(char))
        super().draw()
    def _loadCharact(self):
        self.rawButtons = []
        allChars = []
        for chName,chSt in jsonLoad().items():
            nCh = Character()
            nCh.setName(chName)
            nCh.setStats(chSt)
            allChars.append(nCh)
        return allChars
class PlayerCharacterMenu(Menu):
    def __init__(self,player,name = "Меню игрока "):
        self.player = player
        self.char = player.character
        self.isDM = True
        super().__init__(name+player.character.name,[])
    def showInfo(self):
        self.showChar(self.char)
    def showStatSTR(self,key):
        name = translateOBJ[key]
        val = self.char.Stats[key]
        if isinstance(val,str) or isinstance(val,int):
            print(str(name.center(88,".")).center(100))
            print(str(str(val).center(88)).center(100))
    def otherStatsShow(self,st):
        print(str("Остальные характеристики".center(88,".")).center(100))
        for key, val in st.items():
            if isinstance(val,str) or isinstance(val,int):
                print(str(translateOBJ[key].center(88,".")).center(100))
                print(str(val).center(100))
            if key == "MaxspellCells":
                continue
    def spCellShow(self,_Cells):
        if "MaxspellCells" not in self.char.Stats["otherStats"]:
            return
        print("Ячейки заклинаний".center(100,"-"))
        _maxCells = self.char.Stats["otherStats"]["MaxspellCells"]
        cellhave = " --***-- "
        celldiact = " ------- "
        cellhavent = " "*9
        
        line = ""
        for cellLevel, count in _maxCells.items():
            if str(count) != "0":
                line += str(cellLevel).center(9)
            else:
                line += cellhavent
        line = line.center(100)
        print(line)
        for repeat in range(max(list(map(int,list(_maxCells.values()))))):
            line = ""
            for cellL in _maxCells.keys():
                if int(repeat) + 1 <= int(_Cells[cellL]):
                    line += cellhave
                elif int(repeat) + 1 <= int(_maxCells[cellL]):
                    line += celldiact
                else:
                    line += cellhavent
            print(line.center(100))
    def showCharStatus(self):
        _status = self.char.status
        _acts = {
            "True":"**+**",
            "False":"-----"
            }
        for repeat in range(3):
            line = ""
            for status in list(_status.keys())[repeat*5:repeat*5+5]:
                line += " " + status.center(18) + " "
            print(line.center(100))
            line = ""
            for _act in list(_status.values())[repeat*5:repeat*5+5]:
                line += " " + _acts[str(_act)].center(18) + " "
            print(line.center(100)) 


    def showChar(self,char):
        print("\033[36;1m")
        tprint(char.name)
        print("\033[0m")
        print("Статы".center(100,"-"))
        self.showStatSTR("class")
        self.showStatSTR("race")
        self.showStatSTR("speed")
        self.showStatSTR("level")
        self.showStatSTR("experience")
        self.showStatSTR("worldview")
        self.showStatSTR("background")
        self.showStatSTR("masterBonus")
        print(str("Умения".center(88,".")).center(100))
        for skill in self.char.Stats["skills"]:
            print(str(skill.center(88)).center(100))
        print(str("Модификаторы".center(88,".")).center(100))
        line = ""
        for dice in self.char.Stats["diceStats"]:
            line += translateOBJ[dice].center(12) + "   "
        print(line.center(100))
        line = ""
        for dice in self.char.Stats["diceStats"].values():
            line += str(dice).center(12) + "   "
        print(line.center(100))
        self.otherStatsShow(self.char.Stats["otherStats"])
        self.spCellShow(self.char.spellCells)
        print("Эффекты".center(100,"-"))
        self.showCharStatus()
    def GetAction(self):
        command = input("Введите команду = ")
        self.comManager(command)
    def comManager(self,command):
        comm = command.split(" ")
        comm.append("NONE42")
        match comm[0]:
            case "-1":
                try: ServerOBJ._closeServer()
                except: ClientOBJ._disconnect()
                quit()
            case "upd":
                self.draw()
            case "help":
                print("""Все команды: \n
                 help - это меню \n
                 lvl (+/-num) - добавить num уровней \n
                 exp (+/-num) - добавить num опыта \n
                 spcell (num) (+/-num2) - прибавить num2 к ячейкам num уровня \n
                 status <Enter> (num) - изменить статус персонажа(если не было - включить и наоборот) \n
                 modif - изменить параметны модификаторов \n
                 inv (add/del) (item) - добавляет или удаляет предмет из инвентаря \n
                 items {magic/loot} - показать предметы выбранной категории (можно оставить пустой) \n
                 spells (add/del) (spell) - добавляет или удаляет используемые заклинания""")
                if self.isDM:
                    print("exit - вернуться на экран выбора игрока")
                input()
                self.draw()
            case "lvl":
                self.char.setLevel(comm[1])
                self.send()
            case "exp":
                self.char.setXp(comm[1])
                self.send()
            case "spcell":
                self.char.spellCellsCh(comm[1],comm[2])
                self.send()
            case "status":
                if comm[1].upper() in self.char.status.keys():
                    self.char.status[comm[1]] = not self.char.status[comm[1]]
                else:
                    for i in self.char.status.keys():
                        print(list(self.char.status.keys()).index(i)+1,i)
                    s = int(input("Выбирети недуг - "))-1
                    self.char.status[list(self.char.status.keys())[s]] = not self.char.status[list(self.char.status.keys())[s]]
                self.send()
            case "inv":
                self.char.invMan(comm[1],comm[2])
            case "exit":
                if self.isDM:
                    manager("playerlistmenu")
                else:
                    self.draw()
            case _:
                self.draw()

    def send(self):
        ServerOBJ.sendToClient(self.player.conn,"newData",self.char.Stats,self.char.spellCells,self.char.status) 
        self.draw()
class CharacterCharacteristicsMenu(PlayerCharacterMenu):
    def __init__(self,char,name = "Меню персонажа "):
        self.rawButtons = []

        self.isDM = False
        self.char = char
        self.name = name + char.name
        self.buttonPrepare()
    def send(self):
        ClientOBJ.sendToServer("newData",self.char.Stats,self.char.spellCells,self.char.status)
        self.draw()
menus = {
    "main" : MainMenu(),
    "host": ServerCreateMenu(),
    "serverstart":ServerStart(),
    "joinserver":JoinServer(),
    "connect" :ServerJoinMenu(),
     "charlist" : CharListMenu(),
     "charcreate": CharCreateMenu(),
     "playerlistmenu": PlayerListMenu(), 
     "charselectmenu": CharacterSelectMenu()
}

def addMenu(name,_class):
    menus[name] = _class

def manager(data):
    menus[data].draw()
if __name__ == "__main__":
    try:
        manager("main")
    except KeyboardInterrupt: ServerOBJ._closeServer(); ClientOBJ._disconnect(); quit() 
