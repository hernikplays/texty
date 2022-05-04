import yaml
from yaml.loader import SafeLoader
from colorama import Fore, Back
import re
from lib.item import Item

from lib.menu import HasItemDialogue, MenuManager
from .save import SaveManager
from .ascii import AsciiAnimation
from .fight import *
from time import sleep
from os import system

class Game: # Hlavní třída, uchovává údaje o hře
    def __init__(self,data:dict,lang):
        self.name = data["meta"]["name"] # Název hry
        self.author = data["meta"]["creator"] # Název tvůrce
        self.current = "start" # Aktuální node
        self.nodes = {} # Seznam všech
        self.inventory = [] # Hráčův inventář
        self.id = data["meta"]["id"]  # "Unikátní" ID hry
        self.lang = lang # Řetězce pro vybraný jazyk
        self.save = SaveManager(self.id,self.lang) # Systém ukládání
        self.equipped = {"weapon":None,"armor":None} # Předměty vybavené hráčem
        self.enemies = {} # Seznam všech nepřátel
        if "equippable" in data["meta"].keys():
            self.equippable = [] # Předměty, které si hráč může vybavit
            for item in data["meta"]["equippable"]:
                name = list(item.keys())[0]
                if "def" in item[name].keys() and "atk" in item[name].keys():
                    self.equippable.append(Item(item[name]["name"],item[name]["atk"],item[name]["def"]))
                elif "def" in item[name].keys():
                    self.equippable.append(Item(name=item[name]["name"],defense=item[name]["def"]))
                elif "atk" in item[name].keys():
                    self.equippable.append(Item(item[name]["name"],item[name]["atk"]))
                if("starter" in item[name].keys()): # Pokud je starter, přidáme hráčí na začátku do inventáře
                    if item[name]["starter"]:
                        i = next((x for x in self.equippable if x.name == list(item.keys())[0]))
                        self.inventory.append(i)
                        self.equipped[i.type] = i
        if "enemies" in data["meta"].keys():
            # Načte nepřátele
            for en in data["meta"]["enemies"]:
                name = list(en.keys())[0]
                self.enemies[name] = {"name":en["name"],"hp":en["hp"],"attacks":en["attacks"],"def":en["def"]}
        for k in data["game"]: # načte všechny nody
            self.nodes.update({k:data["game"][k]})

    def main_menu(self): # Zobrazí hlavní menu
        l = self.save.load()
        if not l:
            # V případě nové hry
            m = MenuManager([self.lang['start'],self.lang['options'],self.lang['quit']],f"{self.name}\n{self.lang['game_by'].replace('$author',self.author)}")
            selection = m.selected
            system("cls||clear")
            if(selection == 0): # Začít
                self.print_text()
            elif(selection == 1): # Nastavení
                self.settings_menu()
            elif(selection == 2): # Vypnout
                print(self.lang['quitting'])
                exit()
        else: # V případě uložené hry zobrazí "Pokračovat"
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

    def settings_menu(self): # Zobrazí nastavení
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
    
    def print_text(self): # Zobrazí hráči aktuální node
        system("cls||clear")
        if "add_item" in self.nodes[self.current].keys(): # V případě, že máme přidat hráči věc do inventáře
                item = self.nodes[self.current]['add_item']
                for i in self.equippable:
                    if i.name == item: # Pokud lze vybavit, změnit na instanci třídy Item
                        item = i
                if item not in self.inventory:
                    self.inventory.append(item)
                    print(self.inventory)
                    system("clear||cls")
                    print(f"{self.lang['acquire'].replace('$item',f'{Fore.CYAN}{item}{Fore.RESET}')}")
                    sleep(3)
                    system("clear||cls")
        animated = re.search(r"(?!{).+(?=})",self.nodes[self.current]["text"]) # Hledá kód pro vložení animovaného textu
        if(animated != None):
            self.print_animated(animated.group(0))
            self.nodes[self.current]["text"] = self.nodes[self.current]["text"].replace("{"+animated.group(0)+"}","") # Odstraní kód z textu
        if("actions" in self.nodes[self.current].keys()):
            actions_desc = [] # uchovává text nodu, abychom jej nemuseli hledat v MenuManager
            need_item = [] # pomáhá implementovat kontrolu potřebného předmětu
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
            if(all(element == None for element in need_item) is False): # Pokud platí, musíme zkontrolovat, jestli hráč má předmět
                need_item.extend([None, None])
                m = HasItemDialogue(actions_desc,self.parse_colors(self.nodes[self.current]["text"]),self.inventory,need_item)
                while need_item[m.selected] != None and all(element not in self.inventory for element in need_item[m.selected]): # Opakovat, dokud uživatel nevybere platný výběr
                    m = HasItemDialogue(actions_desc,self.parse_colors(self.nodes[self.current]["text"]),self.inventory,need_item)
                if m.selected <= len(actions_desc)-3 and "has_item" in self.nodes[self.nodes[self.current]["actions"][m.selected]].keys():
                    for item in need_item[m.selected]:
                        self.inventory.remove(item)
            elif "fight" in self.nodes[self.current].keys():
                # Spustí boj
                enemy = self.enemies[self.nodes[self.current]["fight"]] # Získá info o nepříteli
                m = FightHandler(self.nodes[self.current]["text"],enemy["name"],enemy["hp"],enemy["def"],enemy["attacks"],self.lang,self.equipped,self.inventory)
                input()
                while m.hp > 0 and m.my > 0:
                    m.show()
                    m.rebind() # Znovu nastavuje klávesy, kvůli MenuManageru uvnitř show_inventory, který je maže
                    input()
                system("cls||clear")
                keyboard.remove_all_hotkeys()
                if m.hp < 1:
                    # Nepřítel byl poražen
                    print(self.lang["defeated"].replace("$enemy",enemy["name"]))
                    sleep(3)
                    self.current = self.nodes[self.current]["actions"][0] # Přesune na první akci
                    self.print_text()
                    return
                else:
                    # Hráč byl poražen TODO: Otestovat
                    print(self.lang["defeat"].replace("$enemy",enemy["name"]))
                    sleep(3)
                    self.print_text()
                    return
            else:
                m = MenuManager(actions_desc,self.parse_colors(self.nodes[self.current]["text"]))
            sel = m.selected
            if(sel == len(actions_desc)-2): # Zobrazit inventář
                self.show_inventory()
            elif (sel == len(actions_desc)-1): # Uložit a ukončit
                self.save.currentPrompt = self.current 
                self.save.inventory = self.inventory
                self.save.save()
                exit(0)
            else:
                self.current = self.nodes[self.current]["actions"][sel]
                self.print_text()
        else:
            print(self.parse_colors(self.nodes[self.current]["text"]))
            print("")

    def show_inventory(self): # Zobrazí hráčův inventář
        if len(self.inventory) == 0:
            MenuManager([self.lang["return"]],f"    {self.lang['inside_inv']}    \n")
        else:
            s = ""
            op = [self.lang["return"]]
            for i,item in enumerate(self.inventory):
                if type(item) is Item: # Pokud je předmět třídy Item, zobrazit zda-li je vybaven nebo ne
                    if self.equipped["weapon"] == item or self.equipped["armor"] == item:
                        op.append(f"- {item.name} | {self.lang['equipped']}")
                    else:
                        op.append(f"- {item.name}")
                else:
                    if(i == len(self.inventory)): # poslední, nepřidávat newline
                        s += f"- {item}"
                    else:
                        s += f"- {item}\n"
            m = MenuManager(op,f"    {self.lang['inside_inv']}    \n{s}")
            if(m.selected != len(op)-1):
                # Vybavit
                i = op[m.selected]
                self.equipped[i.type] = i
        self.print_text()

    def print_animated(self,animid): # Zobrazí animaci
        animation = AsciiAnimation()
        animation.load_ascii(animid)
        animation.play()
        print()
        
    def parse_colors(self,text:str) -> str: # Převádí kód na barvy v terminálu
        newText = text.replace("&b",Fore.CYAN).replace("&c",Fore.RED).replace("&e", Fore.YELLOW).replace("&a",Fore.GREEN).replace("&9",Fore.BLUE).replace("&r",Fore.RESET).replace("&f",Fore.WHITE).replace("&5",Fore.MAGENTA).replace("\n",Fore.RESET + "\n") # replace color codes and newlines with colorama
        newText += Fore.RESET # resetovat na konci
        return newText

def load(file_path,lang): # Načte hru z YAML souboru
    try:
        with open(file_path) as f:
            data = yaml.load(f,Loader=SafeLoader)
            g = Game(data,lang)
            return g
    except Exception as e:
        print(f"{Back.RED}{Fore.WHITE}ERROR{Fore.RESET}{Back.RESET}")
        print(e)
        return None