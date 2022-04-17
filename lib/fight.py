import math
from .ascii import *

class FightHandler:
    def __init__(self,name:str,hp:int,attacks:list,img:str="") -> None:
        self.name = name
        self.max = hp # starting HP
        self.hp = self.max # current HP
        self.attacks = attacks
        self.img = img

    def show(self):
        p = math.trunc(self.hp/self.max*10)
        h = "🟥"*p
        if str(p).endswith(".5"):
            h += "◾"
        print(f"{self.name} {h} {self.hp}/{self.max}")
        if self.img != "":
            anim = AsciiAnimation()
            anim.load_ascii(self.img)
            anim.play()
