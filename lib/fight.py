import math

from lib.menu import MenuManager

from .ascii import *
from colorama import Fore
import keyboard
from random import randrange

class FightHandler:
    def __init__(self,message:str,name:str,hp:int,defense:int,attacks:dict,lang:dict,eq:dict,inv:list,img:str="") -> None:
        self.selected = 0
        self.rebind()
        self.name = name
        self.max = hp # starting ENEMY HP
        self.hp = self.max # current ENEMY HP
        self.enemyDef = defense # ENEMY DEF
        self.my = 30 # starting PLAYER HP TODO: maybe make this a variable
        self.attacks = attacks
        self.img = img
        self.lang = lang
        self.message = message
        self.equipped = eq
        self.inventory = inv
        self.show()

    def up(self):
        if self.selected == 0:
            self.selected = 2
        else:
            self.selected -= 1
        system("cls||clear")
        self.show()

    def down(self):
        if self.selected == 2:
            self.selected = 0
        else:
            self.selected += 1
        system("cls||clear")
        self.show()

    def show(self):
        system("cls||clear")
        p = math.trunc(self.hp/self.max*10)
        h = "🟥"*p
        if str(p).endswith(".5"):
            h += "◾"
        print(self.message)
        print(f"{self.name} {h} {self.hp}/{self.max}")
        if self.img != "":
            anim = AsciiAnimation()
            anim.load_ascii(self.img)
            anim.play()
        s = [self.lang["attack"],self.lang["defend"],self.lang["inventory"]]
        for selection in s:
            if(self.selected == s.index(selection)):
                print(f"{Fore.RED}⚔{Fore.RESET} {selection}")
            else:
                print(f"  {selection}")
        
    def make_selection(self) -> None:
        if self.selected == 0:
            self.attack()
        elif self.selected == 1:
            self.defend()
        elif self.selected == 2:
            self.show_inventory()

    def rebind(self):
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey("up",self.up)
        keyboard.add_hotkey("down",self.down)
        keyboard.add_hotkey("enter",self.make_selection)

    def show_inventory(self): # Basically `Game` show_inventory
        system("cls||clear")
        if len(self.inventory) == 0:
            FightMenu([self.lang["return"]],f"    {self.lang['inside_inv']}    \n")
        else:
            s = ""
            for i,item in enumerate(self.inventory):
                if type(item) is not str:
                    if(i == len(self.inventory)): # last item
                        s += f"- {item.name}"
                    else:
                        s += f"- {item.name}\n"
                else:
                    if(i == len(self.inventory)): # last item
                        s += f"- {item}"
                    else:
                        s += f"- {item}\n"
            FightMenu([self.lang["return"]],f"    {self.lang['inside_inv']}    \n{s}")

    def attack(self):
        p = randrange(len(self.attacks))
        name = list(self.attacks[p].keys())[0]
        enemyAtk = self.attacks[p][name]["atk"]
        enemyDef = self.enemyDef
        playerAtk = self.equipped["weapon"].attack
        playerDef = self.equipped["armor"].defense
        self.hp -= playerAtk - enemyDef # enemy takes damage
        self.my -= enemyAtk - playerDef # player takes damage
        self.message = f"{self.lang['enemydmg'].replace('$atk',str(playerAtk - enemyDef)).replace('$name',self.name)}\n{self.lang['playerdmg'].replace('$atk',str(enemyAtk - playerDef)).replace('$name',self.attacks[p][name]['name'])}"

    def defend(self):
        self.message = self.lang["defended"]

class FightMenu(MenuManager):
    def __init__(self,selections:list,additional:str):
        self.selected = 0 # current selection
        self.selections = selections # available selections
        self.additional = additional # additional text to display above the menu
        keyboard.add_hotkey("up",self.up)
        keyboard.add_hotkey("down",self.down)
        keyboard.add_hotkey("enter",self.make_selection)
        self.show_menu()