from tempfile import TemporaryDirectory
from zipfile import ZipFile
from os import listdir

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
                    if f.endswith("yaml"):
                        # TODO: load asc config file
                        pass
                    with open(f"{tmpdir}/ascii/{name}/{f}") as f: # add all frames into list
                        self.frames.append(f.read())