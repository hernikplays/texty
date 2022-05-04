class Item:
    def __init__(self,name:str,attack:int = 0,defense:int = 0) -> None:
        self.name = name
        if attack == 0 and defense > 0:
            self.type = "armor"
        else:
            self.type = "weapon"
        self.attack = attack
        self.defense = defense