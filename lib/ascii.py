from tempfile import TemporaryDirectory
from zipfile import ZipFile
from os import listdir
import yaml
class AsciiAnimation:
    def __init__(self) -> None:
        self.frames = []
        self.speed = 0.2

    def load_ascii(self,name:str):
        """
        Returns ASCII by name
        """

        with TemporaryDirectory() as tmpdir: # we enter a temporary directory
            with ZipFile(f"./assets/{name}.asc","r") as z: # extract the asc file
                z.extractall(f"{tmpdir}/ascii/{name}")
                for f in listdir(f"{tmpdir}/ascii/{name}"): # read all the files
                    if f == "config.yml":
                        with open(f"{tmpdir}/ascii/{name}/{f}",encoding="utf-8") as c:
                            data = yaml.load(c,Loader=yaml.SafeLoader)
                            if(data["speed"] != None):
                                self.speed = data["speed"]
                        pass
                    with open(f"{tmpdir}/ascii/{name}/{f}",encoding="utf-8") as f: # add all frames into list
                        self.frames.append(f.read())