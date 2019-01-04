# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 15:59
# @Author  : Luc
# @Email   : lucyang0901@gmail.com
# @File    : print_colors.py

from colorama import Fore, Style


def green(string):
    print(Fore.GREEN + str(string) + Style.RESET_ALL)


def red(string):
    print(Fore.RED + str(string) + Style.RESET_ALL)


def yellow(string):
    print(Fore.YELLOW + str(string) + Style.RESET_ALL)


def blue(string):
    print(Fore.BLUE + str(string) + Style.RESET_ALL)
