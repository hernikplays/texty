from sys import argv
from loader import *

def main():
    if len(argv)<2:
        print("You need to specify a path to a YAML file")
        exit(1)
    else:
        game = load(argv[1])
        game.printme()

if __name__ == "__main__":
    main()

