from os import path
import yaml

class SaveManager: # manages save and configuration files
    def __init__(self,id:str):
        self.id = id # game ID
        self.currentPrompt = "" # Current prompt
        self.inventory = [] # Items in inventory

    def load(self):
        if(path.exists(f"./saves/{self.id}.yml")):
            with open(f"./saves/{self.id}.yml",encoding="utf-8") as f:
                data = yaml.load(f,Loader=yaml.SafeLoader)
                self.currentPrompt = data["currentPrompt"]
                self.inventory = data["inventory"]
                return True
        return False

    def save(self):
        data = {"id":self.id,"currentPrompt":self.currentPrompt,"inventory":self.inventory}
        with open(f"./saves/{self.id}.yml",mode="w",encoding="utf-8") as f:
            yaml.dump(data,f)