from sys import argv
from game import *
from colorama import init

def main():
    init()
    if len(argv)<2:
        print("You need to specify a path to a YAML file")
        exit(1)
    else:
        game = load(argv[1])
        game.printme()

if __name__ == "__main__":
    main()

