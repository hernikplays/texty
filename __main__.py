from genericpath import isdir
import sys
from lib.game import *
from colorama import init, Back, Fore
from os import mkdir, listdir, path

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

def main():
    l = lang()
    init()
    if(not isdir("./games")):
        mkdir("./games")
    games = []
    for file in listdir("./games"):
        if file.endswith("yml") or file.endswith("yaml"):
            # hledá hry
            if len(sys.argv) > 1 and (sys.argv[1] == "-v" or sys.argv[1] == "--verbose"): # nepoužívá try/except pro vypsání celé chybové hlášky (debugování)
                g = load(f"./games/{file}",l)
                if g is not None:
                    games.append(g)
            else:        
                try:
                    # parsuje
                    g = load(f"./games/{file}",l)
                    if g is not None:
                        games.append(g)
                except Exception as e:
                    print(f"{Back.RED}{Fore.WHITE}{l['error_loading']} {file}{Fore.RESET}{Back.RESET}:")
                    print(e)
                    print(l['enter'])
                    input()
    
    # výpis menu
    if len(games) < 1:
        print(l['no_games'])
    else:
        names = []
        for n in games: 
            if(n is not None): 
                names.append(n.name)
        m = MenuManager(names,f"     TEXTY     \n{l['available']}")
        games[m.selected].main_menu()


if __name__ == "__main__":
    main()
