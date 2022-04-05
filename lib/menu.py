from os import system
import keyboard
from colorama import Fore
class MenuManager:
    '''
    Creates text menus controllable with arrow keys
    '''
    def __init__(self,selections:list,additional:str):
        self.selected = 0 # current selection
        self.selections = selections # available selections
        self.additional = additional # additional text to display above the menu
        keyboard.add_hotkey("up",self.up)
        keyboard.add_hotkey("down",self.down)
        keyboard.add_hotkey("enter",self.make_selection)
        self.show_menu()
        input()

    def make_selection(self) -> int:
        keyboard.remove_all_hotkeys()

    def up(self):
        if self.selected == 0:
            self.selected = len(self.selections)-1
        else:
            self.selected -= 1
        system("cls||clear")
        self.show_menu()

    def down(self):
        if self.selected == len(self.selections)-1:
            self.selected = 0
        else:
            self.selected += 1
        system("cls||clear")
        self.show_menu()

    def show_menu(self):
        print(self.additional)
        for selection in self.selections:
            if(self.selected == self.selections.index(selection)):
                print(f"{Fore.RED}->{Fore.RESET} {selection}")
            else:
                print(f"   {selection}")

class HasItemDialogue(MenuManager):
    '''
    Custom handler for dialogue, that requires to check if the user has an item
    '''
    def __init__(self, selections: list, additional: str,inv:list,need_item:list):
        self.inventory = inv
        self.need_items = need_item
        super().__init__(selections, additional)

    def show_menu(self):
        print(self.additional)
        for i,selection in enumerate(self.selections):
            if(self.need_items[i] != None and self.need_items[i] not in self.inv):
                # user does not have the needed item
                if(self.selected == i):
                    print(f"{Fore.RED}-> {Fore.CYAN}{selection}{Fore.RESET} (Need '{self.need_items[i]}')")
                else:
                    print(f"   {Fore.CYAN}{selection}{Fore.RESET}")
            else:
                # we don't need to change color for an item user doesn't have
                if(self.selected == i):
                    print(f"{Fore.RED}->{Fore.RESET} {selection}")
                else:
                    print(f"   {selection}")
