import yaml
from yaml.loader import SafeLoader
from colorama import Fore, Back
import re

from lib.menu import HasItemDialogue, MenuManager
from .save import SaveManager
from .ascii import AsciiAnimation
from time import sleep
from os import system

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
            m = MenuManager([self.lang['start'],self.lang['options'],self.lang['quit']],f"{self.name}\n{self.lang['game_by'].replace('$author',self.author)}")
            selection = m.selected
            system("cls||clear")
            if(selection == 0): # start new game
                self.print_text()
            elif(selection == 1):
                self.settings_menu()
            elif(selection == 2):
                print(self.lang['quitting'])
                exit()
        else: # Display continue
            m = MenuManager([self.lang['continue'],self.lang['new_name'],self.lang['options'],self.lang['quit']],f"{self.name}\n{self.lang['game_by'].replace('$author',self.author)}")
            selection = m.selected
            system("cls||clear")
            if(selection == 0):
                self.current = self.save.currentPrompt
                self.inventory = self.save.inventory
                self.print_text()
            elif(selection == 1):
                self.print_text()
            elif(selection == 2):
                self.settings_menu()
            elif(selection == 3):
                print(self.lang['quitting'])
                exit()

    def settings_menu(self): # displays the settings menu
        m = MenuManager([self.lang['lang'],self.lang['back']],self.lang['options'])
        selection = m.selected
        if(selection == 0):
            m = MenuManager(["English","Česky",self.lang['back']],self.lang['lang'])
            selection = m.selected
            system("cls||clear")
            if(selection == 0):
                with open("./saves/lang","w") as f:
                    f.write("en")
            elif(selection == 1):
                with open("./saves/lang","w") as f:
                    f.write("cz")
            self.settings_menu()
        else:
            self.main_menu()
    
    def print_text(self): # Prints out the current prompt
        system("cls||clear")
        animated = re.search(r"(?!{).+(?=})",self.nodes[self.current]["text"]) # find the animated text
        if(animated != None):
            self.print_animated(animated.group(0))
            self.nodes[self.current]["text"] = self.nodes[self.current]["text"].replace("{"+animated.group(0)+"}","") # remove the animated text from the text prompt
        if("actions" in self.nodes[self.current].keys()):
            actions_desc = []
            need_item = []
            for option in self.nodes[self.current]["actions"]:
                try:
                    actions_desc.append(self.nodes[option]["description"])
                    if "has_item" in self.nodes[option].keys(): 
                        need_item.append(self.nodes[option]["has_item"])
                    else:
                        need_item.append(None)
                except:
                    print(f"{Back.RED}{Fore.WHITE}{self.lang['no_action'].replace('$action',option)}{Fore.RESET}")
                    exit(1)
            m = ""
            if((element == None for element in need_item) is False):
                # we need to check if user has item
                m = HasItemDialogue(self.nodes[self.current]["actions"],self.parse_colors(self.nodes[self.current]["text"]),self.inventory,need_item)
            else:
                m = MenuManager(self.nodes[self.current]["actions"],self.parse_colors(self.nodes[self.current]["text"]))
            sel = m.selected
            if "add_item" in self.nodes[self.current]: # if there is an add_inventory key in the node,
                # add item to inventory
                self.inventory.append(self.nodes[self.current]["add_inventory"])
            self.current = self.nodes[self.current]["actions"][sel]
            self.save.currentPrompt = self.current # save the current prompt
            self.print_text()
        else:
            print(self.parse_colors(self.nodes[self.current]["text"]))
            print("")

    def print_animated(self,animid): # prints the first found occurence of an ascii animation
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
