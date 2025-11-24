from art import *
from pyfiglet import Figlet
from colorama import Fore, Style

def show_intro():
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT, end='')
    lprint(length=230, height=1, char="*")
    banner = Figlet(font='ansi_shadow', width=200, justify='center').renderText("Survival - Flight \nBy : Group - 1")
    print(banner)
    lprint(length=230, height=1, char="*")
    print(Style.RESET_ALL, end='')
