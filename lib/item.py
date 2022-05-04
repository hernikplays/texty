class Item: # Reprezentuje vybavitelný předmět
    def __init__(self,name:str,attack:int = 0,defense:int = 0) -> None:
        self.name = name # Název, jak je zobrazován hráči
        if attack == 0 and defense > 0: # Nastaví typ předmětu
            self.type = "armor"
        else:
            self.type = "weapon"
        self.attack = attack # Stat útoku
        self.defense = defense # Stat obrany