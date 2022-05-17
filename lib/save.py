from time import sleep
from os import path, system
import yaml

from lib.game import Item

class SaveManager: # Spravuje ukládání
    def __init__(self,gid:str,lang):
        self.id = gid # ID hry
        self.currentPrompt = "" # Aktuální node
        self.inventory = [] # Předměty v inventáři
        self.equipped = {"weapon":None,"armor":None} # Výbava
        self.version = 2
        self.lang = lang

    def load(self):
        if(path.exists(f"./saves/{self.id}.yml")):
            with open(f"./saves/{self.id}.yml",encoding="utf-8") as f:
                data = yaml.load(f,Loader=yaml.SafeLoader) # Načteme z YAMLu
                self.currentPrompt = data["currentPrompt"]
                if(data["version"] < self.version): # V případě nekompatibility zobrazit varování
                    system("cls||clear")
                    print(self.lang["no_comp"])
                    sleep(5)
                self.inventory = []
                for item in data["inventory"]: # Zpracovat inventář (zvlášť pouze text a zvlášť vybavitelné)
                    if type(item) is str:
                        self.inventory.append(item)
                    else:
                        i = Item(item["name"],item["atk"],item["def"])
                        self.inventory.append(i)
                        # Přidat stejnou kopii jako vybavenou pokud je vybavena
                        if(data["equipped"]["weapon"] is not None):
                            if(data["equipped"]["weapon"]["name"] == i.name):
                                self.equipped["weapon"] = i
                        if(data["equipped"]["armor"] is not None):
                            if(data["equipped"]["armor"]["name"] == i.name):
                                self.equipped["armor"] = i
                return True
        return False

    def save(self):
        inv = []
        for item in self.inventory:
            if type(item) is str:
                inv.append(item)
            else:
                # Pro vybavitelné předměty
                inv.append({"name":item.name,"atk":item.attack,"def":item.defense})

        # Zpracovat vybavené předměty
        if(self.equipped["weapon"] is not None):
            self.equipped["weapon"] = {"name":self.equipped["weapon"].name,"atk":self.equipped["weapon"].attack}
        if(self.equipped["armor"] is not None):
            self.equipped["armor"] = {"name":self.equipped["armor"].name,"def":self.equipped["armor"].defense}
        data = {"id":self.id,"currentPrompt":self.currentPrompt,"inventory":inv,"version":self.version,"equipped":self.equipped}
        with open(f"./saves/{self.id}.yml",mode="w",encoding="utf-8") as f:
            yaml.dump(data,f)
