from tempfile import TemporaryDirectory
from time import sleep
from zipfile import ZipFile
from os import listdir, system
import yaml
class AsciiAnimation:
    def __init__(self) -> None:
        self.frames = []
        self.speed = 0.2

    def load_ascii(self,name:str):
        """
        Loads art from .asc file
        """

        with TemporaryDirectory() as tmpdir: # Vytvoříme dočasnou složku
            with ZipFile(f"./assets/{name}.asc","r") as z: # Extrahujeme asc soubor
                z.extractall(f"{tmpdir}/ascii/{name}")
                for f in listdir(f"{tmpdir}/ascii/{name}"): # Přečte soubory
                    if f == "config.yml":
                        with open(f"{tmpdir}/ascii/{name}/{f}",encoding="utf-8") as c:
                            data = yaml.load(c,Loader=yaml.SafeLoader)
                            if(data["speed"] != None):
                                self.speed = data["speed"]
                    with open(f"{tmpdir}/ascii/{name}/{f}",encoding="utf-8") as f: # Přidá všechny snímky do seznamu
                        self.frames.append(f.read())

    def play(self):
        """
        Plays the animation frame by frame
        """
        for frame in self.frames:
            system("cls||clear")
            print(frame)
            sleep(self.speed)