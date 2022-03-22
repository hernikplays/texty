from genericpath import isdir
from lib.game import *
from colorama import init, Back, Fore
from os import mkdir, listdir


def main(): # TODO: Maybe a menu for available text games?
    init()
    if(not isdir("./games")):
        mkdir("./games")
    games = []
    for file in listdir("./games"):
        if file.endswith("yml") or file.endswith("yaml"):
            # finds available games
            try:
                # try parsing
                g = load(f"./games/{file}")
                games.append(g)
            except Exception as e:
                print(f"{Back.RED}{Fore.RED}An exception has occured while loading {file}:")
                print(e)

if __name__ == "__main__":
    main()
