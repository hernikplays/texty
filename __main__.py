from sys import argv
from lib.game import *
from colorama import init

def main(): # TODO: Maybe a menu for available text games?
    init()
    if len(argv)<2:
        print("You need to specify a path to a YAML file")
        exit(1)
    else:
        game = load(argv[1])
        if(game is None):
            exit(1)
        game.main_menu()

if __name__ == "__main__":
    main()