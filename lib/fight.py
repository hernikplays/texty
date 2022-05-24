import math
from lib.item import Item

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
        self.max = hp # životy nepřítele
        self.hp = self.max # AKTUÁLNÍ životy nepřítele
        self.enemyDef = defense # Obrana nepřítele
        self.my = 30 # životy hráče TODO: maybe make this a variable
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
        h = f"{Fore.RED}■{Fore.RESET}"*p

        j = math.trunc(self.my/30*10)
        a = f"{Fore.GREEN}■{Fore.RESET}"*j
        if str(p).endswith(".5"):
            h += "◾"
        if str(a).endswith(".5"):
            a += "◾"
        print(self.message)
        print(f"{self.lang['you']} {a} {self.my}/30")
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

    def show_inventory(self): # Zobrazuje inventář TODO: Možná taky equipovat?
        system("cls||clear")
        if len(self.inventory) == 0:
            FightMenu([self.lang["return"]],f"    {self.lang['inside_inv']}    \n")
        else:
            op = []
            items = []
            s = ""
            for i,item in enumerate(self.inventory):
                if type(item) is Item: # Pokud je předmět třídy Item, zobrazit zda-li je vybaven nebo ne
                    if self.equipped["weapon"] == item or self.equipped["armor"] == item:
                        op.append(f"- {item.name} | {self.lang['equipped']}")
                    else:
                        op.append(f"- {item.name}")
                    items.append(item)    
                else:
                    if(i == len(self.inventory)): # poslední, nepřidávat newline
                        s += f"- {item}"
                    else:
                        s += f"- {item}\n"
                    items.append(None)    
            op.append(self.lang["return"])       
            m = FightMenu(op,f"    {self.lang['inside_inv']}    \n{s}")
            if(m.selected != len(op)-1):
                # Vybavit
                i = items[m.selected]
                self.equipped[i.type] = i

    def attack(self): # Provede útok vypočítáním ze statů útoku a obrany
        p = randrange(len(self.attacks))
        name = list(self.attacks[p].keys())[0]
        enemyAtk = self.attacks[p][name]["atk"]
        enemyDef = self.enemyDef
        playerAtk = 0
        playerDef = 0
        if self.equipped["weapon"] is not None:
            playerAtk = self.equipped["weapon"].attack
        if self.equipped["armor"] is not None:
            playerDef = self.equipped["armor"].defense

        c = enemyAtk - playerDef
        e = playerAtk - enemyDef
        if c < 0:
            c = 0
        if e < 0:
            e = 0
        self.hp -= e # zásah nepříteli
        self.my -= c # zásah hráči
        self.message = f"{self.lang['enemydmg'].replace('$atk',str(playerAtk - enemyDef)).replace('$name',self.name)}\n{self.lang['playerdmg'].replace('$atk',str(enemyAtk - playerDef)).replace('$name',self.attacks[p][name]['name'])}" # Změnit zprávu

    def defend(self):
        self.message = self.lang["defended"]

class FightMenu(MenuManager): # Upravené menu, které nemá input na konci, protože to jinak buguje
    def __init__(self,selections:list,additional:str):
        keyboard.remove_all_hotkeys()
        self.selected = 0
        self.selections = selections
        self.additional = additional 
        keyboard.add_hotkey("up",self.up)
        keyboard.add_hotkey("down",self.down)
        keyboard.add_hotkey("enter",self.make_selection)
        self.show_menu()
