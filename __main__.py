from genericpath import isdir
from lib.game import *
from colorama import init, Back, Fore
from os import mkdir, listdir

def lang():
    lang = "en"
    if not (path.exists("./saves/lang")):
        mkdir("./saves")
        with open("./saves/lang","w") as f:
            f.write("en")
    else:
        with open("./saves/lang","r") as f:
            lang = f.read()
            if lang == "cz":
                lang = "cz"
    data = ""
    with open(f"./lib/lang/{lang}.yml",encoding="utf-8") as f:
        data = yaml.load(f,Loader=SafeLoader)
    return data

def main(): # TODO: Maybe a menu for available text games?
    l = lang()
    init()
    if(not isdir("./games")):
        mkdir("./games")
    games = []
    for file in listdir("./games"):
        if file.endswith("yml") or file.endswith("yaml"):
            # finds available games
            try:
                # try parsing
                g = load(f"./games/{file}",l)
                games.append(g)
            except Exception as e:
                print(f"{Back.RED}{Fore.RED}{l['error_loading']} {file}:")
                print(e)
    # PRINT OUT GAME SELECT
    # TODO SWITCH TO MENU MANAGER
    print("     TEXTY   ")
    print(l['available'])
    if len(games) < 1:
        print(l['no_games'])
    else:
        for i,g in enumerate(games):
            print(f"{i} - {g.name}")
    print(f"{len(games)} - {l['quit']}")


if __name__ == "__main__":
    main()
