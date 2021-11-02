import yaml
from yaml.loader import SafeLoader

class Game:
    def __init__(self,name:str,author:str,game:dict):
        self.name = name
        self.author = author
        self.current = "start"
        self.nodes = {}
        for k in game:
            self.nodes.update({k:game[k]})

    def make_selection(self,selection):
        if(selection >= len(self.nodes[self.current][selection]) or selection < 0):
            print("Invalid selection")
        else:
            self.current = self.nodes[self.current][selection]

    
    def printme(self):
        '''
        Used to print out the current prompt with the options
        '''
        print(self.nodes[self.current]["text"])
        print("")
        ostring = ""
        for i,option in enumerate(self.nodes[self.current]["actions"]):
            ostring+=f"{i} - {self.nodes[option]['description']}\n"
        print(ostring)
        sel = input("Make a selection (number): ")

def load(file_path):
    '''Loads the game from a YAML file to a Game class'''
    with open(file_path) as f:
        data = yaml.load(f,Loader=SafeLoader)
        g = Game(data["meta"]["name"],data["meta"]["creator"],data["game"])
        return g