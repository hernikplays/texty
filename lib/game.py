import yaml
from yaml.loader import SafeLoader
from colorama import Fore, Back, Style
import re
from .save import SaveManager
from .ascii import AsciiAnimation
from time import sleep
from os import system, path, mkdir

class Game: # the game class keeps information about the loaded game
    def __init__(self,data:dict):
        self.name = data["meta"]["name"]
        self.author = data["meta"]["creator"]
        self.current = "start"
        self.nodes = {}
        self.inventory = []
        self.save = SaveManager()
        self.id = data["meta"]["id"]
        for k in data["game"]:
            self.nodes.update({k:data["game"][k]})

    def main_menu(self): # displays the main menu
        l = self.save.load()
        if not l:
            # New game
            print(self.name)
            print(self.lang['game_by'].replace("$author",self.author))
            print("")
            print(f"1 - {self.lang['start']}")
            print(f"2 - {self.lang['options']}")
            print(f"0 - {self.lang['quit']}")
            selection = self.make_selection(3)
            system("cls||clear")
            if(selection == 1): # start new game
                self.print_text()
            elif(selection == 2):
                self.settings_menu()
            elif(selection == 0):
                print(self.lang['quitting'])
                exit()
        else: # Display continue
            print(self.name)
            print(self.lang['game_by'].replace("$author",self.author))
            print("")
            print(f"1 - {self.lang['continue']}")
            print(f"2 - {self.lang['new_name']}")
            print(f"3 - {self.lang['settings']}")
            print(f"0 - {self.lang['quit']}")
            selection = self.make_selection(3)
            system("cls||clear")
            if(selection == 1):
                self.current = self.save.currentPrompt
                self.inventory = self.save.inventory
                self.print_text()
            elif(selection == 2):
                self.print_text()
            elif(selection == 3):
                self.settings_menu()
            elif(selection == 0):
                print("Quitting")
                exit()

    def settings_menu(self): # displays the settings menu
        print("Options")
        print("")
        print(f"1 - {self.lang['lang']}")
        print("0 - Back")
        selection = self.make_selection(1)
        if(selection == 1):
            print(self.lang['lang'])
            print("")
            print("1 - English")
            print("2 - Česky")
            print(f"0 - {self.lang['back']}")
            selection = self.make_selection(2)
            system("cls||clear")
            if(selection == 1):
                with open("./saves/lang","w") as f:
                    f.write("en")
            elif(selection == 2):
                with open("./saves/lang","w") as f:
                    f.write("cz")
            self.settings_menu()
        else:
            self.main_menu()

    def make_selection(self, length=0) -> int: # this method makes sure a valid selection is made and returns the selection as a number
        # TODO: replace with selection by keyboard(?)
        l = length # sets the length
        if(l == 0): # if no length was set, we get it from nodes
            l = len(self.nodes[self.current]["actions"])-1
        y = False
        selection = 0
        # TODO: Check for "has_item"
        while y == False: # while the selection is not correct
            try:
                selection = int(input(self.lang['selection'])) # ask for selection
            except ValueError: # handle wrong input type
                print(self.lang['not_number'])
            if(selection > l or selection < 0): # if the number is bigger than the length or smaller than 0, print error
                print(self.lang['invalid'])
            else:
                y = True # else return the selection
        return selection
    
    def print_text(self): # Prints out the current prompt
        system("cls||clear")
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
            if "add_item" in self.nodes[self.current]: # if there is an add_inventory key in the node,
                # add item to inventory
                self.inventory.append(self.nodes[self.current]["add_inventory"])
            self.current = self.nodes[self.current]["actions"][sel]
            self.save.currentPrompt = self.current # save the current prompt
            self.print_text()

    def print_animated(self,animid): # prinst the first found occurence of an ascii animation
        animation = AsciiAnimation()
        animation.load_ascii(animid)
        for frame in animation.frames:
            system("cls||clear")
            print(frame)
            sleep(animation.speed)
        print()
        
    def parse_colors(self,text:str) -> str: # Converts color codes into terminal colors
        newText = text.replace("&b",Fore.CYAN).replace("&c",Fore.RED).replace("&e", Fore.YELLOW).replace("&a",Fore.GREEN).replace("&9",Fore.BLUE).replace("&r",Fore.RESET).replace("&f",Fore.WHITE).replace("&5",Fore.MAGENTA).replace("\n",Fore.RESET + "\n") # replace color codes and newlines with colorama
        newText += Fore.RESET # reset color at the end of the text
        return newText

def load(file_path,lang): # starts to load the game from YAML
    try:
        with open(file_path) as f:
            data = yaml.load(f,Loader=SafeLoader)
            g = Game(data)
            g.lang = lang
            return g
    except Exception as e:
        print(f"{Back.RED}{Fore.WHITE}{g.lang['error_loading']}{Fore.RESET}{Back.RESET}")
        print(e)
        return None
