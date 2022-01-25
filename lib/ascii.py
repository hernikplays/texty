from tempfile import TemporaryDirectory
from zipfile import ZipFile
from os import listdir

def ascii_art(name):
    """
    Returns ASCII by name
    """
    a = []

    with TemporaryDirectory() as tmpdir:
        with ZipFile(f"./assets/{name}.asc","r") as z:
            z.extractall(f"{tmpdir}/ascii/{name}")
            for f in listdir(f"{tmpdir}/ascii/{name}"):
                with open(f"{tmpdir}/ascii/{name}/{f}") as f:
                    a.append(f.read())
    return a
