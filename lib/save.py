from time import sleep
from os import path, system
import yaml

from lib.game import Item

class SaveManager: # manages save and configuration files
    def __init__(self,gid:str,lang):
        self.id = gid # game ID
        self.currentPrompt = "" # Current prompt
        self.inventory = [] # Items in inventory
        self.version = 1
        self.lang = lang

    def load(self):
        if(path.exists(f"./saves/{self.id}.yml")):
            with open(f"./saves/{self.id}.yml",encoding="utf-8") as f:
                data = yaml.load(f,Loader=yaml.SafeLoader)
                self.currentPrompt = data["currentPrompt"]
                if(data["version"] < self.version):
                    system("cls||clear")
                    print(self.lang["no_comp"])
                    sleep(5)
                inv = []
                for item in data["inventory"]:
                    if type(item) is str:
                        inv.append(item)
                    else:
                        # Item class
                        inv.append(Item(item["name"],item["atk"],item["def"]))
                return True
        return False

    def save(self):
        inv = []
        for item in self.inventory:
            if type(item) is str:
                inv.append(item)
            else:
                # Item class
                inv.append({"name":item.name,"atk":item.attack,"def":item.defense})
        data = {"id":self.id,"currentPrompt":self.currentPrompt,"inventory":self.inventory,"version":1}
        with open(f"./saves/{self.id}.yml",mode="w",encoding="utf-8") as f:
            yaml.dump(data,f)
