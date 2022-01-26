import yaml
from yaml.loader import SafeLoader
from colorama import Fore, Back, Style
import re
from .ascii import AsciiAnimation
from time import sleep
from os import system

class Game:
    def __init__(self,data:dict):
        self.name = data["meta"]["name"]
        self.author = data["meta"]["creator"]
        self.current = "start"
        self.nodes = {}
        self.inventory = []
        for k in data["game"]:
            self.nodes.update({k:data["game"][k]})

    def make_selection(self) -> int:
        y = False
        selection = 0
        # TODO: Check for "has_item"
        while y == False:
            try:
                selection = int(input("Make a selection (number): "))
            except ValueError:
                print("Not a number selection")
            if(selection >= len(self.nodes[self.current]["actions"]) or selection < 0):
                print("Invalid selection")
            else:
                y = True
        return selection
    
    def print_text(self):
        '''
        Used to print out the current prompt with the options
        '''
        animated = re.search(r"(?!{).+(?=})",self.nodes[self.current]["text"]) # find the animated text
        if(animated != None):
            self.print_animated(animated.group(0))
            self.nodes[self.current]["text"] = self.nodes[self.current]["text"].replace("{"+animated.group(0)+"}","") # remove the animated text from the text prompt
        print(self.parse_colors(self.nodes[self.current]["text"]))
        print("")
        ostring = ""
        if("actions" in self.nodes[self.current].keys()):
            for i,option in enumerate(self.nodes[self.current]["actions"]):
                ostring+=f"{i} - {self.nodes[option]['description']}\n"
            print(ostring)
            sel = self.make_selection()
            if(self.nodes[self.current]["add_inventory"] is not None):
                # add item to inventory
                self.inventory.append(self.nodes[self.current]["add_inventory"])
            self.current = self.nodes[self.current]["actions"][sel]
            self.print_text()

    def print_animated(self,animid):
        '''
        Used to print out animated text,
        currently only prints out the first occurence of an animated text
        (in curly braces)
        '''
        animation = AsciiAnimation()
        animation.load_ascii(animid)
        for frame in animation.frames:
            system("cls||clear")
            print(frame)
            sleep(animation.speed)
        print()
        

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