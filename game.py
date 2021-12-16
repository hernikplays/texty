import yaml
from yaml.loader import SafeLoader
from colorama import Fore, Back, Style

class Game:
    def __init__(self,data:dict):
        self.name = data["meta"]["name"]
        self.author = data["meta"]["creator"]
        self.current = "start"
        self.nodes = {}
        for k in data["game"]:
            self.nodes.update({k:data["game"][k]})

    def make_selection(self,selection:int) -> bool:
        if(type(selection) != int or selection >= len(self.nodes[self.current]["actions"]) or selection < 0):
            print("Invalid selection")
            return False
        else:
            self.current = self.nodes[self.current]["actions"][selection]
            return True

    
    def printme(self):
        '''
        Used to print out the current prompt with the options
        '''
        print(self.parse_colors(self.nodes[self.current]["text"]))
        print("")
        ostring = ""
        if("actions" in self.nodes[self.current].keys()):
            for i,option in enumerate(self.nodes[self.current]["actions"]):
                ostring+=f"{i} - {self.nodes[option]['description']}\n"
            print(ostring)
            sel = input("Make a selection (number): ")
            isWrong = self.make_selection(int(sel))
            while isWrong == False:
                sel = input("Make a selection (number): ")
                isWrong = self.make_selection(sel)
            self.printme()

    def parse_colors(self,text:str) -> str:
        '''
        Used to convert color codes in string to colors from the colorama lib
        '''
        newText = text.replace("&b",Fore.CYAN).replace("&c",Fore.RED).replace("&e", Fore.YELLOW).replace("&a",Fore.GREEN).replace("&9",Fore.BLUE).replace("&r",Fore.RESET).replace("&f",Fore.WHITE).replace("&5",Fore.MAGENTA).replace("\n",Fore.RESET + "\n") # replace color codes and newlines with colorama
        newText += Fore.RESET # reset color at the end of the text
        return newText


def load(file_path):
    '''Loads the game from a YAML file to a Game class'''
    try:
        with open(file_path) as f:
            data = yaml.load(f,Loader=SafeLoader)
            g = Game(data)
            return g
    except Exception as e:
        print(f"{Back.RED}{Fore.WHITE}An exception has occured while loading the game from the YAML file:{Fore.RESET}{Back.RESET}")
        print(e)
        return None
