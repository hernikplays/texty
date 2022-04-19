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
        self.name = data["meta"]["name"] # Game name
        self.author = data["meta"]["creator"] # Game creator
        self.current = "start" # Current prompt
        self.nodes = {} # All nodes
        self.inventory = [] # Player's inventory
        self.id = data["meta"]["id"]  # Game ID
        self.save = SaveManager(self.id) # saving
        self.equipped = {"weapon":None,"armor":None} # Items equipped by player
        if "equippable" in data["meta"].keys():
            self.equippable = [] # Items that can be equipped by player
            for item in data["meta"]["equippable"]:
                name = list(item.keys())[0]
                if "def" in item[name].keys() and "atk" in item[name].keys():
                    self.equippable.append(Item(name,item[name]["atk"],item[name]["def"]))
                elif "def" in item[name].keys():
                    self.equippable.append(Item(name=name,defense=item[name]["def"]))
                elif "atk" in item[name].keys():
                    self.equippable.append(Item(name,item[name]["atk"]))
                if("starter" in item[name].keys()): # if starter, equip and add to inventory
                    if item[name]["starter"]:
                        i = next((x for x in self.equippable if x.name == list(item.keys())[0]))
                        self.inventory.append(i)
                        self.equipped[i.type] = i
                    
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
            m = MenuManager([self.lang['continue'],self.lang['new_game'],self.lang['options'],self.lang['quit']],f"{self.name}\n{self.lang['game_by'].replace('$author',self.author)}")
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
        if "add_item" in self.nodes[self.current].keys(): # if there is an add_inventory key in the node,
                # add item to inventory
                item = self.nodes[self.current]['add_item']
                if item not in self.inventory:
                    self.inventory.append(item)
                    print(self.inventory)
                    system("clear||cls")
                    print(f"{self.lang['acquire'].replace('$item',f'{Fore.CYAN}{item}{Fore.RESET}')}")
                    sleep(3)
                    system("clear||cls")
        animated = re.search(r"(?!{).+(?=})",self.nodes[self.current]["text"]) # find the animated text
        if(animated != None):
            self.print_animated(animated.group(0))
            self.nodes[self.current]["text"] = self.nodes[self.current]["text"].replace("{"+animated.group(0)+"}","") # remove the animated text from the text prompt
        if("actions" in self.nodes[self.current].keys()):
            actions_desc = [] # has descriptions of text prompts, so that we don't need to find them in MenuManager
            need_item = [] # helps implement a check for needing an item
            for option in self.nodes[self.current]["actions"]:
                try:
                    actions_desc.append(self.nodes[option]["description"])
                    if "has_item" in self.nodes[option].keys(): 
                        need_item.append(self.nodes[option]["has_item"])
                    else:
                        need_item.append(None)
                except Exception:
                    print(f"{Back.RED}{Fore.WHITE}{self.lang['no_action'].replace('$action',option)}{Fore.RESET}")
                    exit(1)
            m = ""
            actions_desc.extend([self.lang['inventory'],self.lang['quit']])
            if(all(element == None for element in need_item) is False):
                need_item.extend([None, None])
                # we need to check if user has item
                m = HasItemDialogue(actions_desc,self.parse_colors(self.nodes[self.current]["text"]),self.inventory,need_item)
                # TODO: Remove item from inventory after using it?
                while need_item[m.selected] != None and all(element not in self.inventory for element in need_item[m.selected]): # until user selects an available prompt, re-prompt again
                    m = HasItemDialogue(actions_desc,self.parse_colors(self.nodes[self.current]["text"]),self.inventory,need_item)
                if m.selected <= len(actions_desc)-3 and "has_item" in self.nodes[self.nodes[self.current]["actions"][m.selected]].keys():
                    for item in need_item[m.selected]:
                        self.inventory.remove(item)
            else:
                m = MenuManager(actions_desc,self.parse_colors(self.nodes[self.current]["text"]))
            sel = m.selected
            if(sel == len(actions_desc)-2): # show inventory
                self.show_inventory()
            elif (sel == len(actions_desc)-1): # Save & quit
                self.save.currentPrompt = self.current # save the current prompt
                self.save.inventory = self.inventory
                self.save.save()
                exit(0)
            else:
                self.current = self.nodes[self.current]["actions"][sel]
                self.print_text()
        else:
            print(self.parse_colors(self.nodes[self.current]["text"]))
            print("")

    def show_inventory(self):
        if len(self.inventory) == 0:
            MenuManager([self.lang["return"]],f"    {self.lang['inside_inv']}    \n")
        else:
            s = ""
            for i,item in enumerate(self.inventory):
                if(i == len(self.inventory)): # last item
                    s += f"- {item}"
                else:
                    s += f"- {item}\n"
            MenuManager([self.lang["return"]],f"    {self.lang['inside_inv']}    \n{s}")
        self.print_text()

    def print_animated(self,animid): # prints the first found occurence of an ascii animation
        animation = AsciiAnimation()
        animation.load_ascii(animid)
        animation.play()
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
        print(f"{Back.RED}{Fore.WHITE}ERROR{Fore.RESET}{Back.RESET}")
        print(e)
        return None

class Item:
    def __init__(self,name:str,attack:int = 0,defense:int = 0) -> None:
        self.name = name
        if attack == 0 and defense > 0:
            self.type = "armor"
        else:
            self.type = "weapon"
        self.attack = attack
        self.defense = defense