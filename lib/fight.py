import math

from lib.game import Item
from .ascii import *
from colorama import Fore
import keyboard

class FightHandler:
    def __init__(self,message:str,name:str,hp:int,attacks:list,lang:dict,eq:Item,img:str="") -> None:
        self.selected = 0
        keyboard.add_hotkey("up",self.up)
        keyboard.add_hotkey("down",self.down)
        keyboard.add_hotkey("enter",self.attack)
        self.name = name
        self.max = hp # starting HP
        self.hp = self.max # current HP
        self.attacks = attacks
        self.img = img
        self.lang = lang
        self.message = message
        self.equipped = eq
        input()

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
            if(self.selected == self.selections.index(selection)):
                print(f"{Fore.RED}⚔{Fore.RESET} {selection}")
            else:
                print(f"  {selection}")
        
    def attack(self):
        self.hp
        input()
